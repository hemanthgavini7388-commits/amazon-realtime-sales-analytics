import queue
import time
import yaml
from datetime import datetime
from db import get_conn, upsert_category, upsert_product, insert_fact_many
from producer import start_producer

def safe_date(x):
    if x is None:
        return None
    s = str(x)
    if s.lower() in ("nat", "none", "nan", ""):
        return None
    # MySQL DATE expects YYYY-MM-DD
    return s.split(" ")[0]


def safe_dt(x):
    if x is None:
        return None
    s = str(x).replace("Z", "")
    if s.lower() in ("nat", "none", "nan", ""):
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def main():
    with open("src/config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    mysql_cfg = cfg["mysql"]
    rate = cfg["pipeline"]["rate_per_sec"]
    batch_size = cfg["pipeline"]["batch_size"]
    csv_path = cfg["paths"]["stream_csv"]

    q = queue.Queue(maxsize=5000)

    # Start producer thread
    start_producer(csv_path, q, rate)

    conn = get_conn(mysql_cfg)
    cur = conn.cursor()

    batch = []
    consumed = 0
    t0 = time.time()

    while True:
        item = q.get()
        if item is None:
            break

        category_name = str(item.get("product_category", "Unknown"))
        product_title = str(item.get("product_title", ""))
        page_url = str(item.get("product_page_url", ""))
        image_url = str(item.get("product_image_url", ""))

        category_id = upsert_category(cur, category_name)
        product_id = upsert_product(cur, product_title, page_url, image_url)

        event_time = safe_dt(item.get("data_collected_at"))
        delivery_date = safe_date(item.get("delivery_date"))

        row = (
            product_id, category_id, event_time,
            item.get("product_rating"), item.get("total_reviews"), item.get("purchased_last_month"),
            item.get("discounted_price"), item.get("original_price"), item.get("discount_percentage"),
            item.get("is_best_seller"), item.get("is_sponsored"), item.get("has_coupon"), item.get("buy_box_availability"),
            delivery_date, item.get("sustainability_tags")
        )

        batch.append(row)

        if len(batch) >= batch_size:
            insert_fact_many(cur, batch)
            consumed += len(batch)
            batch.clear()

            elapsed = time.time() - t0
            r = consumed / elapsed if elapsed > 0 else 0
            print(f"[CONSUMER] Inserted {consumed} rows | avg rate {r:.2f} rows/sec")

    if batch:
        insert_fact_many(cur, batch)
        consumed += len(batch)

    print(f"[CONSUMER] Finished. Total inserted: {consumed}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
