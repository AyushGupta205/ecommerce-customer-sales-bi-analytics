"""
Script to generate rich interactive Jupyter Notebooks for Data Cleaning and EDA.
"""

import nbformat as nbf
import os

NOTEBOOKS_DIR = r'd:\Ecomercee\notebooks'
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# NOTEBOOK 1: 01_data_cleaning.ipynb
# -------------------------------------------------------------------------
nb1 = nbf.v4.new_notebook()
nb1.cells = [
    nbf.v4.new_markdown_cell("""# 01 - Data Cleaning, Quality Audits & Normalization Pipeline
### Project: E-Commerce Customer, Sales & Business Intelligence Analytics
**Author:** Senior Data Analyst & BI Developer  
**Dataset:** Brazilian E-Commerce Public Dataset by Olist  

---

## 1. Objectives & Pipeline Overview
The goal of this notebook is to execute an audit and cleaning process across all 9 relational entities of the Brazilian Olist E-Commerce dataset:
1. **Schema & Data Types**: Parse date fields to `datetime64[ns]` and validate numeric keys.
2. **Missing Value Imputation**: Translate Portuguese category names into English and handle null dimensions.
3. **Integrity & Deduplication**: Verify primary keys, eliminate duplicate transactions, and resolve duplicate geolocation entries.
4. **Chronological Validity**: Remove chronological anomalies (e.g. delivered prior to purchase).
5. **Data Export**: Save cleansed datasets into `data/processed/` for SQL ingestion and Power BI modeling.
"""),
    nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np

# Configure display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

RAW_DATA_DIR = '../data/raw'
PROCESSED_DATA_DIR = '../data/processed'
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
print("Data directories initialized successfully.")
"""),
    nbf.v4.new_markdown_cell("""## 2. Ingestion and Inspection of Raw Datasets"""),
    nbf.v4.new_code_cell("""df_orders_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_orders_dataset.csv'))
df_items_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_order_items_dataset.csv'))
df_products_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_products_dataset.csv'))
df_trans_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'product_category_name_translation.csv'))
df_customers_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_customers_dataset.csv'))
df_sellers_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_sellers_dataset.csv'))
df_payments_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_order_payments_dataset.csv'))
df_reviews_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_order_reviews_dataset.csv'))
df_geo_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_geolocation_dataset.csv'))

raw_summary = pd.DataFrame({
    'Dataset': ['Orders', 'Order Items', 'Products', 'Customers', 'Sellers', 'Payments', 'Reviews', 'Geolocation', 'Category Translations'],
    'Row Count': [len(df_orders_raw), len(df_items_raw), len(df_products_raw), len(df_customers_raw), len(df_sellers_raw), len(df_payments_raw), len(df_reviews_raw), len(df_geo_raw), len(df_trans_raw)],
    'Column Count': [df_orders_raw.shape[1], df_items_raw.shape[1], df_products_raw.shape[1], df_customers_raw.shape[1], df_sellers_raw.shape[1], df_payments_raw.shape[1], df_reviews_raw.shape[1], df_geo_raw.shape[1], df_trans_raw.shape[1]]
})
raw_summary
"""),
    nbf.v4.new_markdown_cell("""## 3. Cleansing & Transforming Orders Dataset"""),
    nbf.v4.new_code_cell("""df_orders = df_orders_raw.copy().drop_duplicates(subset=['order_id'])

# Datetime conversions
date_cols = [
    'order_purchase_timestamp', 'order_approved_at',
    'order_delivered_carrier_date', 'order_delivered_customer_date',
    'order_estimated_delivery_date'
]
for col in date_cols:
    df_orders[col] = pd.to_datetime(df_orders[col], errors='coerce')

df_orders['order_status'] = df_orders['order_status'].str.strip().str.lower()

# Chronological validation
invalid_mask = (
    (df_orders['order_status'] == 'delivered') &
    (df_orders['order_delivered_customer_date'].notna()) &
    (df_orders['order_delivered_customer_date'] < df_orders['order_purchase_timestamp'])
)
df_orders = df_orders[~invalid_mask]
print(f"Cleaned orders shape: {df_orders.shape}")
df_orders.head(3)
"""),
    nbf.v4.new_markdown_cell("""## 4. Product Category Translation & Dimension Imputation"""),
    nbf.v4.new_code_cell("""df_products = df_products_raw.copy().drop_duplicates(subset=['product_id'])
df_products = df_products.merge(df_trans_raw, on='product_category_name', how='left')

df_products['product_category_name_english'] = (
    df_products['product_category_name_english']
    .fillna('other_uncategorized')
    .str.replace('_', ' ')
    .str.title()
)
df_products['product_category_name'] = df_products['product_category_name'].fillna('outro')

# Impute dimensions with medians
dim_cols = ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 
            'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
for col in dim_cols:
    df_products[col] = df_products[col].fillna(df_products[col].median())

print(f"Cleaned products shape: {df_products.shape}")
df_products.head(3)
"""),
    nbf.v4.new_markdown_cell("""## 5. Order Items, Payments & Reviews Validation"""),
    nbf.v4.new_code_cell("""# Items
df_items = df_items_raw.copy().drop_duplicates(subset=['order_id', 'order_item_id'])
df_items['shipping_limit_date'] = pd.to_datetime(df_items['shipping_limit_date'], errors='coerce')
df_items = df_items[(df_items['price'] > 0) & (df_items['freight_value'] >= 0)]

# Payments
df_payments = df_payments_raw.copy().drop_duplicates()
df_payments['payment_type'] = df_payments['payment_type'].str.strip().str.lower().str.replace('_', ' ').str.title()
df_payments = df_payments[df_payments['payment_type'] != 'Not Defined']
df_payments = df_payments[df_payments['payment_value'] >= 0]

# Reviews
df_reviews = df_reviews_raw.copy()
df_reviews['review_creation_date'] = pd.to_datetime(df_reviews['review_creation_date'], errors='coerce')
df_reviews['review_answer_timestamp'] = pd.to_datetime(df_reviews['review_answer_timestamp'], errors='coerce')
df_reviews = df_reviews.sort_values('review_answer_timestamp', ascending=False).drop_duplicates(subset=['order_id', 'review_id'])
df_reviews = df_reviews[df_reviews['review_score'].between(1, 5)]
df_reviews['review_comment_title'] = df_reviews['review_comment_title'].fillna('')
df_reviews['review_comment_message'] = df_reviews['review_comment_message'].fillna('')

print("Items:", df_items.shape, "| Payments:", df_payments.shape, "| Reviews:", df_reviews.shape)
"""),
    nbf.v4.new_markdown_cell("""## 6. Customers, Sellers & Geolocation Standardization"""),
    nbf.v4.new_code_cell("""df_customers = df_customers_raw.copy().drop_duplicates(subset=['customer_id'])
df_customers['customer_city'] = df_customers['customer_city'].str.strip().str.title()
df_customers['customer_state'] = df_customers['customer_state'].str.strip().str.upper()

df_sellers = df_sellers_raw.copy().drop_duplicates(subset=['seller_id'])
df_sellers['seller_city'] = df_sellers['seller_city'].str.strip().str.title()
df_sellers['seller_state'] = df_sellers['seller_state'].str.strip().str.upper()

# Geolocation aggregation
valid_coords = (
    (df_geo_raw['geolocation_lat'] >= -35.0) & (df_geo_raw['geolocation_lat'] <= 6.0) &
    (df_geo_raw['geolocation_lng'] >= -75.0) & (df_geo_raw['geolocation_lng'] <= -30.0)
)
df_geo = df_geo_raw[valid_coords].groupby('geolocation_zip_code_prefix').agg(
    geolocation_lat=('geolocation_lat', 'mean'),
    geolocation_lng=('geolocation_lng', 'mean'),
    geolocation_city=('geolocation_city', 'first'),
    geolocation_state=('geolocation_state', 'first')
).reset_index()

print("Customers:", df_customers.shape, "| Sellers:", df_sellers.shape, "| Geolocation:", df_geo.shape)
"""),
    nbf.v4.new_markdown_cell("""## 7. Exporting Cleaned Processed Layer"""),
    nbf.v4.new_code_cell("""df_orders.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_orders_clean.csv'), index=False)
df_items.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_items_clean.csv'), index=False)
df_products.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_products_clean.csv'), index=False)
df_customers.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_customers_clean.csv'), index=False)
df_sellers.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_sellers_clean.csv'), index=False)
df_payments.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_payments_clean.csv'), index=False)
df_reviews.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_reviews_clean.csv'), index=False)
df_geo.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_geolocation_clean.csv'), index=False)
print("Data cleaning completed successfully. 8 normalized files saved.")
""")
]

with open(os.path.join(NOTEBOOKS_DIR, '01_data_cleaning.ipynb'), 'w', encoding='utf-8') as f:
    nbf.write(nb1, f)
print("Saved 01_data_cleaning.ipynb")


# -------------------------------------------------------------------------
# NOTEBOOK 2: 02_exploratory_data_analysis.ipynb
# -------------------------------------------------------------------------
nb2 = nbf.v4.new_notebook()
nb2.cells = [
    nbf.v4.new_markdown_cell("""# 02 - Exploratory Data Analysis & Business Intelligence
### Project: E-Commerce Customer, Sales & Business Intelligence Analytics
**Author:** Senior Data Analyst & BI Developer  
**Dataset:** Cleaned Brazilian Olist E-Commerce Dataset  

---

## 1. Objectives
This notebook performs statistical analysis and business intelligence investigation:
1. **Executive KPIs**: Gross Revenue (Product + Freight), Total Orders, AOV, Delivery Rate, Customer Satisfaction.
2. **Sales & Category Dynamics**: Revenue and item volume across product categories and price points.
3. **Customer Intelligence**: Retention metrics (New vs Repeat Customers) and Customer Lifetime Value (CLV) Segmentation.
4. **Delivery Performance & Operational Efficiency**: Lead-time distributions and fulfillment analysis.
5. **Correlation Investigation**: Empirical analysis of delivery lead time vs customer review scores.
"""),
    nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
pd.set_option('display.max_columns', None)

PROCESSED_DATA_DIR = '../data/processed'

df_master = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'analytics_master_orders.csv'))
df_items = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_items_clean.csv'))
df_products = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_products_clean.csv'))
df_customers = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_customers_clean.csv'))
df_reviews = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_reviews_clean.csv'))

df_items_prod = df_items.merge(df_products[['product_id', 'product_category_name_english']], on='product_id', how='left')
print("Datasets loaded successfully.")
"""),
    nbf.v4.new_markdown_cell("""## 2. Core Executive KPIs"""),
    nbf.v4.new_code_cell("""tot_revenue = df_items['revenue'].sum()
tot_orders = df_master['order_id'].nunique()
tot_customers = df_customers['customer_unique_id'].nunique()
aov = tot_revenue / tot_orders
delivered_rate = (df_master['order_status'] == 'delivered').mean() * 100
avg_review = df_reviews['review_score'].mean()
avg_delivery = df_master[df_master['order_status'] == 'delivered']['delivery_days'].mean()

kpi_table = pd.DataFrame({
    'Metric': ['Gross Revenue', 'Total Orders', 'Unique Customers', 'Average Order Value (AOV)', 'Delivery Rate', 'Average Review Score', 'Average Delivery Time'],
    'Value': [f"R$ {tot_revenue:,.2f}", f"{tot_orders:,}", f"{tot_customers:,}", f"R$ {aov:.2f}", f"{delivered_rate:.2f}%", f"{avg_review:.2f} / 5.0", f"{avg_delivery:.1f} days"]
})
kpi_table
"""),
    nbf.v4.new_markdown_cell("""## 3. Monthly Revenue & Order Growth Trend"""),
    nbf.v4.new_code_cell("""monthly_trend = df_master[df_master['order_year_month'] >= '2017-01'].groupby('order_year_month').agg(
    Revenue=('total_order_revenue', 'sum'),
    Orders=('order_id', 'nunique')
).reset_index()

fig, ax1 = plt.subplots(figsize=(12, 5))
ax2 = ax1.twinx()

ax1.plot(monthly_trend['order_year_month'], monthly_trend['Revenue'] / 1e3, color='#2B6CB0', marker='o', linewidth=2.5, label='Revenue (k BRL)')
ax2.bar(monthly_trend['order_year_month'], monthly_trend['Orders'], alpha=0.3, color='#4A5568', label='Orders')

ax1.set_title("Monthly Revenue & Order Volume Growth (2017 - 2018)", fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel("Year-Month")
ax1.set_ylabel("Revenue (Thousands BRL)", color='#2B6CB0')
ax2.set_ylabel("Order Count", color='#4A5568')
ax1.set_xticklabels(monthly_trend['order_year_month'], rotation=45, ha='right')
plt.show()
"""),
    nbf.v4.new_markdown_cell("""## 4. Category Sales & Pricing Structure"""),
    nbf.v4.new_code_cell("""cat_summary = df_items_prod.groupby('product_category_name_english').agg(
    Revenue=('revenue', 'sum'),
    Items_Sold=('order_item_id', 'count'),
    Avg_Price=('price', 'mean')
).sort_values('Revenue', ascending=False)

top10 = cat_summary.head(10)
plt.figure(figsize=(10, 5))
sns.barplot(data=top10.reset_index(), y='product_category_name_english', x='Revenue', palette='Blues_r', hue='product_category_name_english', legend=False)
plt.title("Top 10 Product Categories by Gross Revenue (BRL)", fontsize=13, fontweight='bold')
plt.xlabel("Revenue (BRL)")
plt.ylabel("")
plt.show()
"""),
    nbf.v4.new_markdown_cell("""## 5. Customer Retention & Value Segmentation"""),
    nbf.v4.new_code_cell("""cust_retention = df_customers.groupby('customer_unique_id')['customer_order_count'].first()
new_c = (cust_retention == 1).sum()
rep_c = (cust_retention > 1).sum()

plt.figure(figsize=(6, 6))
plt.pie([new_c, rep_c], labels=[f'One-Time ({new_c:,})', f'Repeat ({rep_c:,})'], autopct='%1.1f%%',
        colors=['#4299E1', '#48BB78'], startangle=140, wedgeprops=dict(width=0.45, edgecolor='white'))
plt.title("Customer Retention Proportion (New vs Repeat)", fontsize=13, fontweight='bold')
plt.show()
"""),
    nbf.v4.new_markdown_cell("""## 6. Correlation Analysis: Delivery Lead Time vs Review Rating"""),
    nbf.v4.new_code_cell("""deliv_rev = df_master[df_master['order_status'] == 'delivered'].dropna(subset=['delivery_days', 'review_score'])
corr = deliv_rev['delivery_days'].corr(deliv_rev['review_score'])
print(f"Pearson Correlation between Delivery Days and Review Score: {corr:.4f}")

deliv_rev['delivery_tier'] = pd.cut(
    deliv_rev['delivery_days'],
    bins=[0, 5, 10, 15, 20, 30, 60, 200],
    labels=['0-5 Days', '6-10 Days', '11-15 Days', '16-20 Days', '21-30 Days', '31-60 Days', '60+ Days']
)
tier_summary = deliv_rev.groupby('delivery_tier', observed=False).agg(
    Orders=('order_id', 'count'),
    Avg_Rating=('review_score', 'mean'),
    Pct_5_Star=('review_score', lambda x: (x == 5).mean() * 100),
    Pct_1_Star=('review_score', lambda x: (x == 1).mean() * 100)
).reset_index()

print("\\nDelivery Days Tier vs Customer Satisfaction:")
tier_summary
""")
]

with open(os.path.join(NOTEBOOKS_DIR, '02_exploratory_data_analysis.ipynb'), 'w', encoding='utf-8') as f:
    nbf.write(nb2, f)
print("Saved 02_exploratory_data_analysis.ipynb")
