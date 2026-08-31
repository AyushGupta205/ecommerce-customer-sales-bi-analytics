-- ============================================================================
-- 05_advanced_analysis.sql
-- Project: E-Commerce Customer, Sales & Business Intelligence Analytics
-- Author: Senior Data Analyst & BI Developer
-- Purpose: Advanced Analytical SQL (CTEs, Window Functions, RFM, Cohorts, Pareto)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Cumulative Running Revenue & 3-Month Moving Average
-- ----------------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        o.order_year_month,
        COUNT(DISTINCT o.order_id) AS monthly_orders,
        ROUND(SUM(i.revenue), 2) AS monthly_revenue
    FROM fact_orders o
    JOIN fact_order_items i ON o.order_id = i.order_id
    WHERE o.order_year_month >= '2017-01'
    GROUP BY o.order_year_month
)
SELECT 
    order_year_month,
    monthly_revenue,
    SUM(monthly_revenue) OVER (ORDER BY order_year_month) AS cumulative_running_revenue,
    ROUND(AVG(monthly_revenue) OVER (ORDER BY order_year_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m_revenue
FROM monthly_metrics
ORDER BY order_year_month;

-- ----------------------------------------------------------------------------
-- 2. Pareto Analysis (80/20 Rule): Category Cumulative Revenue Contribution
-- ----------------------------------------------------------------------------
WITH category_revenue AS (
    SELECT 
        p.product_category_name_english AS category,
        ROUND(SUM(i.revenue), 2) AS category_revenue
    FROM fact_order_items i
    JOIN dim_products p ON i.product_id = p.product_id
    GROUP BY p.product_category_name_english
),
ranked_categories AS (
    SELECT 
        category,
        category_revenue,
        SUM(category_revenue) OVER (ORDER BY category_revenue DESC) AS running_category_revenue,
        SUM(category_revenue) OVER () AS total_overall_revenue
    FROM category_revenue
)
SELECT 
    category,
    category_revenue,
    running_category_revenue,
    ROUND(100.0 * running_category_revenue / total_overall_revenue, 2) AS cumulative_revenue_pct,
    CASE 
        WHEN 100.0 * running_category_revenue / total_overall_revenue <= 80.0 THEN 'Core 80% Contributor'
        ELSE 'Long Tail 20% Contributor'
    END AS pareto_classification
FROM ranked_categories
ORDER BY category_revenue DESC;

-- ----------------------------------------------------------------------------
-- 3. RFM (Recency, Frequency, Monetary) Customer Segmentation via NTILE
-- ----------------------------------------------------------------------------
WITH rfm_base AS (
    SELECT 
        c.customer_unique_id,
        MAX(o.order_purchase_timestamp) AS last_purchase,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(i.revenue) AS monetary_value
    FROM dim_customers c
    JOIN fact_orders o ON c.customer_id = o.customer_id
    JOIN fact_order_items i ON o.order_id = i.order_id
    GROUP BY c.customer_unique_id
),
rfm_scores AS (
    SELECT 
        customer_unique_id,
        last_purchase,
        frequency,
        monetary_value,
        NTILE(5) OVER (ORDER BY last_purchase ASC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM rfm_base
)
SELECT 
    customer_unique_id,
    ROUND(monetary_value, 2) AS monetary_value,
    frequency,
    r_score,
    f_score,
    m_score,
    (r_score * 100 + f_score * 10 + m_score) AS rfm_combined_score,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions / VIP'
        WHEN r_score >= 3 AND m_score >= 3 THEN 'Loyal / High Potential'
        WHEN r_score <= 2 AND m_score >= 4 THEN 'At Risk High Value'
        ELSE 'Standard / Hibernating'
    END AS rfm_segment
FROM rfm_scores
ORDER BY monetary_value DESC
LIMIT 50;

-- ----------------------------------------------------------------------------
-- 4. Seller Performance & Revenue Concentration (Top Sellers DENSE_RANK)
-- ----------------------------------------------------------------------------
WITH seller_metrics AS (
    SELECT 
        s.seller_id,
        s.seller_city,
        s.seller_state,
        COUNT(DISTINCT i.order_id) AS total_orders_fulfilled,
        COUNT(i.order_item_id) AS total_items_sold,
        ROUND(SUM(i.revenue), 2) AS seller_gross_revenue
    FROM dim_sellers s
    JOIN fact_order_items i ON s.seller_id = i.seller_id
    GROUP BY s.seller_id, s.seller_city, s.seller_state
)
SELECT 
    seller_id,
    seller_city,
    seller_state,
    total_orders_fulfilled,
    total_items_sold,
    seller_gross_revenue,
    DENSE_RANK() OVER (ORDER BY seller_gross_revenue DESC) AS seller_revenue_rank,
    ROUND(100.0 * seller_gross_revenue / SUM(seller_gross_revenue) OVER (), 3) AS seller_revenue_share_pct
FROM seller_metrics
ORDER BY seller_gross_revenue DESC
LIMIT 25;

-- ----------------------------------------------------------------------------
-- 5. Customer Monthly Cohort Retention Matrix
-- ----------------------------------------------------------------------------
WITH customer_first_cohort AS (
    SELECT 
        c.customer_unique_id,
        MIN(strftime('%Y-%m', o.order_purchase_timestamp)) AS cohort_month
    FROM dim_customers c
    JOIN fact_orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
),
customer_orders_month AS (
    SELECT 
        c.customer_unique_id,
        strftime('%Y-%m', o.order_purchase_timestamp) AS order_month
    FROM dim_customers c
    JOIN fact_orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id, strftime('%Y-%m', o.order_purchase_timestamp)
)
SELECT 
    fc.cohort_month,
    COUNT(DISTINCT fc.customer_unique_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN om.order_month = fc.cohort_month THEN fc.customer_unique_id END) AS month_0_active,
    COUNT(DISTINCT CASE WHEN om.order_month > fc.cohort_month THEN fc.customer_unique_id END) AS subsequent_active_customers,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN om.order_month > fc.cohort_month THEN fc.customer_unique_id END) / COUNT(DISTINCT fc.customer_unique_id), 2) AS retention_rate_pct
FROM customer_first_cohort fc
LEFT JOIN customer_orders_month om ON fc.customer_unique_id = om.customer_unique_id
WHERE fc.cohort_month >= '2017-01' AND fc.cohort_month <= '2018-03'
GROUP BY fc.cohort_month
ORDER BY fc.cohort_month;
