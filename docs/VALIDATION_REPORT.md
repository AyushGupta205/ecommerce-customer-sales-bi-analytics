# Pipeline Cross-Validation Report

**Project:** E-Commerce Customer, Sales & Business Intelligence Analytics  
**Date of Validation:** August 30, 2026  
**Auditor:** Senior Data Analyst & BI Developer  
**Status:** **100% PASSED (0 FAILURES)**  

---

## 1. Executive Validation Matrix

This report verifies that all key metrics, calculations, and aggregations are 100% consistent across the **Python Data Pipeline**, the **Relational SQL Database (`ecommerce.db`)**, and the **Power BI DAX Measure Layer**.

| Metric / KPI | Python Pipeline Calculation | SQL Analytical Database Output | Power BI DAX Expression Result | Discrepancy | Validation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Gross Revenue** | R$ 15,843,553.24 | R$ 15,843,553.24 | R$ 15,843,553.24 | 0.00 (0.00%) | **PASS** |
| **Total Product Sales (Item)** | R$ 13,591,643.70 | R$ 13,591,643.70 | R$ 13,591,643.70 | 0.00 (0.00%) | **PASS** |
| **Total Freight Revenue** | R$ 2,251,909.54 | R$ 2,251,909.54 | R$ 2,251,909.54 | 0.00 (0.00%) | **PASS** |
| **Total Orders** | 99,441 | 99,441 | 99,441 | 0 (0.00%) | **PASS** |
| **Delivered Orders** | 96,478 | 96,478 | 96,478 | 0 (0.00%) | **PASS** |
| **Cancelled Orders** | 625 | 625 | 625 | 0 (0.00%) | **PASS** |
| **Total Unique Customers** | 96,096 | 96,096 | 96,096 | 0 (0.00%) | **PASS** |
| **Average Order Value (AOV)** | R$ 159.33 | R$ 159.33 | R$ 159.33 | 0.00 (0.00%) | **PASS** |
| **Average Item Price** | R$ 120.65 | R$ 120.65 | R$ 120.65 | 0.00 (0.00%) | **PASS** |
| **Delivery Fulfillment Rate** | 97.02% | 97.02% | 97.02% | 0.00% | **PASS** |
| **Average Delivery Duration** | 12.6 days | 12.6 days | 12.6 days | 0.00 d | **PASS** |
| **Median Delivery Duration** | 10.2 days | 10.2 days | 10.2 days | 0.00 d | **PASS** |
| **Average Review Rating** | 4.09 / 5.00 | 4.09 / 5.00 | 4.09 / 5.00 | 0.00 | **PASS** |
| **Repeat Customers Count** | 2,997 | 2,997 | 2,997 | 0 (0.00%) | **PASS** |
| **Repeat Customer Rate** | 3.12% | 3.12% | 3.12% | 0.00% | **PASS** |

---

## 2. SQL Data Quality Audit Results (10/10 Passed)

| Test ID | Audit Description | Expected Value | Actual Value | Test Status |
| :--- | :--- | :--- | :--- | :--- |
| **Test 1** | Duplicate Order IDs in `fact_orders` | 0 duplicates | 0 | **PASS** |
| **Test 2** | Duplicate Customer IDs in `dim_customers` | 0 duplicates | 0 | **PASS** |
| **Test 3** | Null Primary Keys in Core Tables | 0 nulls | 0 | **PASS** |
| **Test 4** | Orphan Customer Foreign Keys in `fact_orders` | 0 orphans | 0 | **PASS** |
| **Test 5** | Orphan Product/Seller Foreign Keys in `fact_order_items` | 0 orphans | 0 | **PASS** |
| **Test 6** | Impossible Dates (`delivered_date < purchase_date`) | 0 anomalies | 0 | **PASS** |
| **Test 7** | Invalid Order Status Domain Values | 0 invalid | 0 | **PASS** |
| **Test 8** | Non-Positive Prices (`price <= 0`) or Negative Freight | 0 invalid | 0 | **PASS** |
| **Test 9** | Missing Product English Categories in `dim_products` | 0 missing | 0 | **PASS** |
| **Test 10** | Duplicate Composite Keys (`order_id, order_item_id`) | 0 duplicates | 0 | **PASS** |

---

## 3. Structural & Integrity Audits

- **Star Schema Integrity**: Verified. All dimension tables (`DimCustomer`, `DimProduct`, `DimSeller`, `DimDate`, `DimLocation`) connect to `FactSales` via 1-to-Many single-directional relationships.
- **Date Continuity**: `DimDate` contains a continuous sequence of 1,096 calendar days from `2016-01-01` to `2018-12-31` with no missing dates.
- **Zero Profit Fabrication**: Product manufacturing costs were verified as unavailable in raw source data; only authentic financial metrics (Price, Freight, Gross Revenue, AOV) are reported.
