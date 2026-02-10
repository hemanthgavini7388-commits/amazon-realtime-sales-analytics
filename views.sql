-- views.sql
USE amazon_project;

CREATE OR REPLACE VIEW v_fact_snapshot_enriched AS
SELECT
  f.snapshot_id,
  f.event_time,
  DATE(f.event_time) AS kpi_date,
  p.product_title,
  p.product_page_url,
  c.category_name,
  f.product_rating,
  f.total_reviews,
  f.purchased_last_month,
  f.discounted_price,
  f.original_price,
  f.discount_percentage,
  f.is_best_seller,
  f.is_sponsored,
  f.has_coupon,
  f.buy_box_availability,
  f.delivery_date,
  f.sustainability_tags,
  (COALESCE(f.discounted_price,0) * COALESCE(f.purchased_last_month,0)) AS revenue_estimate
FROM fact_product_snapshot f
JOIN dim_product p ON p.product_id = f.product_id
JOIN dim_category c ON c.category_id = f.category_id;

CREATE OR REPLACE VIEW v_category_daily_kpi AS
SELECT
  DATE(f.event_time) AS kpi_date,
  c.category_name,
  ROUND(SUM(COALESCE(f.discounted_price,0) * COALESCE(f.purchased_last_month,0)), 2) AS revenue_estimate,
  SUM(COALESCE(f.purchased_last_month,0)) AS orders_estimate,
  ROUND(AVG(f.product_rating), 3) AS avg_rating,
  COUNT(DISTINCT f.product_id) AS products
FROM fact_product_snapshot f
JOIN dim_category c ON c.category_id = f.category_id
WHERE f.event_time IS NOT NULL
GROUP BY DATE(f.event_time), c.category_name;
