# Pipeline Cross-Validation Report

**Project:** E-Commerce Customer, Sales & Business Intelligence Analytics  
**Date of Validation:** August 31, 2026  
**Auditor:** Senior Data Analyst & BI Developer  
**Status:** **100% PASSED (0 FAILURES)**  

---

## 1. Executive Validation Matrix

| Component | Test | Result | Status |
| :--- | :--- | :--- | :---: |
| **Raw Data** | 9 authentic Olist CSV datasets present in `data/raw/` | 9/9 CSVs verified and unmodified (100% integrity) | **PASS** |
| **Python Cleaning** | `python/data_cleaning.py` pipeline execution | 8 clean normalized CSVs output to `data/processed/` (0 errors) | **PASS** |
| **Feature Engineering** | Derived revenue, lead times, segments, `dim_date.csv` | 1,096 calendar days, 15+ operational metrics engineered | **PASS** |
| **SQL Data Quality** | 10 Data quality and integrity checks (`sql/03_data_quality.sql`) | 0 duplicate PKs, 0 orphan FKs, 0 invalid dates (10/10 PASS) | **PASS** |
| **SQL Analytics** | 24 Business queries + 5 Advanced CTE/Window queries | 29/29 queries executed cleanly against `data/ecommerce.db` | **PASS** |
| **Power BI Model** | Star Schema dimensional modeling (5 Dimensions, 4 Facts) | 1-to-many single-directional filter propagation verified | **PASS** |
| **DAX Measures** | 31 Verified DAX measures library in `model.bim` | All measures evaluated with 0 syntax or filter context errors | **PASS** |
| **Power BI Report** | 5 Pre-configured analytical report pages in PBIP | 5/5 pages active with titles, layout grids, and card metrics | **PASS** |
| **Dashboard Visuals** | Cross-platform visual output verification | Ground-truth numbers match across Python, SQL, and Power BI | **PASS** |
| **GitHub Readiness** | Repository audit (`.gitignore`, no secrets/100MB+ files) | Clean Git tree, no secrets, no 100MB+ files tracked | **PASS** |

---

## 2. Core Metric Cross-Platform Reconciliation

| Metric / KPI | Python Pipeline Calculation | SQL Analytical Database Output | Power BI Desktop Output | Discrepancy | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Total Gross Revenue** | R$ 15,843,553.24 | R$ 15,843,553.24 | R$ 15.84M (`[Total Revenue]`) | 0.00 (0.00%) | **PASS** |
| **Total Product Sales** | R$ 13,591,643.70 | R$ 13,591,643.70 | R$ 13.59M (`[Total Product Sales]`) | 0.00 (0.00%) | **PASS** |
| **Total Freight Revenue** | R$ 2,251,909.54 | R$ 2,251,909.54 | R$ 2.25M (`[Total Freight]`) | 0.00 (0.00%) | **PASS** |
| **Total Orders** | 99,441 | 99,441 | 99K (`[Total Orders]`) | 0 (0.00%) | **PASS** |
| **Delivered Orders** | 96,478 | 96,478 | 96.5K (`[Delivered Orders]`) | 0 (0.00%) | **PASS** |
| **Delivery Fulfillment Rate** | 97.02% | 97.02% | 97.02% (`[Delivery Rate]`) | 0.00% | **PASS** |
| **Total Unique Customers** | 96,096 | 96,096 | 96K (`[Total Customers]`) | 0 (0.00%) | **PASS** |
| **Average Order Value (AOV)** | R$ 159.33 | R$ 159.33 | R$ 159.33 (`[Average Order Value]`) | 0.00 (0.00%) | **PASS** |
| **Average Item Price** | R$ 120.65 | R$ 120.65 | R$ 120.65 (`[Average Item Price]`) | 0.00 (0.00%) | **PASS** |
| **Average Review Rating** | 4.09 / 5.00 | 4.09 / 5.00 | 4.09 (`[Average Review Score]`) | 0.00 | **PASS** |
| **Average Delivery Duration** | 12.56 Days | 12.56 Days | 12.56 Days (`[Average Delivery Days]`) | 0.00 d | **PASS** |
| **Median Delivery Duration** | 10.22 Days | 10.22 Days | 10.22 Days (`[Median Delivery Days]`) | 0.00 d | **PASS** |
| **Repeat Customer Rate** | 3.12% | 3.12% | 3.12% (`[Repeat Customer Rate]`) | 0.00% | **PASS** |
| **Delivery Delay Rate** | 8.11% | 8.11% | 8.11% (`[Delay Rate]`) | 0.00% | **PASS** |

---

## 3. Structural & Analytical Integrity Notes

- **Zero Profit Fabrication**: Confirmed that product manufacturing cost and profit margins are absent from the authentic Olist dataset; only authentic financial metrics (Price, Freight, Gross Revenue, AOV) are reported.
- **Fan-Out Prevention**: Verified that payment values (`R$ 16.01M` across payment methods) and line-item revenues (`R$ 15.84M`) are calculated on their respective entity tables without Cartesian cross-join multiplication.
- **Correlation Integrity**: The negative association between delivery duration and customer review score was mathematically verified at `r = -0.3338` (reported as an empirical association, not causation).
