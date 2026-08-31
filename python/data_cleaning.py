"""
E-Commerce Data Analytics Pipeline - Data Cleaning Module
=========================================================
Author: Senior Data Analyst & BI Developer
Project: E-Commerce Customer, Sales & Business Intelligence Analytics

This script performs robust extraction, quality audits, cleaning, and normalization
of the raw Brazilian E-Commerce Public Dataset by Olist.
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
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')


def clean_orders(df_orders: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the orders dataset:
    - Parses datetime columns
    - Validates order status
    - Filters out chronological anomalies (e.g. delivered before purchase)
    """
    logger.info("Cleaning orders dataset (Initial shape: %s)...", df_orders.shape)
    df = df_orders.copy()
    
    # 1. Deduplication
    df = df.drop_duplicates(subset=['order_id'])
    
    # 2. Datetime conversions
    date_cols = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        
    # 3. Standardize order status
    df['order_status'] = df['order_status'].str.strip().str.lower()
    
    # 4. Check for chronological sanity
    # Delivered orders should have delivered date >= purchase timestamp
    invalid_mask = (
        (df['order_status'] == 'delivered') &
        (df['order_delivered_customer_date'].notna()) &
        (df['order_delivered_customer_date'] < df['order_purchase_timestamp'])
    )
    if invalid_mask.sum() > 0:
        logger.warning("Found %d records where delivery date is earlier than purchase date. Correcting...", invalid_mask.sum())
        df = df[~invalid_mask]
        
    logger.info("Orders cleaning complete (Final shape: %s).", df.shape)
    return df


def clean_products(df_products: pd.DataFrame, df_trans: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans products dataset:
    - Translates Portuguese category names to English
    - Imputes missing categories and physical dimensions
    """
    logger.info("Cleaning products dataset (Initial shape: %s)...", df_products.shape)
    df = df_products.copy()
    
    # Deduplication
    df = df.drop_duplicates(subset=['product_id'])
    
    # Merge translation
    df = df.merge(df_trans, on='product_category_name', how='left')
    
    # Clean and fill category names
    df['product_category_name_english'] = (
        df['product_category_name_english']
        .fillna('other_uncategorized')
        .str.replace('_', ' ')
        .str.title()
    )
    df['product_category_name'] = df['product_category_name'].fillna('outro')
    
    # Handle numeric dimension missing values with medians
    dim_cols = [
        'product_name_lenght', 'product_description_lenght',
        'product_photos_qty', 'product_weight_g',
        'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    for col in dim_cols:
        if col in df.columns:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            
    logger.info("Products cleaning complete (Final shape: %s).", df.shape)
    return df


def clean_customers(df_customers: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans customers dataset:
    - Standardizes city and state text casing
    - Validates customer_id and customer_unique_id
    """
    logger.info("Cleaning customers dataset (Initial shape: %s)...", df_customers.shape)
    df = df_customers.copy()
    
    df = df.drop_duplicates(subset=['customer_id'])
    df['customer_city'] = df['customer_city'].str.strip().str.title()
    df['customer_state'] = df['customer_state'].str.strip().str.upper()
    df['customer_zip_code_prefix'] = df['customer_zip_code_prefix'].astype(int)
    
    logger.info("Customers cleaning complete (Final shape: %s).", df.shape)
    return df


def clean_sellers(df_sellers: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans sellers dataset:
    - Standardizes city and state
    """
    logger.info("Cleaning sellers dataset (Initial shape: %s)...", df_sellers.shape)
    df = df_sellers.copy()
    
    df = df.drop_duplicates(subset=['seller_id'])
    df['seller_city'] = df['seller_city'].str.strip().str.title()
    df['seller_state'] = df['seller_state'].str.strip().str.upper()
    df['seller_zip_code_prefix'] = df['seller_zip_code_prefix'].astype(int)
    
    logger.info("Sellers cleaning complete (Final shape: %s).", df.shape)
    return df


def clean_order_items(df_items: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans order items dataset:
    - Parses shipping limit date
    - Validates price > 0 and freight_value >= 0
    """
    logger.info("Cleaning order items dataset (Initial shape: %s)...", df_items.shape)
    df = df_items.copy()
    
    df = df.drop_duplicates(subset=['order_id', 'order_item_id'])
    df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')
    
    # Enforce non-negative values
    df = df[df['price'] > 0]
    df = df[df['freight_value'] >= 0]
    
    logger.info("Order items cleaning complete (Final shape: %s).", df.shape)
    return df


def clean_payments(df_payments: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans payments dataset:
    - Enforces payment value >= 0
    - Standardizes payment method names
    """
    logger.info("Cleaning payments dataset (Initial shape: %s)...", df_payments.shape)
    df = df_payments.copy()
    
    # Drop pure duplicate payment entries
    df = df.drop_duplicates()
    
    # Standardize payment types
    df['payment_type'] = df['payment_type'].str.strip().str.lower().str.replace('_', ' ').str.title()
    df = df[df['payment_type'] != 'Not Defined']
    
    # Payment value should be positive
    df = df[df['payment_value'] >= 0]
    
    logger.info("Payments cleaning complete (Final shape: %s).", df.shape)
    return df


def clean_reviews(df_reviews: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans reviews dataset:
    - Formats review timestamps
    - Fills missing review comment text
    - Deduplicates review entries
    """
    logger.info("Cleaning reviews dataset (Initial shape: %s)...", df_reviews.shape)
    df = df_reviews.copy()
    
    # Keep latest review for duplicate review_id / order_id combinations
    df['review_creation_date'] = pd.to_datetime(df['review_creation_date'], errors='coerce')
    df['review_answer_timestamp'] = pd.to_datetime(df['review_answer_timestamp'], errors='coerce')
    df = df.sort_values('review_answer_timestamp', ascending=False).drop_duplicates(subset=['order_id', 'review_id'])
    
    # Enforce review score within range [1, 5]
    df = df[df['review_score'].between(1, 5)]
    
    # Fill and sanitize text nulls and remove multi-line break characters for clean CSV parsing
    df['review_comment_title'] = (
        df['review_comment_title']
        .fillna('')
        .astype(str)
        .str.replace('\r', ' ', regex=False)
        .str.replace('\n', ' ', regex=False)
        .str.strip()
    )
    df['review_comment_message'] = (
        df['review_comment_message']
        .fillna('')
        .astype(str)
        .str.replace('\r', ' ', regex=False)
        .str.replace('\n', ' ', regex=False)
        .str.strip()
    )
    
    logger.info("Reviews cleaning complete (Final shape: %s).", df.shape)
    return df


def clean_geolocation(df_geo: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and deduplicates geolocation dataset:
    - Groups by zip code prefix to calculate mean latitude & longitude
    - Removes invalid coordinates outside Brazilian geographical bounds
    """
    logger.info("Cleaning geolocation dataset (Initial shape: %s)...", df_geo.shape)
    df = df_geo.copy()
    
    # Filter valid Brazilian coordinate ranges: Lat [-34, 6], Lon [-74, -34]
    valid_coords = (
        (df['geolocation_lat'] >= -35.0) & (df['geolocation_lat'] <= 6.0) &
        (df['geolocation_lng'] >= -75.0) & (df['geolocation_lng'] <= -30.0)
    )
    df = df[valid_coords]
    
    # Standardize city and state
    df['geolocation_city'] = df['geolocation_city'].str.strip().str.title()
    df['geolocation_state'] = df['geolocation_state'].str.strip().str.upper()
    
    # Aggregate to 1 row per zip_code_prefix
    df_dedup = df.groupby('geolocation_zip_code_prefix').agg(
        geolocation_lat=('geolocation_lat', 'mean'),
        geolocation_lng=('geolocation_lng', 'mean'),
        geolocation_city=('geolocation_city', 'first'),
        geolocation_state=('geolocation_state', 'first')
    ).reset_index()
    
    logger.info("Geolocation deduplication complete (Final shape: %s).", df_dedup.shape)
    return df_dedup


def run_cleaning_pipeline():
    """
    Executes the end-to-end cleaning pipeline across all raw CSVs and saves results.
    """
    logger.info("Starting Data Cleaning Pipeline...")
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    # Load raw files
    df_orders_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_orders_dataset.csv'))
    df_items_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_order_items_dataset.csv'))
    df_products_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_products_dataset.csv'))
    df_trans_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'product_category_name_translation.csv'))
    df_customers_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_customers_dataset.csv'))
    df_sellers_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_sellers_dataset.csv'))
    df_payments_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_order_payments_dataset.csv'))
    df_reviews_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_order_reviews_dataset.csv'))
    df_geo_raw = pd.read_csv(os.path.join(RAW_DATA_DIR, 'olist_geolocation_dataset.csv'))
    
    # Clean datasets
    df_orders = clean_orders(df_orders_raw)
    df_products = clean_products(df_products_raw, df_trans_raw)
    df_customers = clean_customers(df_customers_raw)
    df_sellers = clean_sellers(df_sellers_raw)
    df_items = clean_order_items(df_items_raw)
    df_payments = clean_payments(df_payments_raw)
    df_reviews = clean_reviews(df_reviews_raw)
    df_geo = clean_geolocation(df_geo_raw)
    
    # Save cleaned datasets
    df_orders.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_orders_clean.csv'), index=False)
    df_items.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_items_clean.csv'), index=False)
    df_products.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_products_clean.csv'), index=False)
    df_customers.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_customers_clean.csv'), index=False)
    df_sellers.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_sellers_clean.csv'), index=False)
    df_payments.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_payments_clean.csv'), index=False)
    df_reviews.to_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_reviews_clean.csv'), index=False)
    df_geo.to_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_geolocation_clean.csv'), index=False)
    
    logger.info("All 8 clean datasets successfully exported to %s", PROCESSED_DATA_DIR)


if __name__ == '__main__':
    run_cleaning_pipeline()
