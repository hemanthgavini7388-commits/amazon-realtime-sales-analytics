import mysql.connector

def get_conn(cfg: dict):
    return mysql.connector.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        port=cfg.get("port", 3306),
        autocommit=True
    )

def upsert_category(cur, category_name: str) -> int:
    cur.execute(
        "INSERT INTO dim_category(category_name) VALUES(%s) "
        "ON DUPLICATE KEY UPDATE category_name=VALUES(category_name)",
        (category_name,)
    )
    cur.execute("SELECT category_id FROM dim_category WHERE category_name=%s", (category_name,))
    return cur.fetchone()[0]

def upsert_product(cur, title: str, page_url: str, image_url: str) -> int:
    cur.execute(
        "INSERT INTO dim_product(product_title, product_page_url, product_image_url) "
        "VALUES(%s,%s,%s) "
        "ON DUPLICATE KEY UPDATE product_title=VALUES(product_title), product_image_url=VALUES(product_image_url)",
        (title, page_url, image_url)
    )
    cur.execute("SELECT product_id FROM dim_product WHERE product_page_url=%s", (page_url,))
    return cur.fetchone()[0]

def insert_fact_many(cur, rows: list[tuple]):
    sql = """
    INSERT INTO fact_product_snapshot(
      product_id, category_id, event_time,
      product_rating, total_reviews, purchased_last_month,
      discounted_price, original_price, discount_percentage,
      is_best_seller, is_sponsored, has_coupon, buy_box_availability,
      delivery_date, sustainability_tags
    ) VALUES (
      %s,%s,%s,
      %s,%s,%s,
      %s,%s,%s,
      %s,%s,%s,%s,
      %s,%s
    )
    """
    cur.executemany(sql, rows)
