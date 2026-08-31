# Dataset Setup & Verification Guide

This guide details the origin, schema layout, and setup instructions for the **Brazilian E-Commerce Public Dataset by Olist**.

---

## 1. Source & Acquisition

The dataset comprises real commercial order data from the Olist Store in Brazil across 2016 to 2018.

* **Primary Source**: [Kaggle Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
* **License**: CC BY-NC-SA 4.0 (Open dataset for research and educational purposes)

### Automated Ingestion via Python
If setting up from scratch on a new machine, you can download all files directly via `kagglehub`:
```python
import kagglehub, shutil, os

# Download latest dataset version
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
for file in os.listdir(path):
    shutil.copy2(os.path.join(path, file), "data/raw/")
```

---

## 2. Directory Layout & File Verification

Ensure all 9 CSV files are present in `data/raw/`:

| File Name | Expected Records | Description | Primary Key / Identifier |
| :--- | :--- | :--- | :--- |
| `olist_orders_dataset.csv` | ~99,441 | Order header details, timestamps, statuses | `order_id` |
| `olist_order_items_dataset.csv` | ~112,650 | Order line items, price, freight, seller mapping | `(order_id, order_item_id)` |
| `olist_order_payments_dataset.csv` | ~103,886 | Payment methods, installments, payment values | `(order_id, payment_sequential)` |
| `olist_order_reviews_dataset.csv` | ~99,224 | Customer review scores (1-5), comments, timestamps | `review_id` |
| `olist_customers_dataset.csv` | ~99,441 | Customer unique IDs, zip code prefixes, cities, states | `customer_id` |
| `olist_products_dataset.csv` | ~32,951 | Product dimensions, categories, weight, name lengths | `product_id` |
| `olist_sellers_dataset.csv` | ~3,095 | Seller locations, zip code prefixes, cities, states | `seller_id` |
| `olist_geolocation_dataset.csv` | ~1,000,163 | Zip codes, latitude, longitude coordinates | `geolocation_zip_code_prefix` |
| `product_category_name_translation.csv`| 71 | Portuguese to English category translations | `product_category_name` |

---

## 3. Data Flow & Processing Pipeline

```
Raw CSV Files (data/raw/)
       │
       ▼
Python Cleaning Pipeline (python/data_cleaning.py)
  - Date parsing & timezone alignment
  - Null value imputation / documentation
  - Portuguese to English category translation
  - Deduplication & Primary/Foreign Key validation
       │
       ▼
Feature Engineering (python/feature_engineering.py)
  - Revenue calculation (Price + Freight)
  - Delivery lead times & estimated gaps
  - Customer lifetime spend & frequency
  - Customer segmentation (Low / Medium / High value)
       │
       ▼
Processed CSV Layer (data/processed/) & SQLite Database (data/ecommerce.db)
       │
       ▼
Power BI Data Model & SQL Analytical Engine
```
