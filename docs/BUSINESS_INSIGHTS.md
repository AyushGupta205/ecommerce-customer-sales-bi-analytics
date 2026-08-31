# E-Commerce Business Insights & Empirical Findings

**Project:** E-Commerce Customer, Sales & Business Intelligence Analytics  
**Dataset:** Brazilian Olist E-Commerce Dataset (99,441 orders | 2016–2018)  
**Total Analyzed Gross Revenue:** R$ 15,843,553.24  

---

## Executive Summary Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CORE BUSINESS SNAPSHOT                          │
├──────────────────────────┬──────────────────────┬──────────────────────┤
│ Gross Revenue            │ R$ 15,843,553.24     │ Price + Freight      │
│ Total Orders Placed      │ 99,441 Orders        │ 97.02% Delivered     │
│ Total Unique Customers   │ 96,096 Buyers        │ 3.12% Repeat Rate    │
│ Average Order Value      │ R$ 159.33            │ Gross per order      │
│ Avg Delivery Lead Time   │ 12.6 Days            │ Median: 10.2 Days    │
│ Customer Satisfaction    │ 4.09 / 5.00 Stars    │ 57.8% 5-Star Reviews │
└──────────────────────────┴──────────────────────┴──────────────────────┘
```

---

## Insight 1: Steep Customer Retention Bottleneck (96.88% One-Time Buyers)

### Finding
The platform suffers from an extreme one-and-done purchase pattern: 96.88% of unique customers (93,099 individuals) made only a single purchase across the entire 2-year window, while repeat customers accounted for just 3.12% (2,997 individuals).

### Evidence
- Total Unique Customers: 96,096
- Single-Order Buyers: 93,099 (96.88%)
- Multi-Order Buyers: 2,997 (3.12%)
- Average orders per unique customer: 1.035

### Business Meaning
The business model is almost entirely dependent on continuous and expensive top-of-funnel customer acquisition rather than recurring lifetime value (LTV). While customer acquisition is healthy, the lack of retention mechanisms inflates customer acquisition costs (CAC) and limits long-term compounding profitability.

### Actionable Recommendation
Deploy an automated post-purchase CRM sequence:
1. Trigger category-specific replenishment emails (e.g., Health & Beauty consumables at 30/60-day intervals).
2. Offer second-order incentive credits or loyalty tier discounts valid within 45 days of delivery.

---

## Insight 2: High Delivery Lead Times Strongly Degrade Customer Satisfaction

### Finding
There is a direct inverse correlation between delivery duration and customer satisfaction. While orders delivered under 5 days achieve an average rating of 4.45 / 5.0, orders taking over 30 days collapse to 1.76 / 5.0.

### Evidence
- Pearson Correlation (Delivery Days vs Review Score): **r = -0.334**
- **0–5 Days Delivery**: Avg Score: **4.45** | 67.2% 5-Star | 7.3% 1-Star
- **6–10 Days Delivery**: Avg Score: **4.32** | 62.1% 5-Star | 8.8% 1-Star
- **11–15 Days Delivery**: Avg Score: **4.16** | 56.4% 5-Star | 11.2% 1-Star
- **16–20 Days Delivery**: Avg Score: **3.88** | 47.1% 5-Star | 17.5% 1-Star
- **21–30 Days Delivery**: Avg Score: **3.38** | 35.8% 5-Star | 28.4% 1-Star
- **31–60 Days Delivery**: Avg Score: **2.14** | 18.2% 5-Star | 56.9% 1-Star
- **60+ Days Delivery**: Avg Score: **1.76** | 15.2% 5-Star | 68.8% 1-Star

### Business Meaning
Logistics delays are the single largest driver of negative reviews, customer dissatisfaction, and brand churn. Once delivery exceeds 20 days, the probability of receiving a 1- or 2-star rating surges past 40%.

### Actionable Recommendation
Establish strict Carrier SLAs:
1. Cap maximum delivery commitment windows for inter-state shipments.
2. Provide proactive tracking SMS notifications if an in-transit parcel approaches day 14 to manage customer expectations before review submission.

---

## Insight 3: Disproportionate Geographic Concentration in Southeast Brazil

### Finding
Order volume and gross revenue are heavily concentrated in the Southeast region of Brazil, with the state of São Paulo (SP) alone generating over 37% of platform revenue.

### Evidence
- Top 5 States by Gross Revenue:
  1. **São Paulo (SP)**: R$ 5,927,159.25 (37.41% share | 41,746 orders)
  2. **Rio de Janeiro (RJ)**: R$ 2,144,379.69 (13.53% share | 12,852 orders)
  3. **Minas Gerais (MG)**: R$ 1,872,019.24 (11.82% share | 11,635 orders)
  4. **Rio Grande do Sul (RS)**: R$ 890,898.34 (5.62% share | 5,466 orders)
  5. **Paraná (PR)**: R$ 811,156.38 (5.12% share | 5,045 orders)
- Top 5 States Combined Share: **73.5% of total revenue** and **77.2% of order volume**.

### Business Meaning
The platform’s fulfillment infrastructure operates efficiently near the industrial hub of São Paulo (where average delivery lead time is 8.3 days), but remote northern and northeastern regions suffer from extended transit times (e.g., Roraima RR at 29.3 days; Amapá AP at 27.1 days).

### Actionable Recommendation
1. Focus paid performance marketing spend primarily on high-converting SP/RJ/MG corridors.
2. Establish regional micro-fulfillment distribution hubs in Northern hubs (e.g., Salvador BA or Recife PE) to cut transit times to under 12 days.

---

## Insight 4: Revenue Concentration in Core 80% Categories (Pareto Rule)

### Finding
The platform’s 71 product categories follow a classic Pareto distribution: the top 15 product categories generate over 78.4% of total gross platform revenue.

### Evidence
- **Top 5 Revenue Categories**:
  1. **Health Beauty**: R$ 1,441,248.07 (9,670 items | Avg Price R$ 130.16)
  2. **Watches Gifts**: R$ 1,305,541.61 (5,991 items | Avg Price R$ 201.14)
  3. **Bed Bath Table**: R$ 1,241,681.72 (11,115 items | Avg Price R$ 93.30)
  4. **Sports Leisure**: R$ 1,156,656.48 (8,641 items | Avg Price R$ 114.34)
  5. **Computers Accessories**: R$ 1,059,272.40 (7,827 items | Avg Price R$ 116.51)
- Cumulative Top 5 Revenue: R$ 6.20M (39.1% of total)
- Cumulative Top 15 Revenue: R$ 12.42M (78.4% of total)
- Bottom 20 Categories Combined: Under R$ 180,000 (1.1% of total)

### Business Meaning
A handful of consumer lifestyle and electronics categories generate the overwhelming majority of marketplace cash flow, while dozens of low-velocity categories create catalog bloat and operational overhead.

### Actionable Recommendation
Prioritize merchant onboarding and promotional co-marketing in the top 5 powerhouse categories (Health & Beauty, Watches, Bed & Bath, Sports, Computers).

---

## Insight 5: High-Value Customer Tier Generates 27.1% of Revenue with 4.6% of Buyers

### Finding
Customers spending over R$ 500 (High-Value segment) represent only 4.6% of the customer base but account for over 27.1% of all revenue generated.

### Evidence
- **High-Value Tier (> R$ 500)**: 4,424 customers (4.60%) → R$ 4,594,027.05 revenue (27.07% share)
- **Medium-Value Tier (R$ 100–R$ 500)**: 46,869 customers (48.77%) → R$ 9,686,565.49 revenue (57.08% share)
- **Low-Value Tier (< R$ 100)**: 44,803 customers (46.62%) → R$ 2,689,079.51 revenue (15.85% share)

### Business Meaning
High-value purchasers exhibit strong purchasing power and represent prime candidates for premium subscription programs, expedited shipping packages, and VIP loyalty perks.

### Actionable Recommendation
Implement a VIP Tier program with free expedited shipping thresholds for orders over R$ 300 to migrate Medium-Value customers into High-Value spenders.

---

## Insight 6: Credit Card Dominance & Installment Dependency

### Finding
Credit card payments dominate the platform, representing 75.4% of total payment volume, with an average installment count of 3.5 months. Over 51% of credit card transactions are split into multiple monthly installments.

### Evidence
- **Credit Card**: R$ 12,542,084.19 (75.4% share | 76,795 transactions | Avg Installments: 3.5)
- **Boleto (Bancário)**: R$ 2,869,361.69 (17.3% share | 19,784 transactions)
- **Voucher**: R$ 379,436.87 (2.3% share | 5,775 transactions)
- **Debit Card**: R$ 217,989.79 (1.3% share | 1,529 transactions)

### Business Meaning
Brazilian e-commerce consumers rely heavily on installment financing to afford medium-to-high ticket items. Restricting installments or offering poor credit card processing would immediately suppress order conversion.

### Actionable Recommendation
Partner with fintech payment gateways to offer 0%-interest installment promotions (up to 6 installments) during peak sales months (November Black Friday and May Mother's Day).

---

## Insight 7: Punctual Delivery vs Delayed Delivery Sentiment Split

### Finding
Delivering before or on the estimated delivery date results in 88.4% positive ratings (4 and 5 stars), whereas deliveries exceeding the estimated date experience an immediate surge in 1-star reviews from 6.8% up to 55.4%.

### Evidence
- **On-Time / Early Deliveries**: Avg Review Score: **4.29** | 5-Star: **63.8%** | 1-Star: **6.8%**
- **Delayed Deliveries**: Avg Review Score: **2.21** | 5-Star: **17.9%** | 1-Star: **55.4%**
- Overall Delay Rate: **8.1%** of delivered orders arrived after the promised date.

### Business Meaning
Customer dissatisfaction is primarily a function of broken promises rather than pure transit days. A 15-day delivery promised as 18 days yields positive reviews, but a 10-day delivery promised as 8 days creates resentment.

### Actionable Recommendation
Calibrate the automated estimated delivery date algorithm by adding a dynamic +2 day safety buffer on inter-state routes to ensure >96% on-time arrival.

---

## Insight 8: Freight Cost Friction on Low-Ticket Items

### Finding
Freight cost represents an average of 16.5% of total gross revenue across all categories, but in low-ticket categories (e.g., Home Comfort, Fashion Childrens Clothes), freight exceeds 35% to 45% of the item purchase price.

### Evidence
- Overall Product Price: R$ 13,591,643.70 (85.8%) vs Freight: R$ 2,251,909.54 (14.2%)
- Top Category Freight Shares:
  - Furniture Decor: 24.3% Freight Share
  - Bed Bath Table: 18.2% Freight Share
  - Watches Gifts: 7.9% Freight Share
  - Computers Accessories: 12.1% Freight Share

### Business Meaning
Bulky or low-priced items experience high cart abandonment due to "freight shock" at checkout. High-value, compact items (Watches, Perfumes) have minimal freight friction.

### Actionable Recommendation
Introduce multi-item bundled shipping discounts or free freight thresholds (e.g., "Add R$ 50 more to unlock free shipping") to increase basket sizes and offset unit freight overhead.

---

## Insight 9: Strong Seasonal Revenue Spikes (November Black Friday Effect)

### Finding
Revenue expanded dramatically from early 2017 through mid 2018, reaching an all-time peak in November 2017 driven by Black Friday campaigns (over R$ 1.19M in a single month).

### Evidence
- Jan 2017: R$ 138.3K Revenue (949 orders)
- Nov 2017: R$ 1,194.8K Revenue (7,544 orders — 764% growth vs Jan 2017)
- MoM Spike in Nov 2017: **+53.2% revenue surge** over Oct 2017.

### Business Meaning
Marketing campaigns and promotional discounts around Brazilian Black Friday generate massive demand surges that stress seller logistics and carrier capacity.

### Actionable Recommendation
Implement pre-holiday merchant inventory audits starting in September to ensure top sellers hold adequate stock in regional warehouses before the November surge.

---

## Insight 10: Seller Concentration Risk

### Finding
Top 1% of sellers (31 merchants out of 3,095) fulfill over 22.4% of all platform order items and generate over R$ 3.55M in gross sales.

### Evidence
- Total Active Sellers: 3,095
- Top 50 Sellers fulfill 31.8% of all platform line items.
- Top 1 Seller alone fulfilled 2,033 items (R$ 229.4K gross revenue).

### Business Meaning
The marketplace is dependent on a select group of top-performing power sellers. If key sellers face supply chain disruption or leave for rival marketplaces, category revenue would face immediate contraction.

### Actionable Recommendation
Create a Dedicated Key Account Management (KAM) program for the top 100 sellers, offering lower platform commissions, priority marketing placement, and dedicated logistics support.
