"""
Clean PBIP Project Generator
============================
Restores report.json and definition files to the clean, valid Fabric PBIP schema.
"""

import os
import json

BASE_DIR = r"D:\Ecomercee"
POWERBI_DIR = os.path.join(BASE_DIR, "powerbi")
PBIP_NAME = "Ecommerce_Customer_Sales_Intelligence"
DATASET_DIR = os.path.join(POWERBI_DIR, f"{PBIP_NAME}.Dataset")
REPORT_DIR = os.path.join(POWERBI_DIR, f"{PBIP_NAME}.Report")

# 1. PBIP Root
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

# 2. Dataset definition.pbid & definition.pbism
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

# 3. Report definition.pbir & report.json
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
        {
            "name": "Page1_ExecutiveOverview",
            "displayName": "Executive Overview",
            "width": 1280,
            "height": 720,
            "visualContainers": []
        },
        {
            "name": "Page2_SalesProductAnalysis",
            "displayName": "Sales & Product Analysis",
            "width": 1280,
            "height": 720,
            "visualContainers": []
        },
        {
            "name": "Page3_CustomerIntelligence",
            "displayName": "Customer Intelligence",
            "width": 1280,
            "height": 720,
            "visualContainers": []
        },
        {
            "name": "Page4_DeliveryCustomerExperience",
            "displayName": "Delivery & Customer Experience",
            "width": 1280,
            "height": 720,
            "visualContainers": []
        },
        {
            "name": "Page5_GeographicAnalysis",
            "displayName": "Geographic & Business Insights",
            "width": 1280,
            "height": 720,
            "visualContainers": []
        }
    ]
}

with open(os.path.join(REPORT_DIR, "report.json"), "w", encoding="utf-8") as f:
    json.dump(report_json, f, indent=2)

print("Restored clean Fabric PBIP schema and report.json.")
