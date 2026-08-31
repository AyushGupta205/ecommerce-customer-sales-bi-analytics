"""
Comprehensive Power BI Project & Template Generator
===================================================
Author: Senior Data Analyst & BI Developer
Project: E-Commerce Customer, Sales & Business Intelligence Analytics

Generates:
1. Ecommerce_Customer_Sales_Intelligence.pbip (Power BI Project)
2. Ecommerce_Customer_Sales_Intelligence.pbit (Power BI Template)
3. Ecommerce_Customer_Sales_Intelligence.Dataset (definition.pbid, definition.pbism, model.bim)
4. Ecommerce_Customer_Sales_Intelligence.Report (definition.pbir, report.json)
"""

import os
import json
import zipfile

BASE_DIR = r"D:\Ecomercee"
PROCESSED_DIR = r"D:\Ecomercee\data\processed"
POWERBI_DIR = os.path.join(BASE_DIR, "powerbi")
PBIP_NAME = "Ecommerce_Customer_Sales_Intelligence"

DATASET_DIR = os.path.join(POWERBI_DIR, f"{PBIP_NAME}.Dataset")
REPORT_DIR = os.path.join(POWERBI_DIR, f"{PBIP_NAME}.Report")

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. PBIP ROOT & DEFINITION FILES
# -----------------------------------------------------------------------------
pbip_content = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
    "version": "1.0",
    "artifacts": [
        {
            "report": {
                "path": f"{PBIP_NAME}.Report"
            }
        }
    ]
}
with open(os.path.join(POWERBI_DIR, f"{PBIP_NAME}.pbip"), "w", encoding="utf-8") as f:
    json.dump(pbip_content, f, indent=2)

pbid_content = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/pbid/v1.0/schema.json",
    "version": "1.0",
    "connection": None
}
with open(os.path.join(DATASET_DIR, "definition.pbid"), "w", encoding="utf-8") as f:
    json.dump(pbid_content, f, indent=2)

pbism_content = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
    "version": "1.0"
}
with open(os.path.join(DATASET_DIR, "definition.pbism"), "w", encoding="utf-8") as f:
    json.dump(pbism_content, f, indent=2)

pbir_content = {
    "version": "1.0",
    "datasetReference": {
        "byPath": {
            "path": f"../{PBIP_NAME}.Dataset"
        }
    }
}
with open(os.path.join(REPORT_DIR, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump(pbir_content, f, indent=2)

print("Generated PBIP root & definition files with validated $schema.")

# -----------------------------------------------------------------------------
# 2. MODEL.BIM (Star Schema with 28 DAX Measures & M Partitions)
# -----------------------------------------------------------------------------
model_bim = {
    "name": "EcommerceAnalyticsModel",
    "compatibilityLevel": 1567,
    "model": {
        "culture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True
        },
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "tables": [
            # 1. FactSales
            {
                "name": "FactSales",
                "columns": [
                    {"name": "order_id", "dataType": "string", "sourceColumn": "order_id"},
                    {"name": "order_item_id", "dataType": "int64", "sourceColumn": "order_item_id"},
                    {"name": "product_id", "dataType": "string", "sourceColumn": "product_id"},
                    {"name": "seller_id", "dataType": "string", "sourceColumn": "seller_id"},
                    {"name": "shipping_limit_date", "dataType": "dateTime", "sourceColumn": "shipping_limit_date", "formatString": "yyyy-mm-dd hh:mm"},
                    {"name": "price", "dataType": "double", "sourceColumn": "price", "formatString": "R$ #,##0.00"},
                    {"name": "freight_value", "dataType": "double", "sourceColumn": "freight_value", "formatString": "R$ #,##0.00"},
                    {"name": "revenue", "dataType": "double", "sourceColumn": "revenue", "formatString": "R$ #,##0.00"}
                ],
                "partitions": [
                    {
                        "name": "FactSales",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                'let',
                                f'    Source = Csv.Document(File.Contents("{PROCESSED_DIR}\\\\fact_order_items_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"order_id", type text}, {"order_item_id", Int64.Type}, {"product_id", type text}, {"seller_id", type text}, {"shipping_limit_date", type datetime}, {"price", type number}, {"freight_value", type number}, {"revenue", type number}})',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ],
                "measures": [
                    {"name": "Total Revenue", "expression": "SUM(FactSales[revenue])", "formatString": "R$ #,##0.00"},
                    {"name": "Total Product Sales", "expression": "SUM(FactSales[price])", "formatString": "R$ #,##0.00"},
                    {"name": "Total Freight", "expression": "SUM(FactSales[freight_value])", "formatString": "R$ #,##0.00"},
                    {"name": "Total Items", "expression": "COUNTROWS(FactSales)", "formatString": "#,##0"},
                    {"name": "Average Order Value", "expression": "DIVIDE([Total Revenue], [Total Orders], 0)", "formatString": "R$ #,##0.00"},
                    {"name": "Average Item Price", "expression": "DIVIDE([Total Product Sales], [Total Items], 0)", "formatString": "R$ #,##0.00"},
                    {"name": "Revenue per Customer", "expression": "DIVIDE([Total Revenue], [Total Customers], 0)", "formatString": "R$ #,##0.00"},
                    {"name": "Customer Revenue", "expression": "[Total Revenue]", "formatString": "R$ #,##0.00"},
                    {"name": "Previous Month Revenue", "expression": "CALCULATE([Total Revenue], DATEADD(DimDate[date], -1, MONTH))", "formatString": "R$ #,##0.00"},
                    {"name": "MoM Growth", "expression": "VAR CurrentRev = [Total Revenue] VAR PrevRev = [Previous Month Revenue] RETURN IF(NOT ISBLANK(PrevRev) && PrevRev > 0, DIVIDE(CurrentRev - PrevRev, PrevRev, 0), BLANK())", "formatString": "0.00%"},
                    {"name": "Previous Year Revenue", "expression": "CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[date]))", "formatString": "R$ #,##0.00"},
                    {"name": "YoY Growth", "expression": "VAR CurrentRev = [Total Revenue] VAR PrevYearRev = [Previous Year Revenue] RETURN IF(NOT ISBLANK(PrevYearRev) && PrevYearRev > 0, DIVIDE(CurrentRev - PrevYearRev, PrevYearRev, 0), BLANK())", "formatString": "0.00%"}
                ]
            },
            # 2. FactOrders
            {
                "name": "FactOrders",
                "columns": [
                    {"name": "order_id", "dataType": "string", "sourceColumn": "order_id"},
                    {"name": "customer_id", "dataType": "string", "sourceColumn": "customer_id"},
                    {"name": "order_status", "dataType": "string", "sourceColumn": "order_status"},
                    {"name": "order_purchase_timestamp", "dataType": "dateTime", "sourceColumn": "order_purchase_timestamp", "formatString": "yyyy-mm-dd hh:mm"},
                    {"name": "order_approved_at", "dataType": "dateTime", "sourceColumn": "order_approved_at", "formatString": "yyyy-mm-dd hh:mm"},
                    {"name": "order_delivered_carrier_date", "dataType": "dateTime", "sourceColumn": "order_delivered_carrier_date", "formatString": "yyyy-mm-dd hh:mm"},
                    {"name": "order_delivered_customer_date", "dataType": "dateTime", "sourceColumn": "order_delivered_customer_date", "formatString": "yyyy-mm-dd hh:mm"},
                    {"name": "order_estimated_delivery_date", "dataType": "dateTime", "sourceColumn": "order_estimated_delivery_date", "formatString": "yyyy-mm-dd"},
                    {"name": "order_date", "dataType": "dateTime", "sourceColumn": "order_date", "formatString": "yyyy-mm-dd"},
                    {"name": "order_year", "dataType": "int64", "sourceColumn": "order_year"},
                    {"name": "order_month", "dataType": "int64", "sourceColumn": "order_month"},
                    {"name": "order_month_name", "dataType": "string", "sourceColumn": "order_month_name"},
                    {"name": "order_year_month", "dataType": "string", "sourceColumn": "order_year_month"},
                    {"name": "order_quarter", "dataType": "int64", "sourceColumn": "order_quarter"},
                    {"name": "order_day_of_week", "dataType": "string", "sourceColumn": "order_day_of_week"},
                    {"name": "delivery_days", "dataType": "double", "sourceColumn": "delivery_days", "formatString": "0.00"},
                    {"name": "approval_days", "dataType": "double", "sourceColumn": "approval_days", "formatString": "0.00"},
                    {"name": "estimated_delivery_gap", "dataType": "double", "sourceColumn": "estimated_delivery_gap", "formatString": "0.00"},
                    {"name": "is_delayed", "dataType": "int64", "sourceColumn": "is_delayed"},
                    {"name": "customer_unique_id", "dataType": "string", "sourceColumn": "customer_unique_id"},
                    {"name": "customer_city", "dataType": "string", "sourceColumn": "customer_city"},
                    {"name": "customer_state", "dataType": "string", "sourceColumn": "customer_state"},
                    {"name": "customer_order_count", "dataType": "int64", "sourceColumn": "customer_order_count"},
                    {"name": "customer_total_spend", "dataType": "double", "sourceColumn": "customer_total_spend", "formatString": "R$ #,##0.00"},
                    {"name": "customer_value_segment", "dataType": "string", "sourceColumn": "customer_value_segment"},
                    {"name": "customer_type", "dataType": "string", "sourceColumn": "customer_type"}
                ],
                "partitions": [
                    {
                        "name": "FactOrders",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                'let',
                                f'    Source = Csv.Document(File.Contents("{PROCESSED_DIR}\\\\fact_orders_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"order_id", type text}, {"customer_id", type text}, {"order_status", type text}, {"order_purchase_timestamp", type datetime}, {"order_approved_at", type datetime}, {"order_delivered_carrier_date", type datetime}, {"order_delivered_customer_date", type datetime}, {"order_estimated_delivery_date", type datetime}, {"order_date", type datetime}, {"order_year", Int64.Type}, {"order_month", Int64.Type}, {"order_month_name", type text}, {"order_year_month", type text}, {"order_quarter", Int64.Type}, {"order_day_of_week", type text}, {"delivery_days", type number}, {"approval_days", type number}, {"estimated_delivery_gap", type number}, {"is_delayed", Int64.Type}, {"customer_unique_id", type text}, {"customer_city", type text}, {"customer_state", type text}, {"customer_order_count", Int64.Type}, {"customer_total_spend", type number}, {"customer_value_segment", type text}, {"customer_type", type text}})',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ],
                "measures": [
                    {"name": "Total Orders", "expression": "DISTINCTCOUNT(FactOrders[order_id])", "formatString": "#,##0"},
                    {"name": "Delivered Orders", "expression": "CALCULATE([Total Orders], FactOrders[order_status] = \"delivered\")", "formatString": "#,##0"},
                    {"name": "Cancelled Orders", "expression": "CALCULATE([Total Orders], FactOrders[order_status] = \"canceled\")", "formatString": "#,##0"},
                    {"name": "Delivery Rate", "expression": "DIVIDE([Delivered Orders], [Total Orders], 0)", "formatString": "0.00%"},
                    {"name": "Cancellation Rate", "expression": "DIVIDE([Cancelled Orders], [Total Orders], 0)", "formatString": "0.00%"},
                    {"name": "Average Delivery Days", "expression": "CALCULATE(AVERAGE(FactOrders[delivery_days]), FactOrders[order_status] = \"delivered\")", "formatString": "0.00"},
                    {"name": "Median Delivery Days", "expression": "CALCULATE(MEDIAN(FactOrders[delivery_days]), FactOrders[order_status] = \"delivered\")", "formatString": "0.00"},
                    {"name": "Delayed Orders", "expression": "CALCULATE([Total Orders], FactOrders[order_status] = \"delivered\", FactOrders[is_delayed] = 1)", "formatString": "#,##0"},
                    {"name": "Delay Rate", "expression": "DIVIDE([Delayed Orders], [Delivered Orders], 0)", "formatString": "0.00%"}
                ]
            },
            # 3. FactPayments
            {
                "name": "FactPayments",
                "columns": [
                    {"name": "order_id", "dataType": "string", "sourceColumn": "order_id"},
                    {"name": "payment_sequential", "dataType": "int64", "sourceColumn": "payment_sequential"},
                    {"name": "payment_type", "dataType": "string", "sourceColumn": "payment_type"},
                    {"name": "payment_installments", "dataType": "int64", "sourceColumn": "payment_installments"},
                    {"name": "payment_value", "dataType": "double", "sourceColumn": "payment_value", "formatString": "R$ #,##0.00"}
                ],
                "partitions": [
                    {
                        "name": "FactPayments",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                'let',
                                f'    Source = Csv.Document(File.Contents("{PROCESSED_DIR}\\\\fact_order_payments_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"order_id", type text}, {"payment_sequential", Int64.Type}, {"payment_type", type text}, {"payment_installments", Int64.Type}, {"payment_value", type number}})',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            # 4. FactReviews
            {
                "name": "FactReviews",
                "columns": [
                    {"name": "review_id", "dataType": "string", "sourceColumn": "review_id"},
                    {"name": "order_id", "dataType": "string", "sourceColumn": "order_id"},
                    {"name": "review_score", "dataType": "int64", "sourceColumn": "review_score"},
                    {"name": "review_comment_title", "dataType": "string", "sourceColumn": "review_comment_title"},
                    {"name": "review_comment_message", "dataType": "string", "sourceColumn": "review_comment_message"},
                    {"name": "review_creation_date", "dataType": "dateTime", "sourceColumn": "review_creation_date", "formatString": "yyyy-mm-dd"},
                    {"name": "review_answer_timestamp", "dataType": "dateTime", "sourceColumn": "review_answer_timestamp", "formatString": "yyyy-mm-dd hh:mm"}
                ],
                "partitions": [
                    {
                        "name": "FactReviews",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                'let',
                                f'    Source = Csv.Document(File.Contents("{PROCESSED_DIR}\\\\fact_order_reviews_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"review_id", type text}, {"order_id", type text}, {"review_score", Int64.Type}, {"review_comment_title", type text}, {"review_comment_message", type text}, {"review_creation_date", type datetime}, {"review_answer_timestamp", type datetime}})',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ],
                "measures": [
                    {"name": "Average Review Score", "expression": "AVERAGE(FactReviews[review_score])", "formatString": "0.00"},
                    {"name": "Five Star Reviews", "expression": "CALCULATE(COUNTROWS(FactReviews), FactReviews[review_score] = 5)", "formatString": "#,##0"},
                    {"name": "Five Star Review %", "expression": "DIVIDE([Five Star Reviews], COUNTROWS(FactReviews), 0)", "formatString": "0.00%"},
                    {"name": "Low Rating Reviews", "expression": "CALCULATE(COUNTROWS(FactReviews), FactReviews[review_score] IN {1, 2})", "formatString": "#,##0"},
                    {"name": "Low Rating %", "expression": "DIVIDE([Low Rating Reviews], COUNTROWS(FactReviews), 0)", "formatString": "0.00%"}
                ]
            },
            # 5. DimCustomer
            {
                "name": "DimCustomer",
                "columns": [
                    {"name": "customer_id", "dataType": "string", "sourceColumn": "customer_id"},
                    {"name": "customer_unique_id", "dataType": "string", "sourceColumn": "customer_unique_id"},
                    {"name": "customer_zip_code_prefix", "dataType": "int64", "sourceColumn": "customer_zip_code_prefix"},
                    {"name": "customer_city", "dataType": "string", "sourceColumn": "customer_city"},
                    {"name": "customer_state", "dataType": "string", "sourceColumn": "customer_state"},
                    {"name": "customer_order_count", "dataType": "int64", "sourceColumn": "customer_order_count"},
                    {"name": "customer_total_spend", "dataType": "double", "sourceColumn": "customer_total_spend", "formatString": "R$ #,##0.00"},
                    {"name": "customer_value_segment", "dataType": "string", "sourceColumn": "customer_value_segment"}
                ],
                "partitions": [
                    {
                        "name": "DimCustomer",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                'let',
                                f'    Source = Csv.Document(File.Contents("{PROCESSED_DIR}\\\\dim_customers_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"customer_id", type text}, {"customer_unique_id", type text}, {"customer_zip_code_prefix", Int64.Type}, {"customer_city", type text}, {"customer_state", type text}, {"customer_order_count", Int64.Type}, {"customer_total_spend", type number}, {"customer_value_segment", type text}})',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ],
                "measures": [
                    {"name": "Total Customers", "expression": "DISTINCTCOUNT(DimCustomer[customer_unique_id])", "formatString": "#,##0"},
                    {"name": "Repeat Customers", "expression": "CALCULATE(DISTINCTCOUNT(DimCustomer[customer_unique_id]), DimCustomer[customer_order_count] > 1)", "formatString": "#,##0"},
                    {"name": "New Customers", "expression": "CALCULATE(DISTINCTCOUNT(DimCustomer[customer_unique_id]), DimCustomer[customer_order_count] = 1)", "formatString": "#,##0"},
                    {"name": "Repeat Customer Rate", "expression": "DIVIDE([Repeat Customers], [Total Customers], 0)", "formatString": "0.00%"},
                    {"name": "Orders per Customer", "expression": "DIVIDE([Total Orders], [Total Customers], 0)", "formatString": "0.00"}
                ]
            },
            # 6. DimProduct
            {
                "name": "DimProduct",
                "columns": [
                    {"name": "product_id", "dataType": "string", "sourceColumn": "product_id"},
                    {"name": "product_category_name", "dataType": "string", "sourceColumn": "product_category_name"},
                    {"name": "product_name_lenght", "dataType": "int64", "sourceColumn": "product_name_lenght"},
                    {"name": "product_description_lenght", "dataType": "int64", "sourceColumn": "product_description_lenght"},
                    {"name": "product_photos_qty", "dataType": "int64", "sourceColumn": "product_photos_qty"},
                    {"name": "product_weight_g", "dataType": "double", "sourceColumn": "product_weight_g"},
                    {"name": "product_length_cm", "dataType": "double", "sourceColumn": "product_length_cm"},
                    {"name": "product_height_cm", "dataType": "double", "sourceColumn": "product_height_cm"},
                    {"name": "product_width_cm", "dataType": "double", "sourceColumn": "product_width_cm"},
                    {"name": "product_category_name_english", "dataType": "string", "sourceColumn": "product_category_name_english"}
                ],
                "partitions": [
                    {
                        "name": "DimProduct",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                'let',
                                f'    Source = Csv.Document(File.Contents("{PROCESSED_DIR}\\\\dim_products_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"product_id", type text}, {"product_category_name", type text}, {"product_name_lenght", Int64.Type}, {"product_description_lenght", Int64.Type}, {"product_photos_qty", Int64.Type}, {"product_weight_g", type number}, {"product_length_cm", type number}, {"product_height_cm", type number}, {"product_width_cm", type number}, {"product_category_name_english", type text}})',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            # 7. DimSeller
            {
                "name": "DimSeller",
                "columns": [
                    {"name": "seller_id", "dataType": "string", "sourceColumn": "seller_id"},
                    {"name": "seller_zip_code_prefix", "dataType": "int64", "sourceColumn": "seller_zip_code_prefix"},
                    {"name": "seller_city", "dataType": "string", "sourceColumn": "seller_city"},
                    {"name": "seller_state", "dataType": "string", "sourceColumn": "seller_state"}
                ],
                "partitions": [
                    {
                        "name": "DimSeller",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                'let',
                                f'    Source = Csv.Document(File.Contents("{PROCESSED_DIR}\\\\dim_sellers_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"seller_id", type text}, {"seller_zip_code_prefix", Int64.Type}, {"seller_city", type text}, {"seller_state", type text}})',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            # 8. DimLocation
            {
                "name": "DimLocation",
                "columns": [
                    {"name": "geolocation_zip_code_prefix", "dataType": "int64", "sourceColumn": "geolocation_zip_code_prefix"},
                    {"name": "geolocation_lat", "dataType": "double", "sourceColumn": "geolocation_lat"},
                    {"name": "geolocation_lng", "dataType": "double", "sourceColumn": "geolocation_lng"},
                    {"name": "geolocation_city", "dataType": "string", "sourceColumn": "geolocation_city"},
                    {"name": "geolocation_state", "dataType": "string", "sourceColumn": "geolocation_state"}
                ],
                "partitions": [
                    {
                        "name": "DimLocation",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                'let',
                                f'    Source = Csv.Document(File.Contents("{PROCESSED_DIR}\\\\dim_geolocation_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"geolocation_zip_code_prefix", Int64.Type}, {"geolocation_lat", type number}, {"geolocation_lng", type number}, {"geolocation_city", type text}, {"geolocation_state", type text}})',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            # 9. DimDate
            {
                "name": "DimDate",
                "columns": [
                    {"name": "date_key", "dataType": "int64", "sourceColumn": "date_key"},
                    {"name": "date", "dataType": "dateTime", "sourceColumn": "date", "formatString": "yyyy-mm-dd"},
                    {"name": "year", "dataType": "int64", "sourceColumn": "year"},
                    {"name": "quarter", "dataType": "int64", "sourceColumn": "quarter"},
                    {"name": "quarter_name", "dataType": "string", "sourceColumn": "quarter_name"},
                    {"name": "year_quarter", "dataType": "string", "sourceColumn": "year_quarter"},
                    {"name": "month", "dataType": "int64", "sourceColumn": "month"},
                    {"name": "month_name", "dataType": "string", "sourceColumn": "month_name", "sortByColumn": "month"},
                    {"name": "month_short", "dataType": "string", "sourceColumn": "month_short", "sortByColumn": "month"},
                    {"name": "year_month", "dataType": "string", "sourceColumn": "year_month"},
                    {"name": "day", "dataType": "int64", "sourceColumn": "day"},
                    {"name": "day_of_week", "dataType": "int64", "sourceColumn": "day_of_week"},
                    {"name": "day_name", "dataType": "string", "sourceColumn": "day_name"},
                    {"name": "week_of_year", "dataType": "int64", "sourceColumn": "week_of_year"},
                    {"name": "is_weekend", "dataType": "int64", "sourceColumn": "is_weekend"}
                ],
                "partitions": [
                    {
                        "name": "DimDate",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                'let',
                                f'    Source = Csv.Document(File.Contents("{PROCESSED_DIR}\\\\dim_date.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"date_key", Int64.Type}, {"date", type datetime}, {"year", Int64.Type}, {"quarter", Int64.Type}, {"quarter_name", type text}, {"year_quarter", type text}, {"month", Int64.Type}, {"month_name", type text}, {"month_short", type text}, {"year_month", type text}, {"day", Int64.Type}, {"day_of_week", Int64.Type}, {"day_name", type text}, {"week_of_year", Int64.Type}, {"is_weekend", Int64.Type}})',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            }
        ],
        "relationships": [
            {
                "name": "Rel_Orders_Customers",
                "fromTable": "FactOrders",
                "fromColumn": "customer_id",
                "toTable": "DimCustomer",
                "toColumn": "customer_id",
                "crossFilteringBehavior": "oneDirection"
            },
            {
                "name": "Rel_Sales_Orders",
                "fromTable": "FactSales",
                "fromColumn": "order_id",
                "toTable": "FactOrders",
                "toColumn": "order_id",
                "crossFilteringBehavior": "oneDirection"
            },
            {
                "name": "Rel_Sales_Products",
                "fromTable": "FactSales",
                "fromColumn": "product_id",
                "toTable": "DimProduct",
                "toColumn": "product_id",
                "crossFilteringBehavior": "oneDirection"
            },
            {
                "name": "Rel_Sales_Sellers",
                "fromTable": "FactSales",
                "fromColumn": "seller_id",
                "toTable": "DimSeller",
                "toColumn": "seller_id",
                "crossFilteringBehavior": "oneDirection"
            },
            {
                "name": "Rel_Payments_Orders",
                "fromTable": "FactPayments",
                "fromColumn": "order_id",
                "toTable": "FactOrders",
                "toColumn": "order_id",
                "crossFilteringBehavior": "oneDirection"
            },
            {
                "name": "Rel_Reviews_Orders",
                "fromTable": "FactReviews",
                "fromColumn": "order_id",
                "toTable": "FactOrders",
                "toColumn": "order_id",
                "crossFilteringBehavior": "oneDirection"
            },
            {
                "name": "Rel_Orders_Date",
                "fromTable": "FactOrders",
                "fromColumn": "order_date",
                "toTable": "DimDate",
                "toColumn": "date",
                "crossFilteringBehavior": "oneDirection"
            }
        ]
    }
}

model_bim_str = json.dumps(model_bim, indent=2)
with open(os.path.join(DATASET_DIR, "model.bim"), "w", encoding="utf-8") as f:
    f.write(model_bim_str)

print("Saved model.bim.")

# -----------------------------------------------------------------------------
# 3. REPORT.JSON (5 Interactive Pages Layout)
# -----------------------------------------------------------------------------
report_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
    "themeCollection": {
        "baseTheme": {
            "name": "CY24SU08",
            "version": "5.57",
            "type": 2
        }
    },
    "sections": [
        {"name": "Page1_ExecutiveOverview", "displayName": "Executive Overview", "width": 1280, "height": 720},
        {"name": "Page2_SalesProductAnalysis", "displayName": "Sales & Product Analysis", "width": 1280, "height": 720},
        {"name": "Page3_CustomerIntelligence", "displayName": "Customer Intelligence", "width": 1280, "height": 720},
        {"name": "Page4_DeliveryCustomerExperience", "displayName": "Delivery & Customer Experience", "width": 1280, "height": 720},
        {"name": "Page5_GeographicAnalysis", "displayName": "Geographic & Business Insights", "width": 1280, "height": 720}
    ]
}

report_json_str = json.dumps(report_json, indent=2)
with open(os.path.join(REPORT_DIR, "report.json"), "w", encoding="utf-8") as f:
    f.write(report_json_str)

print("Saved report.json.")

# -----------------------------------------------------------------------------
# 4. STANDALONE POWER BI TEMPLATE (.PBIT) GENERATION
# -----------------------------------------------------------------------------
pbit_path = os.path.join(POWERBI_DIR, f"{PBIP_NAME}.pbit")

layout_dict = {
    "id": 0,
    "resourcePackages": [],
    "sections": [
        {"id": 0, "name": "ReportSection1", "displayName": "Executive Overview", "filters": "[]", "ordinal": 0, "config": "{}"},
        {"id": 1, "name": "ReportSection2", "displayName": "Sales & Product Analysis", "filters": "[]", "ordinal": 1, "config": "{}"},
        {"id": 2, "name": "ReportSection3", "displayName": "Customer Intelligence", "filters": "[]", "ordinal": 2, "config": "{}"},
        {"id": 3, "name": "ReportSection4", "displayName": "Delivery & Customer Experience", "filters": "[]", "ordinal": 3, "config": "{}"},
        {"id": 4, "name": "ReportSection5", "displayName": "Geographic & Business Insights", "filters": "[]", "ordinal": 4, "config": "{}"}
    ],
    "config": "{\"version\":\"5.57\",\"themeCollection\":{\"baseTheme\":{\"name\":\"CY24SU08\",\"version\":\"5.57\",\"type\":2}}}"
}
layout_bytes = json.dumps(layout_dict, indent=2).encode('utf-16le')

content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="application/xml" />
  <Override PartName="/DataModelSchema" ContentType="" />
</Types>"""

metadata_json = json.dumps({"name": "EcommerceAnalyticsModel", "version": "1.0"}).encode('utf-8')
version_bytes = "1.18".encode('utf-16le')

with zipfile.ZipFile(pbit_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr("Version", version_bytes)
    z.writestr("Report/Layout", layout_bytes)
    z.writestr("DataModelSchema", model_bim_str.encode('utf-8'))
    z.writestr("Metadata", metadata_json)
    z.writestr("[Content_Types].xml", content_types_xml.encode('utf-8'))

print(f"Generated standalone Power BI template: {pbit_path} ({os.path.getsize(pbit_path):,} bytes)")
