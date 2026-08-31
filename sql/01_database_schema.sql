-- ============================================================================
-- 01_database_schema.sql
-- Project: E-Commerce Customer, Sales & Business Intelligence Analytics
-- Author: Senior Data Analyst & BI Developer
-- Engine: MySQL 8.0 & SQLite 3 Compatible DDL
-- ============================================================================

-- Drop existing tables in reverse dependency order
DROP TABLE IF EXISTS fact_order_reviews;
DROP TABLE IF EXISTS fact_order_payments;
DROP TABLE IF EXISTS fact_order_items;
DROP TABLE IF EXISTS fact_orders;
DROP TABLE IF EXISTS dim_products;
DROP TABLE IF EXISTS dim_sellers;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_geolocation;
DROP TABLE IF EXISTS dim_date;

-- ----------------------------------------------------------------------------
-- 1. Dimension: Geolocation (Aggregated unique zip codes)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_geolocation (
    geolocation_zip_code_prefix INT PRIMARY KEY,
    geolocation_lat DECIMAL(10, 6) NOT NULL,
    geolocation_lng DECIMAL(10, 6) NOT NULL,
    geolocation_city VARCHAR(100) NOT NULL,
    geolocation_state VARCHAR(5) NOT NULL
);

-- ----------------------------------------------------------------------------
-- 2. Dimension: Customers
-- ----------------------------------------------------------------------------
CREATE TABLE dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_zip_code_prefix INT NOT NULL,
    customer_city VARCHAR(100) NOT NULL,
    customer_state VARCHAR(5) NOT NULL,
    customer_order_count INT DEFAULT 1,
    customer_total_spend DECIMAL(12, 2) DEFAULT 0.00,
    customer_value_segment VARCHAR(50)
);

CREATE INDEX idx_cust_unique_id ON dim_customers(customer_unique_id);
CREATE INDEX idx_cust_state ON dim_customers(customer_state);
CREATE INDEX idx_cust_zip ON dim_customers(customer_zip_code_prefix);

-- ----------------------------------------------------------------------------
-- 3. Dimension: Sellers
-- ----------------------------------------------------------------------------
CREATE TABLE dim_sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT NOT NULL,
    seller_city VARCHAR(100) NOT NULL,
    seller_state VARCHAR(5) NOT NULL
);

CREATE INDEX idx_seller_state ON dim_sellers(seller_state);
CREATE INDEX idx_seller_zip ON dim_sellers(seller_zip_code_prefix);

-- ----------------------------------------------------------------------------
-- 4. Dimension: Products
-- ----------------------------------------------------------------------------
CREATE TABLE dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g DECIMAL(10, 2),
    product_length_cm DECIMAL(10, 2),
    product_height_cm DECIMAL(10, 2),
    product_width_cm DECIMAL(10, 2),
    product_category_name_english VARCHAR(100) NOT NULL
);

CREATE INDEX idx_prod_category ON dim_products(product_category_name_english);

-- ----------------------------------------------------------------------------
-- 5. Dimension: Date (Time Intelligence)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    date DATE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    quarter_name VARCHAR(10) NOT NULL,
    year_quarter VARCHAR(15) NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    month_short VARCHAR(10) NOT NULL,
    year_month VARCHAR(10) NOT NULL,
    day INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    week_of_year INT NOT NULL,
    is_weekend INT NOT NULL
);

CREATE INDEX idx_date_year_month ON dim_date(year_month);

-- ----------------------------------------------------------------------------
-- 6. Fact: Orders (Header level facts & operational timestamps)
-- ----------------------------------------------------------------------------
CREATE TABLE fact_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    order_status VARCHAR(30) NOT NULL,
    order_purchase_timestamp DATETIME NOT NULL,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME NOT NULL,
    order_date DATE,
    order_year INT,
    order_month INT,
    order_month_name VARCHAR(20),
    order_year_month VARCHAR(10),
    order_quarter INT,
    order_day_of_week VARCHAR(20),
    delivery_days DECIMAL(8, 2),
    approval_days DECIMAL(8, 2),
    estimated_delivery_gap DECIMAL(8, 2),
    is_delayed INT DEFAULT 0,
    customer_unique_id VARCHAR(50),
    customer_city VARCHAR(100),
    customer_state VARCHAR(5),
    customer_order_count INT,
    customer_total_spend DECIMAL(12, 2),
    customer_value_segment VARCHAR(50),
    customer_type VARCHAR(30),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

CREATE INDEX idx_orders_customer_id ON fact_orders(customer_id);
CREATE INDEX idx_orders_status ON fact_orders(order_status);
CREATE INDEX idx_orders_purchase_time ON fact_orders(order_purchase_timestamp);
CREATE INDEX idx_orders_year_month ON fact_orders(order_year_month);

-- ----------------------------------------------------------------------------
-- 7. Fact: Order Items (Line item level price, freight, revenue facts)
-- ----------------------------------------------------------------------------
CREATE TABLE fact_order_items (
    order_id VARCHAR(50) NOT NULL,
    order_item_id INT NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    seller_id VARCHAR(50) NOT NULL,
    shipping_limit_date DATETIME,
    price DECIMAL(10, 2) NOT NULL,
    freight_value DECIMAL(10, 2) NOT NULL,
    revenue DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES fact_orders(order_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
    FOREIGN KEY (seller_id) REFERENCES dim_sellers(seller_id)
);

CREATE INDEX idx_items_order_id ON fact_order_items(order_id);
CREATE INDEX idx_items_product_id ON fact_order_items(product_id);
CREATE INDEX idx_items_seller_id ON fact_order_items(seller_id);

-- ----------------------------------------------------------------------------
-- 8. Fact: Order Payments
-- ----------------------------------------------------------------------------
CREATE TABLE fact_order_payments (
    order_id VARCHAR(50) NOT NULL,
    payment_sequential INT NOT NULL,
    payment_type VARCHAR(50) NOT NULL,
    payment_installments INT NOT NULL,
    payment_value DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES fact_orders(order_id)
);

CREATE INDEX idx_payments_order_id ON fact_order_payments(order_id);
CREATE INDEX idx_payments_type ON fact_order_payments(payment_type);

-- ----------------------------------------------------------------------------
-- 9. Fact: Order Reviews (Customer satisfaction scores)
-- ----------------------------------------------------------------------------
CREATE TABLE fact_order_reviews (
    review_id VARCHAR(50) NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    review_score INT NOT NULL,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME,
    PRIMARY KEY (review_id, order_id),
    FOREIGN KEY (order_id) REFERENCES fact_orders(order_id)
);

CREATE INDEX idx_reviews_order_id ON fact_order_reviews(order_id);
CREATE INDEX idx_reviews_score ON fact_order_reviews(review_score);
