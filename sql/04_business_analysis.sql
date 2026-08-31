-- ============================================================================
-- 04_business_analysis.sql
-- Project: E-Commerce Customer, Sales & Business Intelligence Analytics
-- Author: Senior Data Analyst & BI Developer
-- Purpose: 24 Core Analytical Business Questions & KPIs
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Total Orders
-- ----------------------------------------------------------------------------
SELECT COUNT(DISTINCT order_id) AS total_orders 
FROM fact_orders;

-- ----------------------------------------------------------------------------
-- 2. Delivered Orders & Delivery Rate
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(CASE WHEN order_status = 'delivered' THEN 1 END) AS delivered_orders,
    COUNT(*) AS total_orders,
    ROUND(100.0 * COUNT(CASE WHEN order_status = 'delivered' THEN 1 END) / COUNT(*), 2) AS delivery_rate_pct
FROM fact_orders;

-- ----------------------------------------------------------------------------
-- 3. Cancelled Orders & Cancellation Rate
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(CASE WHEN order_status = 'canceled' THEN 1 END) AS canceled_orders,
    ROUND(100.0 * COUNT(CASE WHEN order_status = 'canceled' THEN 1 END) / COUNT(*), 2) AS cancellation_rate_pct
FROM fact_orders;

-- ----------------------------------------------------------------------------
-- 4. Total Gross Revenue (Product Sales + Freight)
-- ----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(price), 2) AS total_product_sales,
    ROUND(SUM(freight_value), 2) AS total_freight_value,
    ROUND(SUM(revenue), 2) AS total_gross_revenue
FROM fact_order_items;

-- ----------------------------------------------------------------------------
-- 5. Average Order Value (AOV)
-- ----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(i.revenue) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM fact_orders o
JOIN fact_order_items i ON o.order_id = i.order_id;

-- ----------------------------------------------------------------------------
-- 6. Monthly Gross Revenue Trend (Excluding Ramp-up Period < 2017)
-- ----------------------------------------------------------------------------
SELECT 
    o.order_year_month,
    ROUND(SUM(i.revenue), 2) AS monthly_revenue,
    ROUND(SUM(i.price), 2) AS monthly_item_sales,
    ROUND(SUM(i.freight_value), 2) AS monthly_freight
FROM fact_orders o
JOIN fact_order_items i ON o.order_id = i.order_id
WHERE o.order_year_month >= '2017-01'
GROUP BY o.order_year_month
ORDER BY o.order_year_month;

-- ----------------------------------------------------------------------------
-- 7. Monthly Orders Trend
-- ----------------------------------------------------------------------------
SELECT 
    order_year_month,
    COUNT(DISTINCT order_id) AS monthly_orders
FROM fact_orders
WHERE order_year_month >= '2017-01'
GROUP BY order_year_month
ORDER BY order_year_month;

-- ----------------------------------------------------------------------------
-- 8. Top 10 Product Categories by Gross Revenue
-- ----------------------------------------------------------------------------
SELECT 
    p.product_category_name_english AS category,
    COUNT(i.order_item_id) AS items_sold,
    ROUND(SUM(i.revenue), 2) AS total_revenue,
    ROUND(AVG(i.price), 2) AS avg_item_price
FROM fact_order_items i
JOIN dim_products p ON i.product_id = p.product_id
GROUP BY p.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 9. Top 10 Individual Products by Revenue
-- ----------------------------------------------------------------------------
SELECT 
    i.product_id,
    p.product_category_name_english AS category,
    COUNT(i.order_item_id) AS units_sold,
    ROUND(SUM(i.revenue), 2) AS product_total_revenue
FROM fact_order_items i
JOIN dim_products p ON i.product_id = p.product_id
GROUP BY i.product_id, p.product_category_name_english
ORDER BY product_total_revenue DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 10. Bottom 10 Product Categories by Gross Revenue
-- ----------------------------------------------------------------------------
SELECT 
    p.product_category_name_english AS category,
    COUNT(i.order_item_id) AS items_sold,
    ROUND(SUM(i.revenue), 2) AS total_revenue
FROM fact_order_items i
JOIN dim_products p ON i.product_id = p.product_id
GROUP BY p.product_category_name_english
ORDER BY total_revenue ASC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 11. Gross Revenue by Customer State
-- ----------------------------------------------------------------------------
SELECT 
    o.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(i.revenue), 2) AS total_revenue,
    ROUND(SUM(i.revenue) / COUNT(DISTINCT o.order_id), 2) AS state_aov
FROM fact_orders o
JOIN fact_order_items i ON o.order_id = i.order_id
GROUP BY o.customer_state
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- 12. Order Volume by State
-- ----------------------------------------------------------------------------
SELECT 
    customer_state,
    COUNT(DISTINCT order_id) AS order_volume,
    ROUND(100.0 * COUNT(DISTINCT order_id) / (SELECT COUNT(*) FROM fact_orders), 2) AS order_share_pct
FROM fact_orders
GROUP BY customer_state
ORDER BY order_volume DESC;

-- ----------------------------------------------------------------------------
-- 13. Payment Method Analysis
-- ----------------------------------------------------------------------------
SELECT 
    payment_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS avg_payment_value,
    ROUND(AVG(payment_installments), 1) AS avg_installments
FROM fact_order_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;

-- ----------------------------------------------------------------------------
-- 14. Installment Analysis
-- ----------------------------------------------------------------------------
SELECT 
    payment_installments,
    COUNT(*) AS transaction_count,
    ROUND(SUM(payment_value), 2) AS total_value,
    ROUND(AVG(payment_value), 2) AS avg_value
FROM fact_order_payments
WHERE payment_type = 'Credit Card'
GROUP BY payment_installments
ORDER BY payment_installments;

-- ----------------------------------------------------------------------------
-- 15. Review Score Distribution
-- ----------------------------------------------------------------------------
SELECT 
    review_score,
    COUNT(*) AS review_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM fact_order_reviews), 2) AS score_share_pct
FROM fact_order_reviews
GROUP BY review_score
ORDER BY review_score DESC;

-- ----------------------------------------------------------------------------
-- 16. Overall Average & Median Delivery Time
-- ----------------------------------------------------------------------------
SELECT 
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(approval_days), 2) AS avg_approval_days,
    ROUND(AVG(estimated_delivery_gap), 2) AS avg_estimated_buffer_days
FROM fact_orders
WHERE order_status = 'delivered';

-- ----------------------------------------------------------------------------
-- 17. Delivery Time by Customer State
-- ----------------------------------------------------------------------------
SELECT 
    customer_state,
    COUNT(order_id) AS delivered_orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(100.0 * SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) / COUNT(order_id), 2) AS delay_rate_pct
FROM fact_orders
WHERE order_status = 'delivered'
GROUP BY customer_state
ORDER BY avg_delivery_days ASC;

-- ----------------------------------------------------------------------------
-- 18. Delivery Time by Product Category (Top 10 Categories)
-- ----------------------------------------------------------------------------
SELECT 
    p.product_category_name_english AS category,
    COUNT(DISTINCT o.order_id) AS orders_count,
    ROUND(AVG(o.delivery_days), 2) AS avg_delivery_days
FROM fact_orders o
JOIN fact_order_items i ON o.order_id = i.order_id
JOIN dim_products p ON i.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name_english
HAVING COUNT(DISTINCT o.order_id) >= 500
ORDER BY avg_delivery_days ASC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 19. New vs Repeat Customer Analysis
-- ----------------------------------------------------------------------------
SELECT 
    customer_type,
    COUNT(DISTINCT customer_unique_id) AS customer_count,
    ROUND(100.0 * COUNT(DISTINCT customer_unique_id) / (SELECT COUNT(DISTINCT customer_unique_id) FROM dim_customers), 2) AS customer_pct,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_order_revenue), 2) AS total_revenue
FROM (
    SELECT 
        o.customer_type,
        o.customer_unique_id,
        o.order_id,
        SUM(i.revenue) AS total_order_revenue
    FROM fact_orders o
    JOIN fact_order_items i ON o.order_id = i.order_id
    GROUP BY o.customer_type, o.customer_unique_id, o.order_id
) sub
GROUP BY customer_type;

-- ----------------------------------------------------------------------------
-- 20. Customer Spending Segmentation Summary
-- ----------------------------------------------------------------------------
SELECT 
    customer_value_segment,
    COUNT(DISTINCT customer_unique_id) AS customer_count,
    ROUND(SUM(customer_total_spend), 2) AS total_spend,
    ROUND(AVG(customer_total_spend), 2) AS avg_spend_per_customer
FROM dim_customers
GROUP BY customer_value_segment
ORDER BY total_spend DESC;

-- ----------------------------------------------------------------------------
-- 21. Top 10 Lifetime Spenders
-- ----------------------------------------------------------------------------
SELECT 
    customer_unique_id,
    customer_city,
    customer_state,
    customer_order_count,
    ROUND(customer_total_spend, 2) AS total_lifetime_spend
FROM dim_customers
ORDER BY customer_total_spend DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 22. Quarterly Gross Revenue Growth
-- ----------------------------------------------------------------------------
SELECT 
    order_year,
    order_quarter,
    COUNT(DISTINCT o.order_id) AS quarter_orders,
    ROUND(SUM(i.revenue), 2) AS quarter_revenue
FROM fact_orders o
JOIN fact_order_items i ON o.order_id = i.order_id
WHERE o.order_year >= 2017
GROUP BY order_year, order_quarter
ORDER BY order_year, order_quarter;

-- ----------------------------------------------------------------------------
-- 23. Month-over-Month (MoM) Revenue Change
-- ----------------------------------------------------------------------------
WITH monthly_rev AS (
    SELECT 
        o.order_year_month,
        ROUND(SUM(i.revenue), 2) AS revenue
    FROM fact_orders o
    JOIN fact_order_items i ON o.order_id = i.order_id
    WHERE o.order_year_month >= '2017-01'
    GROUP BY o.order_year_month
)
SELECT 
    order_year_month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY order_year_month) AS prev_month_revenue,
    ROUND(100.0 * (revenue - LAG(revenue, 1) OVER (ORDER BY order_year_month)) / LAG(revenue, 1) OVER (ORDER BY order_year_month), 2) AS mom_growth_pct
FROM monthly_rev;

-- ----------------------------------------------------------------------------
-- 24. Year-over-Year (YoY) Revenue Comparison (2017 vs 2018 for Jan-Aug)
-- ----------------------------------------------------------------------------
WITH yoy_base AS (
    SELECT 
        o.order_year,
        o.order_month,
        o.order_month_name,
        ROUND(SUM(i.revenue), 2) AS monthly_rev
    FROM fact_orders o
    JOIN fact_order_items i ON o.order_id = i.order_id
    WHERE o.order_year IN (2017, 2018) AND o.order_month <= 8
    GROUP BY o.order_year, o.order_month, o.order_month_name
)
SELECT 
    y18.order_month,
    y18.order_month_name,
    y17.monthly_rev AS revenue_2017,
    y18.monthly_rev AS revenue_2018,
    ROUND(100.0 * (y18.monthly_rev - y17.monthly_rev) / y17.monthly_rev, 2) AS yoy_growth_pct
FROM yoy_base y18
JOIN yoy_base y17 ON y18.order_month = y17.order_month AND y17.order_year = 2017 AND y18.order_year = 2018
ORDER BY y18.order_month;
