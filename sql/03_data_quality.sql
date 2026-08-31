-- ============================================================================
-- 03_data_quality.sql
-- Project: E-Commerce Customer, Sales & Business Intelligence Analytics
-- Author: Senior Data Analyst & BI Developer
-- Purpose: 10 Data Quality and Integrity Audits
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Test 1: Check for Duplicate Order IDs in Fact Orders (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 
    'Test 1: Duplicate Order IDs' AS test_name,
    order_id, 
    COUNT(*) AS record_count
FROM fact_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- ----------------------------------------------------------------------------
-- Test 2: Check for Duplicate Customer IDs in Dim Customers (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 
    'Test 2: Duplicate Customer IDs' AS test_name,
    customer_id, 
    COUNT(*) AS record_count
FROM dim_customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- ----------------------------------------------------------------------------
-- Test 3: Check for Null Primary Keys across Core Tables (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 'Test 3: Null PK in Orders' AS test_name, COUNT(*) AS null_pk_count FROM fact_orders WHERE order_id IS NULL
UNION ALL
SELECT 'Test 3: Null PK in Customers', COUNT(*) FROM dim_customers WHERE customer_id IS NULL
UNION ALL
SELECT 'Test 3: Null PK in Products', COUNT(*) FROM dim_products WHERE product_id IS NULL
UNION ALL
SELECT 'Test 3: Null PK in Sellers', COUNT(*) FROM dim_sellers WHERE seller_id IS NULL;

-- ----------------------------------------------------------------------------
-- Test 4: Check for Orphan Foreign Keys in Fact Orders -> Dim Customers (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 
    'Test 4: Orphan Customer FKs in Orders' AS test_name,
    COUNT(o.order_id) AS orphan_count
FROM fact_orders o
LEFT JOIN dim_customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- ----------------------------------------------------------------------------
-- Test 5: Check for Orphan Foreign Keys in Fact Order Items -> Dim Products / Sellers (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 
    'Test 5: Orphan Product FKs in Order Items' AS test_name,
    COUNT(i.order_id) AS orphan_count
FROM fact_order_items i
LEFT JOIN dim_products p ON i.product_id = p.product_id
WHERE p.product_id IS NULL
UNION ALL
SELECT 
    'Test 5: Orphan Seller FKs in Order Items',
    COUNT(i.order_id)
FROM fact_order_items i
LEFT JOIN dim_sellers s ON i.seller_id = s.seller_id
WHERE s.seller_id IS NULL;

-- ----------------------------------------------------------------------------
-- Test 6: Check for Impossible Chronological Delivery Dates (Delivered < Purchased) (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 
    'Test 6: Impossible Delivery Dates' AS test_name,
    COUNT(*) AS invalid_date_records
FROM fact_orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_delivered_customer_date < order_purchase_timestamp;

-- ----------------------------------------------------------------------------
-- Test 7: Check for Invalid Order Status Values (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 
    'Test 7: Invalid Order Statuses' AS test_name,
    order_status, 
    COUNT(*) AS count
FROM fact_orders
WHERE order_status NOT IN ('delivered', 'shipped', 'canceled', 'invoiced', 'processing', 'unavailable', 'created', 'approved')
GROUP BY order_status;

-- ----------------------------------------------------------------------------
-- Test 8: Check for Non-Positive Price or Negative Freight Values (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 
    'Test 8: Invalid Prices/Freight' AS test_name,
    COUNT(*) AS invalid_financial_rows
FROM fact_order_items
WHERE price <= 0 OR freight_value < 0;

-- ----------------------------------------------------------------------------
-- Test 9: Check for Missing Product Categories in Dim Products (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 
    'Test 9: Missing Product Categories' AS test_name,
    COUNT(*) AS missing_category_count
FROM dim_products
WHERE product_category_name_english IS NULL OR product_category_name_english = '';

-- ----------------------------------------------------------------------------
-- Test 10: Check for Duplicate Order Line Items (Expected: 0)
-- ----------------------------------------------------------------------------
SELECT 
    'Test 10: Duplicate Order Items' AS test_name,
    order_id, 
    order_item_id, 
    COUNT(*) AS item_count
FROM fact_order_items
GROUP BY order_id, order_item_id
HAVING COUNT(*) > 1;
