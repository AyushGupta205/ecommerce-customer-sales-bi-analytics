# E-Commerce Data Dictionary

**Project:** E-Commerce Customer, Sales & Business Intelligence Analytics  
**Source:** Brazilian E-Commerce Public Dataset by Olist (Cleaned & Processed)  

---

## 1. Table: `dim_customers` (Cleaned Customers Dimension)

| Column Name | Data Type | Description | Business Meaning | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | VARCHAR(50) | Unique identifier for each order customer key | Links transaction to customer | `06b8999e2fba1a1fbc88172c00ba8bc7` |
| `customer_unique_id` | VARCHAR(50) | Unique identifier for the natural individual | Tracks lifetime customer behavior | `861eff4711a542e4b93843c6dd7febb0` |
| `customer_zip_code_prefix` | INT | First 5 digits of Brazilian zip code (CEP) | Customer postal location | `14409` |
| `customer_city` | VARCHAR(100) | Customer city name | City of purchase | `Franca` |
| `customer_state` | VARCHAR(5) | 2-letter Brazilian state acronym | State of residence | `SP` |
| `customer_order_count` | INT | Lifetime number of orders placed by person | Frequency metric | `1` |
| `customer_total_spend` | DECIMAL(12,2) | Lifetime gross revenue spend | Monetary value (BRL) | `146.87` |
| `customer_value_segment` | VARCHAR(50) | Categorized spend tier | Customer classification | `Medium Value ($100-$500)` |

---

## 2. Table: `dim_products` (Cleaned Products Dimension)

| Column Name | Data Type | Description | Business Meaning | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | VARCHAR(50) | Unique product SKU identifier | Catalog primary key | `1e9e8ef04dbcff4541ed26657ea517e5` |
| `product_category_name` | VARCHAR(100) | Portuguese category name | Raw source category | `perfumaria` |
| `product_category_name_english` | VARCHAR(100) | English translated category name | Business reporting category | `Perfumery` |
| `product_name_lenght` | INT | Character length of product title | Content quality metric | `40` |
| `product_description_lenght` | INT | Character length of product description | Listing detail metric | `287` |
| `product_photos_qty` | INT | Number of photos published on listing | Media asset count | `1` |
| `product_weight_g` | DECIMAL(10,2) | Weight of product in grams | Logistics weight | `225.0` |
| `product_length_cm` | DECIMAL(10,2) | Length of packaged product in cm | Packaging dimension | `16.0` |
| `product_height_cm` | DECIMAL(10,2) | Height of packaged product in cm | Packaging dimension | `10.0` |
| `product_width_cm` | DECIMAL(10,2) | Width of packaged product in cm | Packaging dimension | `14.0` |

---

## 3. Table: `dim_sellers` (Cleaned Sellers Dimension)

| Column Name | Data Type | Description | Business Meaning | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `seller_id` | VARCHAR(50) | Unique seller / merchant identifier | Merchant primary key | `3442f8959a84dea7ee197c632cb2df15` |
| `seller_zip_code_prefix` | INT | First 5 digits of seller zip code | Merchant location | `13023` |
| `seller_city` | VARCHAR(100) | City of merchant warehouse | Origin shipping city | `Campinas` |
| `seller_state` | VARCHAR(5) | 2-letter state acronym of merchant | Origin shipping state | `SP` |

---

## 4. Table: `fact_orders` (Cleaned Orders Fact)

| Column Name | Data Type | Description | Business Meaning | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR(50) | Unique order transaction key | Primary key of order | `e481f51cbdc54678b7cc49136f2d6af7` |
| `customer_id` | VARCHAR(50) | Foreign key to `dim_customers` | Ordering customer | `9ef432eb6251297304e76186b10a928d` |
| `order_status` | VARCHAR(30) | Status (`delivered`, `canceled`, etc.) | Fulfillment state | `delivered` |
| `order_purchase_timestamp` | DATETIME | Timestamp when order was placed | Purchase event time | `2017-10-02 10:56:33` |
| `order_approved_at` | DATETIME | Timestamp of payment approval | Approval time | `2017-10-02 11:07:15` |
| `order_delivered_carrier_date` | DATETIME | Timestamp handed over to logistics carrier | Carrier dispatch | `2017-10-04 19:55:00` |
| `order_delivered_customer_date` | DATETIME | Timestamp parcel reached customer | Final delivery time | `2017-10-10 21:25:13` |
| `order_estimated_delivery_date` | DATETIME | Target promised delivery date | Service commitment date | `2017-10-18 00:00:00` |
| `order_date` | DATE | Date part of purchase timestamp | Date filtering | `2017-10-02` |
| `order_year_month` | VARCHAR(10) | Year and month string | Cohort / Monthly grouping | `2017-10` |
| `delivery_days` | DECIMAL(8,2) | Total days from purchase to delivery | Fulfillment lead time | `8.44` |
| `approval_days` | DECIMAL(8,2) | Days from purchase to payment approval | Payment processing time | `0.01` |
| `estimated_delivery_gap` | DECIMAL(8,2) | Estimated date minus actual delivery date | Delivery buffer (>0 early, <0 late)| `7.11` |
| `is_delayed` | INT | Boolean indicator (1 if delivered after estimate) | Punctuality failure | `0` |
| `customer_type` | VARCHAR(30) | New Customer vs Repeat Customer | Retention segment | `New Customer` |

---

## 5. Table: `fact_order_items` (Cleaned Order Items Fact)

| Column Name | Data Type | Description | Business Meaning | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR(50) | Order foreign key | Parent transaction | `00010242fe8c5941c51a3a24f777922f` |
| `order_item_id` | INT | Sequential item number within order | Line item ordinal | `1` |
| `product_id` | VARCHAR(50) | Product foreign key | Purchased catalog item | `4244733e06e7ecb49c54057ccd6474fb` |
| `seller_id` | VARCHAR(50) | Seller foreign key | Merchant fulfiller | `48436dade18ac8b2bce089ec2a041202` |
| `shipping_limit_date` | DATETIME | Seller dispatch deadline | Seller SLA deadline | `2017-09-19 09:45:35` |
| `price` | DECIMAL(10,2) | Item product price (BRL) | Item merchandise value | `58.90` |
| `freight_value` | DECIMAL(10,2) | Shipping charge for this line item (BRL) | Shipping charge | `13.29` |
| `revenue` | DECIMAL(10,2) | Gross revenue (`price + freight_value`) | Total monetary transaction | `72.19` |

---

## 6. Table: `fact_order_payments` (Cleaned Payments Fact)

| Column Name | Data Type | Description | Business Meaning | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR(50) | Order foreign key | Transaction identifier | `b81ef226f3fe1789b1e8b2acac839d17` |
| `payment_sequential` | INT | Payment sequence index for split payments | Split tender index | `1` |
| `payment_type` | VARCHAR(50) | Payment method (`Credit Card`, `Boleto`, `Voucher`, `Debit Card`) | Tender type | `Credit Card` |
| `payment_installments` | INT | Number of installments selected | Financing term | `8` |
| `payment_value` | DECIMAL(10,2) | Amount paid in this transaction (BRL) | Captured payment | `99.33` |

---

## 7. Table: `fact_order_reviews` (Cleaned Reviews Fact)

| Column Name | Data Type | Description | Business Meaning | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `review_id` | VARCHAR(50) | Unique customer review identifier | Review primary key | `7bc64f5821479f3788b057712eb74d12` |
| `order_id` | VARCHAR(50) | Order foreign key | Evaluated order | `b81ef226f3fe1789b1e8b2acac839d17` |
| `review_score` | INT | Customer satisfaction rating (1 to 5) | CSAT score | `5` |
| `review_comment_title` | TEXT | Review subject title | Subject feedback | `Recomendo` |
| `review_comment_message` | TEXT | Free-form customer feedback message | Qualitative feedback | `Excelente produto, chegou antes do prazo.` |
| `review_creation_date` | DATETIME | Timestamp review survey was sent | Survey creation | `2018-01-20 00:00:00` |
| `review_answer_timestamp` | DATETIME | Timestamp review was completed | Survey response time | `2018-01-22 13:48:18` |

---

## 8. Table: `dim_date` (Time Intelligence Dimension)

| Column Name | Data Type | Description | Business Meaning | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `date_key` | INT | Date key in `YYYYMMDD` format | Primary integer key | `20171002` |
| `date` | DATE | Calendar date | Date filter | `2017-10-02` |
| `year` | INT | Calendar year | Year slicing | `2017` |
| `quarter` | INT | Calendar quarter (1-4) | Quarter slicing | `4` |
| `month_name` | VARCHAR(20) | Full month name | Month slicing | `October` |
| `year_month` | VARCHAR(10) | Year and month string | Timeline trend axis | `2017-10` |
| `day_name` | VARCHAR(20) | Full day of the week | Day-of-week analysis | `Monday` |
| `is_weekend` | INT | Boolean indicator (1 if Sat/Sun) | Weekend shopping | `0` |
