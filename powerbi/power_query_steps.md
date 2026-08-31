# Power Query (M) ETL Transformations Specification

**Project:** E-Commerce Customer, Sales & Business Intelligence Analytics  
**Engine:** Power Query (M Language)  

---

## 1. Global Parameters & Ingestion Architecture

In Power BI Desktop, set a parameter `SourcePath` pointing to the folder containing processed datasets:
```powerquery
SourcePath = "D:\Ecomercee\data\processed\" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

---

## 2. Power Query M-Code Recipes

### 2.1 FactSales (`fact_order_items_clean.csv`)
```powerquery
let
    Source = Csv.Document(File.Contents(SourcePath & "fact_order_items_clean.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"order_id", type text},
        {"order_item_id", Int64.Type},
        {"product_id", type text},
        {"seller_id", type text},
        {"shipping_limit_date", type datetime},
        {"price", type number},
        {"freight_value", type number},
        {"revenue", type number}
    })
in
    #"Changed Type"
```

### 2.2 FactOrders (`fact_orders_clean.csv`)
```powerquery
let
    Source = Csv.Document(File.Contents(SourcePath & "fact_orders_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"order_id", type text},
        {"customer_id", type text},
        {"order_status", type text},
        {"order_purchase_timestamp", type datetime},
        {"order_approved_at", type datetime},
        {"order_delivered_carrier_date", type datetime},
        {"order_delivered_customer_date", type datetime},
        {"order_estimated_delivery_date", type datetime},
        {"order_date", type date},
        {"order_year", Int64.Type},
        {"order_month", Int64.Type},
        {"order_month_name", type text},
        {"order_year_month", type text},
        {"order_quarter", Int64.Type},
        {"order_day_of_week", type text},
        {"delivery_days", type number},
        {"approval_days", type number},
        {"estimated_delivery_gap", type number},
        {"is_delayed", Int64.Type},
        {"customer_unique_id", type text},
        {"customer_city", type text},
        {"customer_state", type text},
        {"customer_order_count", Int64.Type},
        {"customer_total_spend", type number},
        {"customer_value_segment", type text},
        {"customer_type", type text}
    })
in
    #"Changed Type"
```

### 2.3 DimProduct (`dim_products_clean.csv`)
```powerquery
let
    Source = Csv.Document(File.Contents(SourcePath & "dim_products_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"product_id", type text},
        {"product_category_name", type text},
        {"product_name_lenght", Int64.Type},
        {"product_description_lenght", Int64.Type},
        {"product_photos_qty", Int64.Type},
        {"product_weight_g", type number},
        {"product_length_cm", type number},
        {"product_height_cm", type number},
        {"product_width_cm", type number},
        {"product_category_name_english", type text}
    })
in
    #"Changed Type"
```

### 2.4 DimCustomer (`dim_customers_clean.csv`)
```powerquery
let
    Source = Csv.Document(File.Contents(SourcePath & "dim_customers_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"customer_id", type text},
        {"customer_unique_id", type text},
        {"customer_zip_code_prefix", Int64.Type},
        {"customer_city", type text},
        {"customer_state", type text},
        {"customer_order_count", Int64.Type},
        {"customer_total_spend", type number},
        {"customer_value_segment", type text}
    })
in
    #"Changed Type"
```

### 2.5 DimDate (`dim_date.csv`)
```powerquery
let
    Source = Csv.Document(File.Contents(SourcePath & "dim_date.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"date_key", Int64.Type},
        {"date", type date},
        {"year", Int64.Type},
        {"quarter", Int64.Type},
        {"quarter_name", type text},
        {"year_quarter", type text},
        {"month", Int64.Type},
        {"month_name", type text},
        {"month_short", type text},
        {"year_month", type text},
        {"day", Int64.Type},
        {"day_of_week", Int64.Type},
        {"day_name", type text},
        {"week_of_year", Int64.Type},
        {"is_weekend", Int64.Type}
    })
in
    #"Changed Type"
```
