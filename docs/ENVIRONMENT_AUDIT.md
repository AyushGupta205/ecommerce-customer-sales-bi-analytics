# Environment Audit Report

**Project**: E-Commerce Customer, Sales & Business Intelligence Analytics  
**Date of Audit**: August 30, 2026  
**Auditor**: Lead Data Analyst & BI Developer  

---

## 1. Executive Summary

This environment audit evaluates the software ecosystem, database instances, execution runtimes, and business intelligence tooling available in the host environment prior to building the end-to-end analytics pipeline.

---

## 2. Detected Tooling & Runtime Environment

| Category | Component / Tool | Version Detected | Status | Location / Details |
| :--- | :--- | :--- | :--- | :--- |
| **Operating System** | Microsoft Windows | Windows 10/11 x64 | **ACTIVE** | Host OS |
| **Python Runtime** | Python (CPython) | 3.13.1 | **ACTIVE** | System PATH |
| **Data Manipulation** | Pandas | 2.2.3 | **ACTIVE** | Primary ETL engine |
| **Numerical Computing**| NumPy | 2.2.1 | **ACTIVE** | Vectorized computations |
| **Visualization** | Matplotlib | 3.10.0 | **ACTIVE** | Static analytical visual generation |
| **Visualization** | Seaborn | 0.13.2 | **ACTIVE** | Statistical distribution plots |
| **Visualization** | Plotly | 6.2.0 | **ACTIVE** | Interactive visual dashboards |
| **Relational Database**| SQLite | 3.45.3 | **ACTIVE** | Standard Python built-in (`sqlite3`) |
| **Relational Database**| MySQL Server 8.0 | 8.0.46 | **ACTIVE** | Windows Service `MySQL80` (Running) |
| **Database Connector** | PyMySQL | 1.2.0 | **ACTIVE** | Installed for Python MySQL operations |
| **ORM / SQL Engine**   | SQLAlchemy | 2.0.36 | **ACTIVE** | SQL database execution pipeline |
| **Notebook Runner**    | Jupyter / nbformat / nbconvert | 4.3.4 / 5.10.4 | **ACTIVE** | Notebook compilation & execution |
| **BI Tool**            | Microsoft Power BI Desktop | Installed | **AVAILABLE** | `C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe` |

---

## 3. Dataset Audit

- **Dataset Identity**: Brazilian E-Commerce Public Dataset by Olist (2016–2018).
- **Physical Availability**: Confirmed. All 9 raw CSV files are stored under `data/raw/`:
  1. `olist_orders_dataset.csv` (17.6 MB)
  2. `olist_order_items_dataset.csv` (15.4 MB)
  3. `olist_order_reviews_dataset.csv` (14.5 MB)
  4. `olist_customers_dataset.csv` (9.0 MB)
  5. `olist_order_payments_dataset.csv` (5.8 MB)
  6. `olist_products_dataset.csv` (2.4 MB)
  7. `olist_sellers_dataset.csv` (0.17 MB)
  8. `olist_geolocation_dataset.csv` (61.3 MB)
  9. `product_category_name_translation.csv` (2.6 KB)
- **Integrity**: Full schema relationships available across orders, customers, sellers, products, payments, reviews, and geolocations.

---

## 4. Database Environment & Architecture

1. **Embedded Relational Store (SQLite)**:
   - A standalone analytical database `data/ecommerce.db` is built and indexed to allow zero-configuration querying across platforms.
2. **Enterprise Relational Store (MySQL 8.0)**:
   - Complete DDL (`sql/01_database_schema.sql`), Data Ingestion (`sql/02_data_loading.sql`), Data Quality (`sql/03_data_quality.sql`), and Analytical Queries (`sql/04_business_analysis.sql`, `sql/05_advanced_analysis.sql`) are prepared with ANSI/MySQL 8.0 compliance.

---

## 5. Power BI Status & Execution Capability

- **Desktop Application**: Installed at `C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe`.
- **Data Model Architecture**: Star Schema with 3 Fact tables and 5 Dimension tables.
- **DAX & Power Query Specification**: Fully documented in markdown and ready to import into Power BI Desktop.
- **Visual Previews**: Automated high-resolution dashboard previews generated under `screenshots/` for recruiter presentation.

---

## 6. Execution Roadmap

1. Run `python/data_cleaning.py` to validate, cleanse, and export normalized datasets to `data/processed/`.
2. Run `python/feature_engineering.py` to calculate analytical dimensions and derived metrics.
3. Run `python/eda.py` to compute statistical metrics and render charts.
4. Execute `python/export_sqlite_db.py` to instantiate `data/ecommerce.db` and run 10 data quality checks.
5. Run analytical SQL test scripts (`sql/04_business_analysis.sql`, `sql/05_advanced_analysis.sql`).
6. Generate DAX library, Power Query M-code, and 5-page dashboard specifications.
7. Conduct cross-validation across Python, SQL, and Power BI layers.
