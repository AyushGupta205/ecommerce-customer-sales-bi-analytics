# Complete End-to-End E-Commerce Data Analytics Project Report

**Project Title:** E-Commerce Customer, Sales & Business Intelligence Analytics  
**Portfolio Target:** Final-Year B.Tech CSE Placement / Data Analyst & BI Developer Portfolio  
**Author:** Senior Data Analyst & BI Developer  
**Date:** August 30, 2026  

---

## 1. Executive Summary

This project delivers an enterprise-grade, end-to-end data analytics and business intelligence pipeline analyzing **99,441 commercial orders** totaling **R$ 15.84 Million in Gross Revenue** from the Brazilian Olist E-Commerce ecosystem.

The pipeline spans raw data ingestion, automated Python cleaning, feature engineering, relational schema modeling, SQL data quality audits, 24 analytical business queries, a star-schema Power BI data model, a 28-measure DAX calculation layer, a 5-page interactive dashboard architecture, and empirical business strategy recommendations.

---

## 2. Technical Architecture & Data Pipeline

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   Raw Layer     │  ──►  │ Python Cleaning │  ──►  │ Feature Eng.    │
│  (9 Olist CSVs) │       │ (data_clean.py) │       │ (feature_eng.py)│
└─────────────────┘       └─────────────────┘       └────────┬────────┘
                                                             │
                                                             ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Power BI Engine │  ◄──  │ 24+ SQL Queries │  ◄──  │ SQLite/MySQL DB │
│(Star Schema/DAX)│       │ (04_business.sql│       │ (ecommerce.db)  │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

1. **Python Data Cleaning (`python/data_cleaning.py`)**:
   - Parses date fields, enforces ISO timestamps, resolves 100% of Portuguese-to-English product category translations, eliminates duplicate records, imputes missing product dimensions, and removes chronological anomalies.
2. **Feature Engineering (`python/feature_engineering.py`)**:
   - Derives total revenue (`price + freight_value`), operational lead times (`delivery_days`, `approval_days`), delivery buffers (`estimated_delivery_gap`), customer value segmentation (Low <$100, Medium $100-$500, High >$500), customer repeat flags, and a dedicated 1,096-day `DimDate` calendar table.
3. **Database Engine (`data/ecommerce.db` & `sql/`)**:
   - Normalizes data into 5 Dimensions and 3 Fact tables with primary keys, foreign keys, and B-Tree indexes.
   - Passes 10 automated SQL data quality tests with zero defects.
4. **Power BI Modeling & DAX (`powerbi/`)**:
   - Star Schema with single-directional 1-to-Many relationships.
   - 28 formatted DAX measures including Time Intelligence (`MoM Growth`, `YoY Growth`), Customer LTV, and a What-If Delivery Improvement Scenario.
5. **Interactive 5-Page Dashboard (`screenshots/` & `powerbi/`)**:
   - Page 1: Executive Overview
   - Page 2: Sales & Product Analysis
   - Page 3: Customer Intelligence & Segmentation
   - Page 4: Delivery Logistics & Customer Experience
   - Page 5: Geographic & Regional Analysis

---

## 3. Core Findings & Business Intelligence Summary

- **Total Gross Revenue:** R$ 15,843,553.24 across 99,441 orders with an Average Order Value (AOV) of R$ 159.33.
- **Customer Retention Deficit:** 96.88% of customers are single-order buyers (93,099), while repeat customers represent only 3.12% (2,997).
- **Logistics & Satisfaction Link:** A strong inverse correlation (r = -0.334) exists between delivery duration and review ratings. Deliveries taking under 5 days achieve a 4.45 / 5.0 rating, while shipments delayed beyond 30 days drop to 1.76 / 5.0.
- **Geographic Concentration:** The Southeast region (SP, RJ, MG, RS, PR) captures 73.5% of gross revenue, with São Paulo (SP) alone contributing 37.4%. Northern states suffer from transit times up to 29.3 days.
- **Pareto Category Dominance:** The top 5 product categories (Health & Beauty, Watches, Bed & Bath, Sports, Computers) account for R$ 6.20M (39.1% of revenue), while the top 15 categories capture 78.4%.

---

## 4. Project Deliverables Checklist

| Category | Deliverable File / Directory | Status |
| :--- | :--- | :--- |
| **Data Cleaning** | `python/data_cleaning.py` & `notebooks/01_data_cleaning.ipynb` | **COMPLETED & VERIFIED** |
| **Feature Engineering** | `python/feature_engineering.py` & `data/processed/` | **COMPLETED & VERIFIED** |
| **Exploratory Data Analysis**| `python/eda.py` & `notebooks/02_exploratory_data_analysis.ipynb` | **COMPLETED & VERIFIED** |
| **Database & Loading** | `sql/01_database_schema.sql`, `sql/02_data_loading.sql`, `data/ecommerce.db` | **COMPLETED & VERIFIED** |
| **SQL Audits & Queries** | `sql/03_data_quality.sql`, `sql/04_business_analysis.sql`, `sql/05_advanced_analysis.sql` | **COMPLETED & VERIFIED** |
| **Power BI Architecture** | `powerbi/data_model.md`, `powerbi/power_query_steps.md`, `powerbi/dax_measures.md` | **COMPLETED & VERIFIED** |
| **Dashboard Specifications** | `powerbi/dashboard_specification.md` & `screenshots/` (5 pages) | **COMPLETED & VERIFIED** |
| **Documentation & Reports** | `docs/DATA_DICTIONARY.md`, `docs/BUSINESS_INSIGHTS.md`, `docs/VALIDATION_REPORT.md` | **COMPLETED & VERIFIED** |
| **Repository Setup** | `README.md`, `requirements.txt`, `.gitignore`, `.env.example` | **COMPLETED & VERIFIED** |
