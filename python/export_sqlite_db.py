"""
E-Commerce Database Loader and Validation Runner
================================================
Author: Senior Data Analyst & BI Developer
Project: E-Commerce Customer, Sales & Business Intelligence Analytics

Populates data/ecommerce.db using SQLite/SQLAlchemy and executes the 10 data quality audits.
"""

import os
import sys
import sqlite3
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
DB_PATH = os.path.join(BASE_DIR, 'data', 'ecommerce.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'sql', '01_database_schema.sql')


def populate_sqlite_database():
    """
    Creates SQLite database, executes schema DDL, and loads processed CSV files.
    """
    logger.info("Initializing SQLite database at: %s", DB_PATH)
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        logger.info("Removed existing database instance.")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read and execute schema
    logger.info("Applying DDL schema from %s...", SCHEMA_PATH)
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    logger.info("Schema tables and indexes created successfully.")
    
    # Load processed CSVs
    table_files = {
        'dim_geolocation': 'dim_geolocation_clean.csv',
        'dim_customers': 'dim_customers_clean.csv',
        'dim_sellers': 'dim_sellers_clean.csv',
        'dim_products': 'dim_products_clean.csv',
        'dim_date': 'dim_date.csv',
        'fact_orders': 'fact_orders_clean.csv',
        'fact_order_items': 'fact_order_items_clean.csv',
        'fact_order_payments': 'fact_order_payments_clean.csv',
        'fact_order_reviews': 'fact_order_reviews_clean.csv'
    }
    
    for table_name, csv_name in table_files.items():
        csv_path = os.path.join(PROCESSED_DATA_DIR, csv_name)
        if not os.path.exists(csv_path):
            logger.error("Missing expected CSV: %s", csv_path)
            continue
        
        logger.info("Loading table `%s` from %s...", table_name, csv_name)
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        logger.info("Loaded %d rows into `%s`.", len(df), table_name)
        
    conn.close()
    logger.info("Database loading complete. Standalone SQLite instance is ready.")


def run_data_quality_tests():
    """
    Executes the 10 data quality checks from sql/03_data_quality.sql and returns test results.
    """
    logger.info("Executing 10 Data Quality tests against SQLite database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    tests = [
        ("Test 1: Duplicate Order IDs", 
         "SELECT COUNT(*) FROM (SELECT order_id FROM fact_orders GROUP BY order_id HAVING COUNT(*) > 1);", 0),
        ("Test 2: Duplicate Customer IDs", 
         "SELECT COUNT(*) FROM (SELECT customer_id FROM dim_customers GROUP BY customer_id HAVING COUNT(*) > 1);", 0),
        ("Test 3: Null Primary Keys in Fact Orders", 
         "SELECT COUNT(*) FROM fact_orders WHERE order_id IS NULL;", 0),
        ("Test 4: Orphan Customer FKs in Orders", 
         "SELECT COUNT(o.order_id) FROM fact_orders o LEFT JOIN dim_customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL;", 0),
        ("Test 5: Orphan Product FKs in Order Items", 
         "SELECT COUNT(i.order_id) FROM fact_order_items i LEFT JOIN dim_products p ON i.product_id = p.product_id WHERE p.product_id IS NULL;", 0),
        ("Test 6: Impossible Delivery Dates (Delivered < Purchased)", 
         "SELECT COUNT(*) FROM fact_orders WHERE order_status = 'delivered' AND order_delivered_customer_date IS NOT NULL AND order_delivered_customer_date < order_purchase_timestamp;", 0),
        ("Test 7: Invalid Order Statuses", 
         "SELECT COUNT(*) FROM fact_orders WHERE order_status NOT IN ('delivered', 'shipped', 'canceled', 'invoiced', 'processing', 'unavailable', 'created', 'approved');", 0),
        ("Test 8: Non-Positive Price or Negative Freight", 
         "SELECT COUNT(*) FROM fact_order_items WHERE price <= 0 OR freight_value < 0;", 0),
        ("Test 9: Missing Categories in Dim Products", 
         "SELECT COUNT(*) FROM dim_products WHERE product_category_name_english IS NULL OR product_category_name_english = '';", 0),
        ("Test 10: Duplicate Order Items (Composite PK)", 
         "SELECT COUNT(*) FROM (SELECT order_id, order_item_id FROM fact_order_items GROUP BY order_id, order_item_id HAVING COUNT(*) > 1);", 0)
    ]
    
    results = []
    print("\n" + "="*80)
    print(" SQL DATA QUALITY AUDIT REPORT")
    print("="*80)
    
    all_passed = True
    for test_name, query, expected in tests:
        cursor.execute(query)
        actual = cursor.fetchone()[0]
        passed = (actual == expected)
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status}] {test_name:<55} Expected: {expected} | Actual: {actual}")
        results.append({'test_name': test_name, 'expected': expected, 'actual': actual, 'status': status})
        
    conn.close()
    print("="*80)
    print(f"Overall Data Quality Result: {'ALL TESTS PASSED' if all_passed else 'TEST FAILURES DETECTED'}\n")
    return results


if __name__ == '__main__':
    populate_sqlite_database()
    run_data_quality_tests()
