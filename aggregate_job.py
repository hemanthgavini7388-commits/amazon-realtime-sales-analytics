import yaml
from db import get_conn

def main():
    with open("src/config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    conn = get_conn(cfg["mysql"])
    cur = conn.cursor()

    sql = """
    INSERT INTO daily_kpi (kpi_date, revenue_estimate, orders_estimate, avg_rating, products, sponsored_share, best_seller_count)
    SELECT
      DATE(event_time) AS kpi_date,
      SUM(COALESCE(discounted_price,0) * COALESCE(purchased_last_month,0)) AS revenue_estimate,
      SUM(COALESCE(purchased_last_month,0)) AS orders_estimate,
      AVG(product_rating) AS avg_rating,
      COUNT(DISTINCT product_id) AS products,
      AVG(CASE WHEN LOWER(is_sponsored) LIKE '%sponsored%' THEN 1 ELSE 0 END) AS sponsored_share,
      SUM(CASE WHEN LOWER(is_best_seller) LIKE '%best%' THEN 1 ELSE 0 END) AS best_seller_count
    FROM fact_product_snapshot
    WHERE event_time IS NOT NULL
    GROUP BY DATE(event_time)
    ON DUPLICATE KEY UPDATE
      revenue_estimate=VALUES(revenue_estimate),
      orders_estimate=VALUES(orders_estimate),
      avg_rating=VALUES(avg_rating),
      products=VALUES(products),
      sponsored_share=VALUES(sponsored_share),
      best_seller_count=VALUES(best_seller_count);
    """
    cur.execute(sql)
    print("[AGG] daily_kpi updated.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
