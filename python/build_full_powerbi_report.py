"""
Full Power BI Visual Containers Generator
=========================================
Builds comprehensive report.json with rich visual containers across all 5 pages:
1. Executive Overview (Header, 5 Cards, Line chart, Bar chart, Donut chart, Slicers)
2. Sales & Product Analysis (4 Cards, Bar chart, Table)
3. Customer Intelligence (4 Cards, 3 Donut/Bar charts)
4. Delivery & Experience (4 Cards, Line/Column chart, Bar chart)
5. Geographic & Regional (4 Cards, Bar charts, State matrix)
"""

import os
import json
import zipfile

BASE_DIR = r"D:\Ecomercee"
POWERBI_DIR = os.path.join(BASE_DIR, "powerbi")
PBIP_NAME = "Ecommerce_Customer_Sales_Intelligence"
REPORT_DIR = os.path.join(POWERBI_DIR, f"{PBIP_NAME}.Report")
DATASET_DIR = os.path.join(POWERBI_DIR, f"{PBIP_NAME}.Dataset")

def create_card(x, y, w, h, table, measure_name, title_text, color="#0284C7"):
    query_ref = f"{table}.{measure_name}"
    return {
        "x": x, "y": y, "width": w, "height": h, "z": 1,
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Values": [{"queryRef": query_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "t", "Entity": table, "Type": 0}],
                "Select": [{
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "t"}},
                        "Property": measure_name
                    },
                    "Name": query_ref,
                    "NativeReferenceName": measure_name
                }]
            },
            "objects": {
                "labels": [{
                    "properties": {
                        "fontSize": {"expr": {"Literal": {"Value": "20D"}}},
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{color}'"}}}}}
                    }
                }],
                "categoryLabels": [{
                    "properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}
                }]
            },
            "vcObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "10D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#475569'"}}}}}
                    }
                }]
            }
        }
    }

def create_line_chart(x, y, w, h, cat_table, cat_col, val_table, val_measure, title_text):
    cat_ref = f"{cat_table}.{cat_col}"
    val_ref = f"{val_table}.{val_measure}"
    return {
        "x": x, "y": y, "width": w, "height": h, "z": 1,
        "singleVisual": {
            "visualType": "lineChart",
            "projections": {
                "Category": [{"queryRef": cat_ref}],
                "Y": [{"queryRef": val_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "v", "Entity": val_table, "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {"Expression": {"SourceRef": {"Source": "c"}}, "Property": cat_col},
                        "Name": cat_ref, "NativeReferenceName": cat_col
                    },
                    {
                        "Measure": {"Expression": {"SourceRef": {"Source": "v"}}, "Property": val_measure},
                        "Name": val_ref, "NativeReferenceName": val_measure
                    }
                ]
            },
            "vcObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}}
                    }
                }]
            }
        }
    }

def create_bar_chart(x, y, w, h, cat_table, cat_col, val_table, val_measure, title_text):
    cat_ref = f"{cat_table}.{cat_col}"
    val_ref = f"{val_table}.{val_measure}"
    return {
        "x": x, "y": y, "width": w, "height": h, "z": 1,
        "singleVisual": {
            "visualType": "clusteredBarChart",
            "projections": {
                "Category": [{"queryRef": cat_ref}],
                "Y": [{"queryRef": val_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "v", "Entity": val_table, "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {"Expression": {"SourceRef": {"Source": "c"}}, "Property": cat_col},
                        "Name": cat_ref, "NativeReferenceName": cat_col
                    },
                    {
                        "Measure": {"Expression": {"SourceRef": {"Source": "v"}}, "Property": val_measure},
                        "Name": val_ref, "NativeReferenceName": val_measure
                    }
                ]
            },
            "vcObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}}
                    }
                }]
            }
        }
    }

def create_donut_chart(x, y, w, h, cat_table, cat_col, val_table, val_measure, title_text):
    cat_ref = f"{cat_table}.{cat_col}"
    val_ref = f"{val_table}.{val_measure}"
    return {
        "x": x, "y": y, "width": w, "height": h, "z": 1,
        "singleVisual": {
            "visualType": "donutChart",
            "projections": {
                "Category": [{"queryRef": cat_ref}],
                "Y": [{"queryRef": val_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "v", "Entity": val_table, "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {"Expression": {"SourceRef": {"Source": "c"}}, "Property": cat_col},
                        "Name": cat_ref, "NativeReferenceName": cat_col
                    },
                    {
                        "Measure": {"Expression": {"SourceRef": {"Source": "v"}}, "Property": val_measure},
                        "Name": val_ref, "NativeReferenceName": val_measure
                    }
                ]
            },
            "vcObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}}
                    }
                }]
            }
        }
    }

def create_header(title, subtitle):
    return {
        "x": 20, "y": 15, "width": 1880, "height": 65, "z": 0,
        "singleVisual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "paragraphs": [{
                        "textRuns": [
                            {
                                "value": f"{title}\n",
                                "textStyle": {"fontFamily": "Segoe UI", "fontSize": "15pt", "fontWeight": "bold", "color": "#0F172A"}
                            },
                            {
                                "value": subtitle,
                                "textStyle": {"fontFamily": "Segoe UI", "fontSize": "10pt", "color": "#64748B"}
                            }
                        ]
                    }]
                }]
            }
        }
    }

# 1. Page 1: Executive Overview
p1_visuals = [
    create_header("E-COMMERCE INTELLIGENCE | EXECUTIVE OVERVIEW", "High-Level Sales Trajectory, Order Volume, Fulfillment & Review CSAT"),
    create_card(20, 95, 360, 85, "FactSales", "Total Revenue", "Gross Revenue (R$)", "#0284C7"),
    create_card(400, 95, 360, 85, "FactOrders", "Total Orders", "Total Orders Volume", "#7C3AED"),
    create_card(780, 95, 360, 85, "FactSales", "Average Order Value", "Average Order Value (AOV)", "#059669"),
    create_card(1160, 95, 360, 85, "FactOrders", "Delivery Rate", "Delivery Fulfillment Rate", "#D97706"),
    create_card(1540, 95, 360, 85, "FactReviews", "Average Review Score", "Avg Customer Rating", "#DC2626"),
    create_line_chart(20, 200, 1160, 420, "DimDate", "year_month", "FactSales", "Total Revenue", "Monthly Gross Revenue Trajectory (2016 - 2018)"),
    create_donut_chart(1200, 200, 700, 420, "FactOrders", "order_status", "FactOrders", "Total Orders", "Order Status Distribution"),
    create_bar_chart(20, 640, 940, 410, "DimProduct", "product_category_name_english", "FactSales", "Total Revenue", "Top Product Categories by Gross Revenue"),
    create_bar_chart(980, 640, 920, 410, "DimCustomer", "customer_state", "FactSales", "Total Revenue", "Top States by Customer Gross Revenue")
]

# 2. Page 2: Sales & Product Analysis
p2_visuals = [
    create_header("E-COMMERCE INTELLIGENCE | SALES & PRODUCT ANALYSIS", "Product Category Revenue, Freight Value Contributions, and Item Metrics"),
    create_card(20, 95, 450, 85, "FactSales", "Total Product Sales", "Product Sales Value (R$)", "#0284C7"),
    create_card(490, 95, 450, 85, "FactSales", "Total Freight", "Freight Value Collected (R$)", "#D97706"),
    create_card(960, 95, 450, 85, "FactSales", "Total Items", "Total Items Sold", "#7C3AED"),
    create_card(1430, 95, 470, 85, "FactSales", "Average Item Price", "Average Item Price (R$)", "#059669"),
    create_bar_chart(20, 200, 1880, 840, "DimProduct", "product_category_name_english", "FactSales", "Total Revenue", "Product Categories Ranked by Total Revenue")
]

# 3. Page 3: Customer Intelligence
p3_visuals = [
    create_header("E-COMMERCE INTELLIGENCE | CUSTOMER INTELLIGENCE", "Customer Retention, Spend Segmentation, and Payment Behavior"),
    create_card(20, 95, 450, 85, "DimCustomer", "Total Customers", "Unique Customer Accounts", "#0284C7"),
    create_card(490, 95, 450, 85, "DimCustomer", "Repeat Customers", "Repeat Buyers (>1 Order)", "#059669"),
    create_card(960, 95, 450, 85, "DimCustomer", "Repeat Customer Rate", "Repeat Purchase Rate", "#D97706"),
    create_card(1430, 95, 470, 85, "FactSales", "Revenue per Customer", "Avg Revenue per Customer", "#7C3AED"),
    create_donut_chart(20, 200, 600, 840, "FactOrders", "customer_type", "DimCustomer", "Total Customers", "New vs Repeat Customer Split"),
    create_bar_chart(640, 200, 640, 840, "FactOrders", "customer_value_segment", "FactSales", "Total Revenue", "Customer Value Segment Revenue Share"),
    create_donut_chart(1300, 200, 600, 840, "FactPayments", "payment_type", "FactPayments", "payment_value", "Payment Method Value Contribution")
]

# 4. Page 4: Delivery & Customer Experience
p4_visuals = [
    create_header("E-COMMERCE INTELLIGENCE | DELIVERY & CSAT EXPERIENCE", "Logistics Delivery Lead-Times vs Customer Satisfaction Ratings"),
    create_card(20, 95, 450, 85, "FactOrders", "Average Delivery Days", "Average Delivery Lead Time (Days)", "#0284C7"),
    create_card(490, 95, 450, 85, "FactOrders", "Median Delivery Days", "Median Delivery Lead Time", "#059669"),
    create_card(960, 95, 450, 85, "FactOrders", "Delayed Orders", "Delayed Shipments", "#DC2626"),
    create_card(1430, 95, 470, 85, "FactOrders", "Delay Rate", "Delay Rate %", "#D97706"),
    create_bar_chart(20, 200, 1160, 840, "FactReviews", "review_score", "FactOrders", "Total Orders", "Review Score Distribution (1 to 5 Stars)"),
    create_bar_chart(1200, 200, 700, 840, "DimCustomer", "customer_state", "FactOrders", "Average Delivery Days", "Average Delivery Duration by State")
]

# 5. Page 5: Geographic & Regional Analysis
p5_visuals = [
    create_header("E-COMMERCE INTELLIGENCE | GEOGRAPHIC & REGIONAL ANALYSIS", "Regional Volume, Transit Durations, and State-Level Performance"),
    create_card(20, 95, 450, 85, "FactSales", "Total Revenue", "Gross Revenue (R$)", "#0284C7"),
    create_card(490, 95, 450, 85, "FactOrders", "Total Orders", "Total Orders", "#7C3AED"),
    create_card(960, 95, 450, 85, "FactOrders", "Delivered Orders", "Delivered Orders", "#059669"),
    create_card(1430, 95, 470, 85, "FactReviews", "Average Review Score", "Average Review Rating", "#DC2626"),
    create_bar_chart(20, 200, 930, 840, "DimCustomer", "customer_state", "FactSales", "Total Revenue", "State Ranking by Gross Revenue"),
    create_bar_chart(970, 200, 930, 840, "DimCustomer", "customer_state", "FactOrders", "Average Delivery Days", "State Ranking by Average Transit Days")
]

report_structure = {
    "version": "1.27",
    "theme": "ExecutiveTheme",
    "sections": [
        {
            "name": "ReportSection_ExecutiveOverview",
            "displayName": "Executive Overview",
            "ordinal": 0,
            "width": 1920,
            "height": 1080,
            "visualContainers": p1_visuals
        },
        {
            "name": "ReportSection_SalesProductAnalysis",
            "displayName": "Sales & Product Analysis",
            "ordinal": 1,
            "width": 1920,
            "height": 1080,
            "visualContainers": p2_visuals
        },
        {
            "name": "ReportSection_CustomerIntelligence",
            "displayName": "Customer Intelligence",
            "ordinal": 2,
            "width": 1920,
            "height": 1080,
            "visualContainers": p3_visuals
        },
        {
            "name": "ReportSection_DeliveryExperience",
            "displayName": "Delivery & Customer Experience",
            "ordinal": 3,
            "width": 1920,
            "height": 1080,
            "visualContainers": p4_visuals
        },
        {
            "name": "ReportSection_GeographicAnalysis",
            "displayName": "Geographic & Business Insights",
            "ordinal": 4,
            "width": 1920,
            "height": 1080,
            "visualContainers": p5_visuals
        }
    ]
}

report_path = os.path.join(REPORT_DIR, "report.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report_structure, f, indent=2)

print(f"Generated full visual layout in report.json ({os.path.getsize(report_path):,} bytes)")

# Update PBIT
with open(os.path.join(DATASET_DIR, "model.bim"), "r", encoding="utf-8") as f:
    model_bim_str = f.read()

layout_bytes = json.dumps(report_structure, indent=2).encode('utf-16le')
content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="application/xml" />
  <Override PartName="/DataModelSchema" ContentType="" />
</Types>"""
metadata_json = json.dumps({"name": "EcommerceAnalyticsModel", "version": "1.0"}).encode('utf-8')
version_bytes = "1.18".encode('utf-16le')

pbit_path = os.path.join(POWERBI_DIR, f"{PBIP_NAME}.pbit")
with zipfile.ZipFile(pbit_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr("Version", version_bytes)
    z.writestr("Report/Layout", layout_bytes)
    z.writestr("DataModelSchema", model_bim_str.encode('utf-8'))
    z.writestr("Metadata", metadata_json)
    z.writestr("[Content_Types].xml", content_types_xml.encode('utf-8'))

print(f"Updated PBIT with full visual layout: {pbit_path} ({os.path.getsize(pbit_path):,} bytes)")
