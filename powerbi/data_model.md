# Power BI Data Model Specification (Star Schema)

**Project:** E-Commerce Customer, Sales & Business Intelligence Analytics  
**Architecture:** Enterprise Dimensional Model (Star Schema)  
**Storage Mode:** Dual / Import Mode  

---

## 1. Schema Architecture Overview

The Power BI data model is organized into a clean **Star Schema** with separated Fact tables (containing transactional events and numeric metrics) and Dimension tables (containing contextual attributes, descriptions, and hierarchy).

```
                      ┌──────────────────┐
                      │     DimDate      │
                      │  (Date Dimension)│
                      └────────┬─────────┘
                               │ 1:N
 ┌─────────────────┐           ▼           ┌──────────────────┐
 │   DimCustomer   │────┐  ┌───────────┐  ┌┤    DimProduct    │
 │ (Customer Dim)  │ 1:N│  │ FactSales │  ││  (Product Dim)   │
 └─────────────────┘    │  │(Line Items│  │└──────────────────┘
                        ▼  │ & Revenue)│  ▼ 1:N
 ┌─────────────────┐  ┌────┴───────────┴────┐ ┌──────────────────┐
 │    DimSeller    │  │                     │ │   DimLocation    │
 │  (Seller Dim)   ├─►│    FactPayments     │ │  (Zip Geo Dim)   │
 └─────────────────┘  │                     │ └──────────────────┘
                 1:N  │     FactReviews     │
                      └─────────────────────┘
```

---

## 2. Table Specifications

### 2.1 Fact Tables

| Table Name | Source File / Table | Primary / Composite Key | Grain | Key Metrics |
| :--- | :--- | :--- | :--- | :--- |
| **`FactSales`** | `fact_order_items_clean.csv` | `(order_id, order_item_id)` | 1 row per ordered product line item | `price`, `freight_value`, `revenue` |
| **`FactOrders`** | `fact_orders_clean.csv` | `order_id` | 1 row per placed commercial order | `delivery_days`, `approval_days`, `delay_days` |
| **`FactPayments`** | `fact_order_payments_clean.csv`| `(order_id, payment_sequential)`| 1 row per payment transaction | `payment_value`, `payment_installments` |
| **`FactReviews`** | `fact_order_reviews_clean.csv` | `(review_id, order_id)` | 1 row per customer review evaluation | `review_score` (1-5) |

### 2.2 Dimension Tables

| Table Name | Source File / Table | Primary Key | Grain | Key Attributes |
| :--- | :--- | :--- | :--- | :--- |
| **`DimCustomer`** | `dim_customers_clean.csv` | `customer_id` | 1 row per order customer transaction | `customer_unique_id`, `customer_city`, `customer_state`, `customer_value_segment`, `customer_order_count`, `customer_total_spend` |
| **`DimProduct`** | `dim_products_clean.csv` | `product_id` | 1 row per unique catalog product | `product_category_name_english`, `product_weight_g`, `product_photos_qty`, `product_length_cm` |
| **`DimSeller`** | `dim_sellers_clean.csv` | `seller_id` | 1 row per registered merchant seller | `seller_city`, `seller_state`, `seller_zip_code_prefix` |
| **`DimDate`** | `dim_date.csv` | `date` / `date_key` | 1 row per calendar day (2016–2018) | `year`, `quarter`, `month_name`, `year_month`, `day_name`, `is_weekend` |
| **`DimLocation`** | `dim_geolocation_clean.csv`| `geolocation_zip_code_prefix`| 1 row per aggregated Brazilian zip code | `geolocation_lat`, `geolocation_lng`, `geolocation_city`, `geolocation_state` |

---

## 3. Relationships & Cardinality Matrix

| From Table (Dimension) | From Column | To Table (Fact) | To Column | Cardinality | Cross-Filter Direction | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `DimCustomer` | `customer_id` | `FactSales` (via `FactOrders`) | `customer_id` | 1 : Many (1:*) | Single (`DimCustomer` filters Fact) | Avoids ambiguity; standard star schema |
| `DimProduct` | `product_id` | `FactSales` | `product_id` | 1 : Many (1:*) | Single (`DimProduct` filters `FactSales`) | Clean product hierarchy drill-down |
| `DimSeller` | `seller_id` | `FactSales` | `seller_id` | 1 : Many (1:*) | Single (`DimSeller` filters `FactSales`) | Merchant performance slicing |
| `DimDate` | `date` | `FactSales` (via `FactOrders`) | `order_purchase_timestamp` | 1 : Many (1:*) | Single (`DimDate` filters Facts) | Enables DAX Time Intelligence (`SAMEPERIODLASTYEAR`, `DATEADD`) |
| `FactSales` | `order_id` | `FactPayments` | `order_id` | 1 : Many (1:*) | Single (`FactSales` filters `FactPayments`) | Payment method breakdown by order |
| `FactSales` | `order_id` | `FactReviews` | `order_id` | 1 : Many (1:*) | Single (`FactSales` filters `FactReviews`) | Review score breakdown by order |

---

## 4. Modeling Best Practices Implemented

1. **Strict 1-to-Many Relationships**: No bi-directional or Many-to-Many relationships to eliminate non-deterministic filter propagation.
2. **Dedicated Measure Table**: All DAX measures are centralized in a dedicated calculation group/table named `_Measures`.
3. **Hidden Surrogate & Foreign Keys**: Foreign keys in Fact tables (`customer_id`, `product_id`, `seller_id`) are hidden from report view to force report builders to use clean Dimension attributes.
4. **Marked as Date Table**: `DimDate` is designated as the official Date Table in Power BI Desktop to guarantee accurate time intelligence calculations.
