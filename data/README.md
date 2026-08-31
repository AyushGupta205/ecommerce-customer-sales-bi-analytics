# Data Directory Documentation

This directory contains the raw and processed datasets for the **E-Commerce Customer, Sales & Business Intelligence Analytics** project.

## Directory Structure

```
data/
├── raw/
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   └── product_category_name_translation.csv
├── processed/
│   ├── dim_customers_clean.csv
│   ├── dim_products_clean.csv
│   ├── dim_sellers_clean.csv
│   ├── dim_geolocation_clean.csv
│   ├── dim_date.csv
│   ├── fact_orders_clean.csv
│   ├── fact_order_items_clean.csv
│   ├── fact_order_payments_clean.csv
│   ├── fact_order_reviews_clean.csv
│   └── analytics_master_orders.csv
└── ecommerce.db
```

## Dataset Lineage

1. **Raw Layer (`data/raw/`)**:
   - Contains immutable copies of the official Brazilian E-Commerce Public Dataset by Olist.
   - Contains 100,000+ orders across 2016–2018 in Brazil.

2. **Processed Layer (`data/processed/`)**:
   - Cleaned, normalized, type-cast, and feature-engineered datasets generated via `python/data_cleaning.py` and `python/feature_engineering.py`.
   - Category names translated from Portuguese to English.
   - Outliers and invalid timestamp anomalies handled systematically.

3. **Database Layer (`data/ecommerce.db`)**:
   - High-performance SQLite database instance populated with normalized tables, primary keys, foreign keys, and indexes for instant SQL analysis.
