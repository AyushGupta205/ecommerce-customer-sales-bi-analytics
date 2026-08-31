# Power BI 5-Page Interactive Dashboard Specification

**Project:** E-Commerce Customer, Sales & Business Intelligence Analytics  
**Target Resolution:** 16:9 (1920 x 1080 px)  
**Color Palette:** Executive Dark Slate (`#1A202C`), Tech Blue (`#2B6CB0`), Accent Emerald (`#38A169`), Coral Red (`#E53E3E`), Slate Grey (`#718096`), Background Light (`#F4F6F9`)  
**Typography:** Segoe UI / Arial  

---

## PAGE 1 — EXECUTIVE OVERVIEW

### Business Purpose
Provide C-Suite and VP-level stakeholders with instant visibility into high-level business health, top-line gross revenue, total order velocity, delivery fulfillment rates, and customer satisfaction ratings.

### Layout Grid & Visual Specifications
1. **Header & Global Slicer Bar (Top)**:
   - Slicers: `Year` (2017, 2018), `Quarter`, `Customer State`, `Product Category`, `Order Status`.
2. **KPI Scorecards (Row 1)**:
   - **Card 1**: Total Gross Revenue (`[Total Revenue]`) — Formatted as `R$ 15.84M`.
   - **Card 2**: Total Orders (`[Total Orders]`) — Formatted as `99.4K`.
   - **Card 3**: Average Order Value (`[Average Order Value]`) — Formatted as `R$ 159.33`.
   - **Card 4**: Delivery Fulfillment Rate (`[Delivery Rate]`) — `97.0%`.
   - **Card 5**: Average Customer Rating (`[Average Review Score]`) — `4.09 / 5.0`.
3. **Monthly Revenue & Order Volume Growth (Row 2, Left - 65% width)**:
   - *Visual Type*: Line & Clustered Column Combo Chart.
   - *X-Axis*: `DimDate[year_month]`.
   - *Column Y-Axis*: `[Total Revenue]`.
   - *Line Y-Axis*: `[Total Orders]`.
   - *Interactivity*: Drill-down from Year -> Quarter -> Month.
4. **Order Status Distribution (Row 2, Right - 35% width)**:
   - *Visual Type*: Donut Chart.
   - *Legend*: `FactOrders[order_status]`.
   - *Values*: `[Total Orders]`.
5. **Top 7 Product Categories by Revenue (Row 3, Left - 65% width)**:
   - *Visual Type*: Horizontal Bar Chart.
   - *Y-Axis*: `DimProduct[product_category_name_english]`.
   - *X-Axis*: `[Total Revenue]`.
6. **Top 5 Revenue Generating States (Row 3, Right - 35% width)**:
   - *Visual Type*: Clustered Column Chart.
   - *X-Axis*: `DimCustomer[customer_state]`.
   - *Y-Axis*: `[Total Revenue]`.

---

## PAGE 2 — SALES & PRODUCT ANALYSIS

### Business Purpose
Deep-dive into product catalog performance, identifying revenue drivers, item pricing elasticities, shipping cost proportions, and category volume vs value dynamics.

### Layout Grid & Visual Specifications
1. **KPI Scorecards (Top)**:
   - `[Total Revenue]`, `[Total Items Sold]`, `[Average Item Price]`, `[Total Freight]`.
2. **Top 10 Product Categories by Revenue (Top Left)**:
   - *Visual Type*: Stacked Horizontal Bar Chart.
   - *Y-Axis*: `DimProduct[product_category_name_english]`.
   - *Values*: `[Total Product Sales]`, `[Total Freight]`.
3. **Item Volume vs Average Price Matrix (Top Right)**:
   - *Visual Type*: Scatter Plot.
   - *X-Axis*: `[Total Items]`.
   - *Y-Axis*: `[Average Item Price]`.
   - *Size*: `[Total Revenue]`.
   - *Details*: `DimProduct[product_category_name_english]`.
4. **Product Price vs Freight Cost Contribution (Bottom Left)**:
   - *Visual Type*: 100% Stacked Bar Chart.
   - *Y-Axis*: Top 8 Categories.
   - *Values*: `Price %`, `Freight %`.
5. **Detailed Product Category Performance Table (Bottom Right)**:
   - *Columns*: Category Name, Units Sold, Gross Revenue, Avg Item Price, Avg Freight per Item, Avg Review Score.

---

## PAGE 3 — CUSTOMER INTELLIGENCE & SEGMENTATION

### Business Purpose
Analyze customer acquisition vs retention, customer lifetime value (CLV) tiers, repeat purchasing patterns, and preferred payment mechanisms.

### Layout Grid & Visual Specifications
1. **KPI Scorecards (Top)**:
   - `[Total Customers]`, `[Repeat Customers]`, `[Repeat Customer Rate]`, `[Revenue per Customer]`, `[Average Order Value]`.
2. **New vs Repeat Customer Donut Breakdown (Top Left)**:
   - *Visual Type*: Donut Chart.
   - *Legend*: `DimCustomer[customer_type]` (One-Time vs Repeat).
   - *Values*: `[Total Customers]`, `[Total Revenue]`.
3. **Customer Share vs Revenue Share by Value Tier (Top Right)**:
   - *Visual Type*: Clustered Column Chart.
   - *X-Axis*: `DimCustomer[customer_value_segment]` (Low <$100, Medium $100-$500, High >$500).
   - *Values*: `% of Customer Base`, `% of Gross Revenue`.
4. **Top 10 Highest Spending Customers (Bottom Left)**:
   - *Visual Type*: Horizontal Bar Chart.
   - *Y-Axis*: Customer Unique ID.
   - *X-Axis*: `[Total Revenue]`.
5. **Payment Method Preference across Customer Tiers (Bottom Right)**:
   - *Visual Type*: Stacked Column Chart.
   - *X-Axis*: Customer Value Segment.
   - *Legend*: Payment Type (Credit Card, Boleto, Voucher, Debit Card).
   - *Values*: `[Total Orders]`.

---

## PAGE 4 — DELIVERY & CUSTOMER EXPERIENCE

### Business Purpose
Evaluate fulfillment logistics, carrier speed, delivery punctuality against estimated delivery dates, and the direct correlation between shipping delays and customer review scores.

### Layout Grid & Visual Specifications
1. **KPI Scorecards (Top)**:
   - `[Average Delivery Days]`, `[Median Delivery Days]`, `[Delay Rate %]`, `[Average Review Score]`, `[5 Star Review %]`.
2. **Average Review Score by Delivery Duration Bracket (Top Left)**:
   - *Visual Type*: Column Chart with Color Alerting.
   - *X-Axis*: Delivery Duration Tier (0-5d, 6-10d, 11-15d, 16-20d, 21-30d, 31-60d, 60+d).
   - *Y-Axis*: `[Average Review Score]`.
3. **Review Rating Distribution (Top Right)**:
   - *Visual Type*: Bar Chart (1 to 5 Stars).
   - *Values*: `Review Count`, `% of Total Reviews`.
4. **Monthly Delivery Duration Trend (Bottom Left)**:
   - *Visual Type*: Line Chart with Target Constant Line (12.6 days mean).
   - *X-Axis*: `DimDate[year_month]`.
   - *Y-Axis*: `[Average Delivery Days]`.
5. **What-If Simulation: Delivery Lead-Time Improvement Scenario (Bottom Right)**:
   - *Controls*: Numeric Range Slider `[Days Reduced: 0 to 10]`.
   - *Cards*: `[Current Average Delivery Days]`, `[Target Delivery Days]`, `[Simulated Satisfaction Rating]`.

---

## PAGE 5 — GEOGRAPHIC & REGIONAL ANALYSIS

### Business Purpose
Map regional performance across all 27 Brazilian states to identify geographic revenue concentration, logistics bottlenecks in Northern states, and regional AOV variations.

### Layout Grid & Visual Specifications
1. **Brazil State Choropleth / Bubble Map (Top Left)**:
   - *Location*: `DimLocation[geolocation_state]`.
   - *Size / Color*: `[Total Revenue]`.
2. **Top 10 States by Order Volume (Top Right)**:
   - *Visual Type*: Horizontal Bar Chart.
   - *Y-Axis*: `DimCustomer[customer_state]`.
   - *X-Axis*: `[Total Orders]`.
3. **State Delivery Speed: Fastest vs Slowest States (Bottom Left)**:
   - *Visual Type*: Horizontal Diverging Bar Chart.
   - *Y-Axis*: State Code.
   - *X-Axis*: `[Average Delivery Days]`.
4. **Geographic Performance Scorecard Matrix (Bottom Right)**:
   - *Columns*: State, Order Count, Gross Revenue, Revenue Share %, AOV, Average Delivery Days, Delay Rate %, Avg Review Score.
