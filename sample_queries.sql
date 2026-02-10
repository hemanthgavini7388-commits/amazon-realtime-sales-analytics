-- sample_queries.sql
USE amazon_project;

-- Proof counts (good for screenshots)
SELECT COUNT(*) AS rows_in_fact FROM fact_product_snapshot;
SELECT COUNT(*) AS products FROM dim_product;
SELECT COUNT(*) AS categories FROM dim_category;

-- Latest inserted rows
SELECT snapshot_id, event_time, delivery_date, discounted_price, purchased_last_month
FROM fact_product_snapshot
ORDER BY snapshot_id DESC
LIMIT 10;

-- Daily KPI view check
SELECT *
FROM v_category_daily_kpi
ORDER BY kpi_date DESC, revenue_estimate DESC
LIMIT 20;

-- Top 10 categories by revenue
SELECT
  category_name,
  ROUND(SUM(revenue_estimate), 2) AS revenue_estimate,
  SUM(orders_estimate) AS orders_estimate,
  ROUND(AVG(avg_rating), 2) AS avg_rating
FROM v_category_daily_kpi
GROUP BY category_name
ORDER BY revenue_estimate DESC
LIMIT 10;

-- Sponsored vs Organic share
SELECT
  ROUND(AVG(CASE WHEN LOWER(is_sponsored) LIKE '%sponsored%' THEN 1 ELSE 0 END), 4) AS sponsored_share,
  ROUND(1 - AVG(CASE WHEN LOWER(is_sponsored) LIKE '%sponsored%' THEN 1 ELSE 0 END), 4) AS organic_share
FROM fact_product_snapshot;

-- Update daily_kpi table (aggregation)
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

-- Check daily_kpi results
SELECT * FROM daily_kpi ORDER BY kpi_date DESC LIMIT 20;
