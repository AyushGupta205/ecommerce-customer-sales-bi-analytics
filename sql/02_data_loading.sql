-- ============================================================================
-- 02_data_loading.sql
-- Project: E-Commerce Customer, Sales & Business Intelligence Analytics
-- Author: Senior Data Analyst & BI Developer
-- Purpose: Ingestion scripts for loading cleaned CSV datasets into relational schema
-- ============================================================================

-- NOTE: For automated cross-platform ingestion, use: `python python/export_sqlite_db.py`
-- Below are standard native SQL load commands for MySQL and SQLite environments.

-- ----------------------------------------------------------------------------
-- MySQL 8.0 LOAD DATA INFILE Commands
-- ----------------------------------------------------------------------------

/*
-- 1. Dim Geolocation
LOAD DATA LOCAL INFILE 'data/processed/dim_geolocation_clean.csv'
INTO TABLE dim_geolocation
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 2. Dim Customers
LOAD DATA LOCAL INFILE 'data/processed/dim_customers_clean.csv'
INTO TABLE dim_customers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 3. Dim Sellers
LOAD DATA LOCAL INFILE 'data/processed/dim_sellers_clean.csv'
INTO TABLE dim_sellers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 4. Dim Products
LOAD DATA LOCAL INFILE 'data/processed/dim_products_clean.csv'
INTO TABLE dim_products
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 5. Dim Date
LOAD DATA LOCAL INFILE 'data/processed/dim_date.csv'
INTO TABLE dim_date
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 6. Fact Orders
LOAD DATA LOCAL INFILE 'data/processed/fact_orders_clean.csv'
INTO TABLE fact_orders
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 7. Fact Order Items
LOAD DATA LOCAL INFILE 'data/processed/fact_order_items_clean.csv'
INTO TABLE fact_order_items
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 8. Fact Order Payments
LOAD DATA LOCAL INFILE 'data/processed/fact_order_payments_clean.csv'
INTO TABLE fact_order_payments
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 9. Fact Order Reviews
LOAD DATA LOCAL INFILE 'data/processed/fact_order_reviews_clean.csv'
INTO TABLE fact_order_reviews
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
*/

-- ----------------------------------------------------------------------------
-- SQLite 3 Native CLI Import Instructions
-- ----------------------------------------------------------------------------
/*
.mode csv
.import data/processed/dim_geolocation_clean.csv dim_geolocation
.import data/processed/dim_customers_clean.csv dim_customers
.import data/processed/dim_sellers_clean.csv dim_sellers
.import data/processed/dim_products_clean.csv dim_products
.import data/processed/dim_date.csv dim_date
.import data/processed/fact_orders_clean.csv fact_orders
.import data/processed/fact_order_items_clean.csv fact_order_items
.import data/processed/fact_order_payments_clean.csv fact_order_payments
.import data/processed/fact_order_reviews_clean.csv fact_order_reviews
*/
