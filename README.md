Amazon Real-Time Sales Data Analytics (Python + MySQL + Power BI)

This project is an end-to-end data analytics pipeline where I simulate real-time Amazon sales product signals, ingest them into MySQL, build daily KPI aggregates, and connect Power BI dashboards** using a live connection (Direct Query/ODBC).  
The goal was to build something that feels like a real business reporting system - not just a one-time analysis.


Project Overview

In many e-commerce companies, the biggest challenge is not just storing data - it’s creating a system that can:

•	continuously ingest new sales product data,
•	calculate daily KPIs automatically,
•	and show business users a dashboard that updates frequently.

In this project, I created a streaming-like pipeline using a Python producer-consumer architecture, stored the data in MySQL, and built a Power BI dashboard for live reporting.

Tech Stack

Python (Producer ,Consumer pipeline)
MySQL + MySQL Workbench (storage + SQL analytics)
Power BI (dashboard + visuals)
Pandas (data processing)
ODBC  Direct Query  (live connection from Power BI to MySQL)

What Data is Included?

The dataset represents Amazon products/sales-related fields such as:

 product title + category
 product rating + review count
pricing & discount
“purchased last month” signal
sponsored / best-seller flags (where available)
time-based snapshots to simulate streaming updates

I included both:
cleaned dataset (used for pipeline)
uncleaned dataset (for cleaning proof)


Architecture (How the system works)

Flow:
1. Producer (Python) reads the cleaned CSV and sends records at a controlled rate (simulating streaming).
2. Consumer (Python) receives records and inserts them into MySQL tables.
3. MySQL stores:
   raw event, snapshot data (fact table)
   product & category dimensions
   daily KPI aggregate table
4. I created SQL views that are Power BI friendly (fast + clean).
5. Power BI connects to MySQL (live), and dashboards refresh as the DB updates.

Repository Structure

text
amazon-realtime-sales-analytics/
data/
rawamazon_products_sales_data_uncleaned.csv
processed/amazon_products_sales_data_cleaned.csv

sql
schema.sql
 views.sql
sample_queries.sql

src
producer.py
consumer.py
db.py
config.yaml

powerbi
amazon_realtime_dashboard.pbix

screenshots
01_executive_overview.png
02_product_drilldown.png
requirements.txt
README.md



Database Design
I used a simple analytics-friendly schema:
•	fact_product_snapshot (raw snapshot/events)
•	dim_product (product info)
•	dim_category (category info)
•	daily_kpi (daily aggregated metrics)
•	plus Power BI views:
o	v_fact_snapshot_enriched
o	v_category_daily_kpi
All table creation queries are available in:
sql schema.sql

Power BI Dashboard
The dashboard is built like a real reporting setup:
•	Page 1: Executive Overview
•	Page 2: Product Drilldown
Page 1 - Executive Overview
This page answers:
•	What’s the current revenue estimate and orders?
•	How is revenue trending daily?
•	Which categories contribute most to revenue?
Page 2 - Product Drilldown
This page answers:
•	Which products are driving the most revenue?
•	How do ratings/reviews relate to performance?
•	Filter by category, best-seller, sponsored (where available)


KPIs Tracked
Main KPIs I calculated in MySQL and displayed in Power BI:
•	Revenue Estimate
•	Orders Estimate
•	Average Rating
•	Products Tracked
•	Category Revenue Contribution
•	Top Products by Revenue

Business Insights (Example Findings)
Here are the types of insights this dashboard is designed to support:
•	Category contribution: Identify which categories generate the highest revenue and should receive inventory/marketing focus.
•	Trend monitoring: Spot days with dips in revenue and investigate changes (price changes, promotions, stockouts).
•	Product winners: Quickly identify top products and replicate success (pricing strategy, promotions, bundles).
•	Review impact: Understand how ratings/reviews correlate with performance.
•	Sponsored / Best-seller impact (if present): Compare performance across sponsored vs non-sponsored items.

How to Run the Pipeline (Local)
1) Install requirements
pip install -r requirements.txt
2) Configure MySQL credentials
Update:
src/config.yaml

3) Create tables + views
Run SQL scripts from:
sql/schema.sql
sql/views.sql

4) Start consumer then producer
Run:
python src/consumer.py
python src/producer.py

Proof / Project Evidence
To make the project verifiable (for CV + GitHub), I included:
•	SQL scripts (schema, views, sample queries)
•	Power BI screenshots
•	PBIX dashboard file
•	Data pipeline code (producer/consumer)
•	Cleaned + raw datasets

Future Improvements
If I extend this project further, I would add:
•	incremental refresh strategy
•	error logging + retry queue
•	scheduled refresh triggers
•	deploying Power BI to service with gateway (true live dashboard)

Author
Hemanth
(Data Analyst | Python | SQL | Power BI)
Next (I can do this for you too)
If you paste your actual KPI numbers (revenue/orders/avg rating) from the dashboard, I’ll add a Key Results  section with real values so it looks even more genuine.



