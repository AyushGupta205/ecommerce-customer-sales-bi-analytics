# DAX Measures Library Specification

**Project:** E-Commerce Customer, Sales & Business Intelligence Analytics  
**Table Location:** `_Measures` Calculation Group  
**Syntax:** Microsoft DAX (Data Analysis Expressions)  

---

## 1. Core Financial & Sales KPIs

### 1.1 Total Revenue
```dax
Total Revenue = 
SUM(FactSales[revenue])
```
*Description:* Calculates total gross e-commerce revenue (Product Price + Freight Value).

### 1.2 Total Product Sales
```dax
Total Product Sales = 
SUM(FactSales[price])
```
*Description:* Sum of item prices excluding shipping and freight charges.

### 1.3 Total Freight Revenue
```dax
Total Freight = 
SUM(FactSales[freight_value])
```
*Description:* Total shipping fees charged across all order items.

### 1.4 Total Orders
```dax
Total Orders = 
DISTINCTCOUNT(FactOrders[order_id])
```
*Description:* Distinct count of unique customer orders placed.

### 1.5 Total Items Sold
```dax
Total Items = 
COUNTROWS(FactSales)
```
*Description:* Total count of distinct physical items purchased.

### 1.6 Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE([Total Revenue], [Total Orders], 0)
```
*Description:* Gross revenue generated per completed order transaction.

### 1.7 Average Item Price
```dax
Average Item Price = 
DIVIDE([Total Product Sales], [Total Items], 0)
```
*Description:* Mean catalog sales price across all purchased items.

### 1.8 Total Customers
```dax
Total Customers = 
DISTINCTCOUNT(DimCustomer[customer_unique_id])
```
*Description:* Total unique individual buyers registered in the database.

### 1.9 Revenue per Customer
```dax
Revenue per Customer = 
DIVIDE([Total Revenue], [Total Customers], 0)
```
*Description:* Lifetime gross revenue generated per unique customer.

---

## 2. Operational & Fulfillment Metrics

### 2.1 Delivered Orders
```dax
Delivered Orders = 
CALCULATE(
    [Total Orders],
    FactOrders[order_status] = "delivered"
)
```

### 2.2 Cancelled Orders
```dax
Cancelled Orders = 
CALCULATE(
    [Total Orders],
    FactOrders[order_status] = "canceled"
)
```

### 2.3 Delivery Rate %
```dax
Delivery Rate = 
DIVIDE([Delivered Orders], [Total Orders], 0)
```

### 2.4 Cancellation Rate %
```dax
Cancellation Rate = 
DIVIDE([Cancelled Orders], [Total Orders], 0)
```

### 2.5 Average Delivery Days
```dax
Average Delivery Days = 
CALCULATE(
    AVERAGE(FactOrders[delivery_days]),
    FactOrders[order_status] = "delivered"
)
```

### 2.6 Median Delivery Days
```dax
Median Delivery Days = 
CALCULATE(
    MEDIAN(FactOrders[delivery_days]),
    FactOrders[order_status] = "delivered"
)
```

### 2.7 Delayed Orders Count
```dax
Delayed Orders = 
CALCULATE(
    [Total Orders],
    FactOrders[order_status] = "delivered",
    FactOrders[is_delayed] = 1
)
```

### 2.8 Delay Rate %
```dax
Delay Rate = 
DIVIDE([Delayed Orders], [Delivered Orders], 0)
```

---

## 3. Customer Retention & Segmentation Metrics

### 3.1 Repeat Customers
```dax
Repeat Customers = 
CALCULATE(
    DISTINCTCOUNT(DimCustomer[customer_unique_id]),
    DimCustomer[customer_order_count] > 1
)
```

### 3.2 Single-Order Customers (New)
```dax
New Customers = 
CALCULATE(
    DISTINCTCOUNT(DimCustomer[customer_unique_id]),
    DimCustomer[customer_order_count] = 1
)
```

### 3.3 Repeat Customer Rate %
```dax
Repeat Customer Rate = 
DIVIDE([Repeat Customers], [Total Customers], 0)
```

### 3.4 Orders per Customer
```dax
Orders per Customer = 
DIVIDE([Total Orders], [Total Customers], 0)
```

---

## 4. Customer Review & Satisfaction Metrics

### 4.1 Average Review Score
```dax
Average Review Score = 
AVERAGE(FactReviews[review_score])
```

### 4.2 5-Star Reviews Count
```dax
5 Star Reviews = 
CALCULATE(
    COUNTROWS(FactReviews),
    FactReviews[review_score] = 5
)
```

### 4.3 5-Star Review %
```dax
5 Star Review % = 
DIVIDE([5 Star Reviews], COUNTROWS(FactReviews), 0)
```

### 4.4 Low Rating Reviews (1 & 2 Stars)
```dax
Low Rating Reviews = 
CALCULATE(
    COUNTROWS(FactReviews),
    FactReviews[review_score] IN {1, 2}
)
```

### 4.5 Low Rating %
```dax
Low Rating % = 
DIVIDE([Low Rating Reviews], COUNTROWS(FactReviews), 0)
```

---

## 5. Time Intelligence & Growth Calculations

### 5.1 Previous Month Revenue (PM)
```dax
Previous Month Revenue = 
CALCULATE(
    [Total Revenue],
    DATEADD(DimDate[date], -1, MONTH)
)
```

### 5.2 Month-over-Month (MoM) Revenue Growth %
```dax
MoM Revenue Growth = 
VAR CurrentRev = [Total Revenue]
VAR PrevRev = [Previous Month Revenue]
RETURN
    IF(
        NOT ISBLANK(PrevRev) && PrevRev > 0,
        DIVIDE(CurrentRev - PrevRev, PrevRev, 0),
        BLANK()
    )
```

### 5.3 Previous Year Revenue (PY)
```dax
Previous Year Revenue = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(DimDate[date])
)
```

### 5.4 Year-over-Year (YoY) Revenue Growth %
```dax
YoY Revenue Growth = 
VAR CurrentRev = [Total Revenue]
VAR PrevYearRev = [Previous Year Revenue]
RETURN
    IF(
        NOT ISBLANK(PrevYearRev) && PrevYearRev > 0,
        DIVIDE(CurrentRev - PrevYearRev, PrevYearRev, 0),
        BLANK()
    )
```

---

## 6. What-If Scenario Analysis: Delivery Improvement Simulation

### 6.1 What-If Parameter: Target Lead Time Reduction (Days)
```dax
Delivery Reduction Days Parameter = 
SELECTEDVALUE('Delivery Scenario'[Days Reduced], 0)
```

### 6.2 Target Average Delivery Days
```dax
Target Delivery Days = 
VAR CurrentDays = [Average Delivery Days]
VAR Reduction = [Delivery Reduction Days Parameter]
RETURN
    MAX(0, CurrentDays - Reduction)
```

### 6.3 Estimated Satisfaction Uplift (Simulation Model)
```dax
Simulated Satisfaction Rating = 
VAR BaseScore = [Average Review Score]
VAR DaysReduced = [Delivery Reduction Days Parameter]
-- Empirical model: each 2 days reduction associates with +0.05 rating uplift
RETURN
    MIN(5.0, BaseScore + (DaysReduced * 0.025))
```
