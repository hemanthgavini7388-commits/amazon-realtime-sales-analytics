-- schema.sql
CREATE DATABASE IF NOT EXISTS amazon_project;
USE amazon_project;

CREATE TABLE IF NOT EXISTS dim_category (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_name VARCHAR(255) NOT NULL,
  UNIQUE KEY uq_category_name (category_name)
);

CREATE TABLE IF NOT EXISTS dim_product (
  product_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  product_title TEXT,
  product_page_url TEXT,
  product_image_url TEXT,
  UNIQUE KEY uq_product_url (product_page_url(255))
);

CREATE TABLE IF NOT EXISTS fact_product_snapshot (
  snapshot_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  product_id BIGINT NOT NULL,
  category_id INT NOT NULL,
  event_time DATETIME NULL,

  product_rating DECIMAL(3,2) NULL,
  total_reviews INT NULL,
  purchased_last_month INT NULL,

  discounted_price DECIMAL(10,2) NULL,
  original_price DECIMAL(10,2) NULL,
  discount_percentage DECIMAL(5,2) NULL,

  is_best_seller VARCHAR(50) NULL,
  is_sponsored VARCHAR(50) NULL,
  has_coupon VARCHAR(50) NULL,
  buy_box_availability VARCHAR(50) NULL,

  delivery_date DATE NULL,
  sustainability_tags TEXT NULL,

  inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  KEY idx_event_time (event_time),
  KEY idx_category (category_id),
  KEY idx_product (product_id),

  CONSTRAINT fk_fact_product FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  CONSTRAINT fk_fact_category FOREIGN KEY (category_id) REFERENCES dim_category(category_id)
);

CREATE TABLE IF NOT EXISTS daily_kpi (
  kpi_date DATE PRIMARY KEY,
  revenue_estimate DECIMAL(18,2) NULL,
  orders_estimate BIGINT NULL,
  avg_rating DECIMAL(5,3) NULL,
  products BIGINT NULL,
  sponsored_share DECIMAL(6,5) NULL,
  best_seller_count BIGINT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
