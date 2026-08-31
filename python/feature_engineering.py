"""
E-Commerce Data Analytics Pipeline - Feature Engineering Module
===============================================================
Author: Senior Data Analyst & BI Developer
Project: E-Commerce Customer, Sales & Business Intelligence Analytics

This module constructs analytical dimensions, customer segments, operational lead times,
revenue aggregations, and date dimension tables.
"""

import os
import sys
import logging
import pandas as pd
import numpy as np

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')


def build_date_dimension(start_date: str = '2016-01-01', end_date: str = '2018-12-31') -> pd.DataFrame:
    """
    Generates a continuous Date Dimension table for Star Schema modeling and Time Intelligence.
    """
    logger.info("Generating DimDate dimension from %s to %s...", start_date, end_date)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    df_date = pd.DataFrame({'date': dates})
    
    df_date['date_key'] = df_date['date'].dt.strftime('%Y%m%d').astype(int)
    df_date['year'] = df_date['date'].dt.year
    df_date['quarter'] = df_date['date'].dt.quarter
    df_date['quarter_name'] = 'Q' + df_date['quarter'].astype(str)
    df_date['year_quarter'] = df_date['year'].astype(str) + '-' + df_date['quarter_name']
    df_date['month'] = df_date['date'].dt.month
    df_date['month_name'] = df_date['date'].dt.strftime('%B')
    df_date['month_short'] = df_date['date'].dt.strftime('%b')
    df_date['year_month'] = df_date['date'].dt.strftime('%Y-%m')
    df_date['day'] = df_date['date'].dt.day
    df_date['day_of_week'] = df_date['date'].dt.dayofweek + 1  # 1 = Monday, 7 = Sunday
    df_date['day_name'] = df_date['date'].dt.strftime('%A')
    df_date['week_of_year'] = df_date['date'].dt.isocalendar().week.astype(int)
    df_date['is_weekend'] = df_date['day_of_week'].isin([6, 7]).astype(int)
    
    logger.info("DimDate generated (%d rows).", len(df_date))
    return df_date


def engineer_features():
    """
    Enriches datasets with business metrics and constructs analytics master dataset.
    """
    logger.info("Starting Feature Engineering...")
    
    # 1. Load Cleaned Datasets
    df_orders = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_orders_clean.csv'))
    df_items = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_items_clean.csv'))
    df_products = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_products_clean.csv'))
    df_customers = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_customers_clean.csv'))
    df_sellers = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_sellers_clean.csv'))
    df_payments = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_payments_clean.csv'))
    df_reviews = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_reviews_clean.csv'))
    
    # Convert timestamps
    for col in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
                'order_delivered_customer_date', 'order_estimated_delivery_date']:
        df_orders[col] = pd.to_datetime(df_orders[col], errors='coerce')
        
    # 2. Order Operational & Lead Time Metrics
    df_orders['order_date'] = df_orders['order_purchase_timestamp'].dt.date
    df_orders['order_year'] = df_orders['order_purchase_timestamp'].dt.year
    df_orders['order_month'] = df_orders['order_purchase_timestamp'].dt.month
    df_orders['order_month_name'] = df_orders['order_purchase_timestamp'].dt.strftime('%B')
    df_orders['order_year_month'] = df_orders['order_purchase_timestamp'].dt.strftime('%Y-%m')
    df_orders['order_quarter'] = df_orders['order_purchase_timestamp'].dt.quarter
    df_orders['order_day_of_week'] = df_orders['order_purchase_timestamp'].dt.strftime('%A')
    
    # Delivery duration (days)
    df_orders['delivery_days'] = (
        (df_orders['order_delivered_customer_date'] - df_orders['order_purchase_timestamp'])
        .dt.total_seconds() / 86400.0
    ).round(2)
    
    # Approval duration (days)
    df_orders['approval_days'] = (
        (df_orders['order_approved_at'] - df_orders['order_purchase_timestamp'])
        .dt.total_seconds() / 86400.0
    ).round(2)
    
    # Estimated delivery gap (Estimated - Actual delivered): >0 means arrived early, <0 means late
    df_orders['estimated_delivery_gap'] = (
        (df_orders['order_estimated_delivery_date'] - df_orders['order_delivered_customer_date'])
        .dt.total_seconds() / 86400.0
    ).round(2)
    
    df_orders['is_delayed'] = (df_orders['estimated_delivery_gap'] < 0).astype(int)
    
    # 3. Item Level Revenue
    # Total Revenue per item = price + freight_value
    df_items['revenue'] = (df_items['price'] + df_items['freight_value']).round(2)
    
    # 4. Aggregated Order Value Metrics
    order_items_agg = df_items.groupby('order_id').agg(
        total_items=('order_item_id', 'count'),
        total_item_price=('price', 'sum'),
        total_freight=('freight_value', 'sum'),
        total_order_revenue=('revenue', 'sum')
    ).reset_index()
    
    # Payment aggregation per order
    order_payments_agg = df_payments.groupby('order_id').agg(
        total_payment_value=('payment_value', 'sum'),
        primary_payment_type=('payment_type', 'first'),
        max_installments=('payment_installments', 'max')
    ).reset_index()
    
    # Review score per order
    order_reviews_agg = df_reviews.groupby('order_id').agg(
        review_score=('review_score', 'mean'),
        has_review_comment=('review_comment_message', lambda x: (x != '').any())
    ).reset_index()
    
    order_reviews_agg['review_category'] = pd.cut(
        order_reviews_agg['review_score'],
        bins=[0, 2, 3, 5],
        labels=['Negative (1-2)', 'Neutral (3)', 'Positive (4-5)']
    )
    
    # 5. Customer Lifetime Value (CLV) & Frequency
    # Merge orders with customer_unique_id
    df_orders_cust = df_orders.merge(
        df_customers[['customer_id', 'customer_unique_id', 'customer_city', 'customer_state']],
        on='customer_id',
        how='left'
    )
    
    # Calculate Customer-level summary
    cust_order_summary = df_orders_cust.groupby('customer_unique_id').agg(
        customer_order_count=('order_id', 'nunique'),
        first_order_timestamp=('order_purchase_timestamp', 'min'),
        last_order_timestamp=('order_purchase_timestamp', 'max')
    ).reset_index()
    
    # Merge order revenues into customer summary
    cust_revenue = df_orders_cust.merge(order_items_agg[['order_id', 'total_order_revenue']], on='order_id', how='left')
    cust_spend = cust_revenue.groupby('customer_unique_id')['total_order_revenue'].sum().reset_index()
    cust_spend.rename(columns={'total_order_revenue': 'customer_total_spend'}, inplace=True)
    
    cust_summary = cust_order_summary.merge(cust_spend, on='customer_unique_id', how='left')
    cust_summary['customer_total_spend'] = cust_summary['customer_total_spend'].fillna(0.0).round(2)
    
    # Segment definition:
    # Low Value: spend < 100
    # Medium Value: 100 <= spend <= 500
    # High Value: spend > 500
    cust_summary['customer_value_segment'] = pd.cut(
        cust_summary['customer_total_spend'],
        bins=[-np.inf, 100, 500, np.inf],
        labels=['Low Value (<$100)', 'Medium Value ($100-$500)', 'High Value (>$500)']
    )
    
    # Update dim_customers with enriched attributes
    df_customers_enriched = df_customers.merge(
        cust_summary[['customer_unique_id', 'customer_order_count', 'customer_total_spend', 'customer_value_segment']],
        on='customer_unique_id',
        how='left'
    )
    
    # Flag Repeat vs New Customers on orders
    df_orders_cust = df_orders_cust.merge(
        cust_summary[['customer_unique_id', 'customer_order_count', 'customer_total_spend', 'customer_value_segment']],
        on='customer_unique_id',
        how='left'
    )
    df_orders_cust['customer_type'] = np.where(df_orders_cust['customer_order_count'] > 1, 'Repeat Customer', 'New Customer')
    
    # 6. Construct Master Analytics Orders Table
    logger.info("Constructing master analytics orders table...")
    df_master = df_orders_cust.merge(order_items_agg, on='order_id', how='left')
    df_master = df_master.merge(order_payments_agg, on='order_id', how='left')
    df_master = df_master.merge(order_reviews_agg, on='order_id', how='left')
    
    # 7. Generate Date Dimension
    df_dim_date = build_date_dimension()
    
    # 8. Export Enhanced Tables
    df_orders_cust.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_orders_clean.csv'), index=False)
    df_items.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_items_clean.csv'), index=False)
    df_customers_enriched.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_customers_clean.csv'), index=False)
    df_dim_date.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_date.csv'), index=False)
    df_master.to_csv(os.path.join(PROCESSED_DATA_DIR, 'analytics_master_orders.csv'), index=False)
    
    logger.info("Feature engineering complete. Enriched datasets exported successfully.")


if __name__ == '__main__':
    engineer_features()
