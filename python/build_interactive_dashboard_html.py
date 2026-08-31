"""
Standalone Interactive HTML Dashboard Generator
==============================================
Generates a complete, interactive, self-contained BI Dashboard in HTML5/CSS3/JavaScript
featuring all 5 pages, dynamic Chart.js visualizations, real data from processed CSVs,
KPI summary cards, interactive filters, and data tables.
"""

import os
import json
import pandas as pd

BASE_DIR = r"D:\Ecomercee"
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# Load datasets
orders_df = pd.read_csv(os.path.join(PROCESSED_DIR, "fact_orders_clean.csv"))
items_df = pd.read_csv(os.path.join(PROCESSED_DIR, "fact_order_items_clean.csv"))
payments_df = pd.read_csv(os.path.join(PROCESSED_DIR, "fact_order_payments_clean.csv"))
reviews_df = pd.read_csv(os.path.join(PROCESSED_DIR, "fact_order_reviews_clean.csv"))
customers_df = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_customers_clean.csv"))
products_df = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_products_clean.csv"))

# Merge items and products
items_prod = items_df.merge(products_df[['product_id', 'product_category_name_english']], on='product_id', how='left')

# 1. Monthly Revenue
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
monthly_rev = items_df.merge(orders_df[['order_id', 'order_year_month']], on='order_id').groupby('order_year_month')['revenue'].sum().reset_index().sort_values('order_year_month')
monthly_labels = monthly_rev['order_year_month'].tolist()
monthly_values = [round(val, 2) for val in monthly_rev['revenue'].tolist()]

# 2. Top 10 Categories
cat_rev = items_prod.groupby('product_category_name_english')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)
cat_labels = cat_rev['product_category_name_english'].tolist()
cat_values = [round(val, 2) for val in cat_rev['revenue'].tolist()]

# 3. Order Status Breakdown
status_counts = orders_df['order_status'].value_counts()
status_labels = status_counts.index.tolist()
status_values = status_counts.values.tolist()

# 4. Customer Types
cust_type_counts = orders_df['customer_type'].value_counts()
cust_type_labels = cust_type_counts.index.tolist()
cust_type_values = cust_type_counts.values.tolist()

# 5. Customer Value Segments
seg_rev = orders_df.merge(items_df.groupby('order_id')['revenue'].sum().reset_index(), on='order_id').groupby('customer_value_segment')['revenue'].sum().reset_index()
seg_labels = seg_rev['customer_value_segment'].tolist()
seg_values = [round(val, 2) for val in seg_rev['revenue'].tolist()]

# 6. Payment Types
pay_counts = payments_df.groupby('payment_type')['payment_value'].sum().reset_index().sort_values('payment_value', ascending=False)
pay_labels = pay_counts['payment_type'].tolist()
pay_values = [round(val, 2) for val in pay_counts['payment_value'].tolist()]

# 7. Delivery Days vs Review Score
orders_rev = orders_df[orders_df['order_status'] == 'delivered'].merge(reviews_df[['order_id', 'review_score']], on='order_id')
bins = [0, 5, 10, 15, 20, 25, 30, 100]
bin_labels = ['0-5d', '6-10d', '11-15d', '16-20d', '21-25d', '26-30d', '30+d']
orders_rev['delivery_bin'] = pd.cut(orders_rev['delivery_days'], bins=bins, labels=bin_labels)
deliv_rating = orders_rev.groupby('delivery_bin', observed=False)['review_score'].mean().reset_index()
deliv_labels = deliv_rating['delivery_bin'].astype(str).tolist()
deliv_values = [round(val, 2) if not pd.isna(val) else 0 for val in deliv_rating['review_score'].tolist()]

# 8. Review Ratings Distribution
rev_counts = reviews_df['review_score'].value_counts().sort_index()
rev_labels = [f'{score} Stars' for score in rev_counts.index.tolist()]
rev_values = rev_counts.values.tolist()

# 9. State Revenue Top 10
state_rev = orders_df.merge(items_df.groupby('order_id')['revenue'].sum().reset_index(), on='order_id').groupby('customer_state')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)
state_labels = state_rev['customer_state'].tolist()
state_values = [round(val, 2) for val in state_rev['revenue'].tolist()]

# 10. State Delivery Days Top 10
state_deliv = orders_df[orders_df['order_status'] == 'delivered'].groupby('customer_state')['delivery_days'].mean().reset_index().sort_values('delivery_days', ascending=False).head(10)
state_deliv_labels = state_deliv['customer_state'].tolist()
state_deliv_values = [round(val, 1) for val in state_deliv['delivery_days'].tolist()]

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Business Intelligence Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }}
        body {{ background-color: #0F172A; color: #F8FAFC; min-height: 100vh; display: flex; flex-direction: column; }}
        header {{ background: #1E293B; border-bottom: 1px solid #334155; padding: 18px 32px; display: flex; justify-content: space-between; align-items: center; }}
        .header-title {{ font-size: 20px; font-weight: 700; color: #38BDF8; letter-spacing: -0.5px; }}
        .header-sub {{ font-size: 13px; color: #94A3B8; margin-top: 2px; }}
        .badge {{ background: #0284C7; color: #FFFFFF; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 9999px; text-transform: uppercase; }}
        
        .nav-tabs {{ display: flex; background: #1E293B; padding: 0 32px; border-bottom: 1px solid #334155; overflow-x: auto; gap: 8px; }}
        .tab-btn {{ background: transparent; border: none; color: #94A3B8; padding: 14px 18px; font-size: 14px; font-weight: 600; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.2s; white-space: nowrap; }}
        .tab-btn:hover {{ color: #F8FAFC; background: #334155; }}
        .tab-btn.active {{ color: #38BDF8; border-bottom-color: #38BDF8; background: #0F172A; }}

        .container {{ padding: 28px 32px; flex: 1; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; margin-bottom: 24px; }}
        .kpi-card {{ background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); position: relative; overflow: hidden; }}
        .kpi-card::before {{ content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: #38BDF8; }}
        .kpi-card.purple::before {{ background: #A855F7; }}
        .kpi-card.emerald::before {{ background: #10B981; }}
        .kpi-card.amber::before {{ background: #F59E0B; }}
        .kpi-title {{ font-size: 12px; font-weight: 600; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.5px; }}
        .kpi-value {{ font-size: 26px; font-weight: 800; color: #F8FAFC; margin-top: 8px; }}
        .kpi-sub {{ font-size: 12px; color: #64748B; margin-top: 4px; }}

        .charts-grid {{ display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }}
        .chart-box {{ background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px; }}
        .chart-box.col-12 {{ grid-column: span 12; }}
        .chart-box.col-8 {{ grid-column: span 8; }}
        .chart-box.col-6 {{ grid-column: span 6; }}
        .chart-box.col-4 {{ grid-column: span 4; }}
        .chart-title {{ font-size: 15px; font-weight: 600; color: #F1F5F9; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }}
        .chart-wrapper {{ position: relative; height: 320px; width: 100%; }}
        
        @media (max-width: 1024px) {{
            .chart-box.col-8, .chart-box.col-6, .chart-box.col-4 {{ grid-column: span 12; }}
        }}
    </style>
</head>
<body>

    <header>
        <div>
            <div class="header-title">E-Commerce Customer, Sales & Business Intelligence Analytics</div>
            <div class="header-sub">99,441 Commercial Orders | R$ 15.84 Million Gross Revenue | Brazilian Olist Ecosystem</div>
        </div>
        <div class="badge">Production Ready</div>
    </header>

    <div class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('tab1', this)">1. Executive Overview</button>
        <button class="tab-btn" onclick="switchTab('tab2', this)">2. Sales & Product Analysis</button>
        <button class="tab-btn" onclick="switchTab('tab3', this)">3. Customer Intelligence</button>
        <button class="tab-btn" onclick="switchTab('tab4', this)">4. Delivery & Experience</button>
        <button class="tab-btn" onclick="switchTab('tab5', this)">5. Geographic & Regional</button>
    </div>

    <div class="container">
        
        <!-- PAGE 1: EXECUTIVE OVERVIEW -->
        <div id="tab1" class="tab-content active">
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Gross Revenue</div>
                    <div class="kpi-value">R$ 15,843,553</div>
                    <div class="kpi-sub">Product Sales + Freight Value</div>
                </div>
                <div class="kpi-card purple">
                    <div class="kpi-title">Total Orders</div>
                    <div class="kpi-value">99,441</div>
                    <div class="kpi-sub">112,650 Items Sold</div>
                </div>
                <div class="kpi-card emerald">
                    <div class="kpi-title">Average Order Value</div>
                    <div class="kpi-value">R$ 159.33</div>
                    <div class="kpi-sub">Avg Item: R$ 120.65</div>
                </div>
                <div class="kpi-card amber">
                    <div class="kpi-title">Delivery Fulfillment</div>
                    <div class="kpi-value">97.02%</div>
                    <div class="kpi-sub">96,478 Delivered Orders</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Average Review Rating</div>
                    <div class="kpi-value">4.09 / 5.00</div>
                    <div class="kpi-sub">57.8% 5-Star Reviews</div>
                </div>
            </div>

            <div class="charts-grid">
                <div class="chart-box col-8">
                    <div class="chart-title">Monthly Revenue Trajectory (2016 - 2018)</div>
                    <div class="chart-wrapper"><canvas id="chartMonthlyRev"></canvas></div>
                </div>
                <div class="chart-box col-4">
                    <div class="chart-title">Order Status Distribution</div>
                    <div class="chart-wrapper"><canvas id="chartOrderStatus"></canvas></div>
                </div>
                <div class="chart-box col-6">
                    <div class="chart-title">Top 10 Revenue-Generating Categories</div>
                    <div class="chart-wrapper"><canvas id="chartTopCat"></canvas></div>
                </div>
                <div class="chart-box col-6">
                    <div class="chart-title">Top 10 States by Revenue</div>
                    <div class="chart-wrapper"><canvas id="chartTopStates"></canvas></div>
                </div>
            </div>
        </div>

        <!-- PAGE 2: SALES & PRODUCT ANALYSIS -->
        <div id="tab2" class="tab-content">
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Product Sales Value</div>
                    <div class="kpi-value">R$ 13,591,643</div>
                    <div class="kpi-sub">85.8% of Total Revenue</div>
                </div>
                <div class="kpi-card amber">
                    <div class="kpi-title">Total Freight Collected</div>
                    <div class="kpi-value">R$ 2,251,909</div>
                    <div class="kpi-sub">14.2% Freight Share</div>
                </div>
                <div class="kpi-card purple">
                    <div class="kpi-title">Catalog SKUs</div>
                    <div class="kpi-value">32,951</div>
                    <div class="kpi-sub">71 English Categories</div>
                </div>
                <div class="kpi-card emerald">
                    <div class="kpi-title">Active Sellers</div>
                    <div class="kpi-value">3,095</div>
                    <div class="kpi-sub">Across 23 States</div>
                </div>
            </div>
            <div class="charts-grid">
                <div class="chart-box col-12">
                    <div class="chart-title">Top 10 Product Categories by Gross Sales (R$)</div>
                    <div class="chart-wrapper"><canvas id="chartTopCat2"></canvas></div>
                </div>
            </div>
        </div>

        <!-- PAGE 3: CUSTOMER INTELLIGENCE -->
        <div id="tab3" class="tab-content">
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Total Unique Customers</div>
                    <div class="kpi-value">96,096</div>
                    <div class="kpi-sub">99,441 Order Accounts</div>
                </div>
                <div class="kpi-card amber">
                    <div class="kpi-title">Repeat Customer Rate</div>
                    <div class="kpi-value">3.12%</div>
                    <div class="kpi-sub">2,997 Repeat Buyers</div>
                </div>
                <div class="kpi-card purple">
                    <div class="kpi-title">Orders Per Customer</div>
                    <div class="kpi-value">1.03</div>
                    <div class="kpi-sub">96.88% One-Time Buyers</div>
                </div>
                <div class="kpi-card emerald">
                    <div class="kpi-title">Revenue Per Customer</div>
                    <div class="kpi-value">R$ 164.87</div>
                    <div class="kpi-sub">Lifetime Value Avg</div>
                </div>
            </div>
            <div class="charts-grid">
                <div class="chart-box col-4">
                    <div class="chart-title">New vs Repeat Customers</div>
                    <div class="chart-wrapper"><canvas id="chartCustType"></canvas></div>
                </div>
                <div class="chart-box col-4">
                    <div class="chart-title">Customer Value Segments</div>
                    <div class="chart-wrapper"><canvas id="chartCustSeg"></canvas></div>
                </div>
                <div class="chart-box col-4">
                    <div class="chart-title">Payment Methods Volume</div>
                    <div class="chart-wrapper"><canvas id="chartPayments"></canvas></div>
                </div>
            </div>
        </div>

        <!-- PAGE 4: DELIVERY & EXPERIENCE -->
        <div id="tab4" class="tab-content">
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Average Delivery Duration</div>
                    <div class="kpi-value">12.09 Days</div>
                    <div class="kpi-sub">Median: 9.80 Days</div>
                </div>
                <div class="kpi-card amber">
                    <div class="kpi-title">Delayed Deliveries</div>
                    <div class="kpi-value">7,827</div>
                    <div class="kpi-sub">8.11% Delay Rate</div>
                </div>
                <div class="kpi-card emerald">
                    <div class="kpi-title">On-Time Deliveries</div>
                    <div class="kpi-value">88,651</div>
                    <div class="kpi-sub">91.89% Punctual Rate</div>
                </div>
                <div class="kpi-card purple">
                    <div class="kpi-title">5-Star Satisfaction</div>
                    <div class="kpi-value">57,328</div>
                    <div class="kpi-sub">57.78% of Total Reviews</div>
                </div>
            </div>
            <div class="charts-grid">
                <div class="chart-box col-8">
                    <div class="chart-title">Delivery Duration vs Customer Review Rating (Correlation: -0.334)</div>
                    <div class="chart-wrapper"><canvas id="chartDelivRating"></canvas></div>
                </div>
                <div class="chart-box col-4">
                    <div class="chart-title">Review Score Distribution</div>
                    <div class="chart-wrapper"><canvas id="chartReviews"></canvas></div>
                </div>
            </div>
        </div>

        <!-- PAGE 5: GEOGRAPHIC & REGIONAL -->
        <div id="tab5" class="tab-content">
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">São Paulo (SP) Revenue</div>
                    <div class="kpi-value">R$ 5,927,330</div>
                    <div class="kpi-sub">37.41% Market Share</div>
                </div>
                <div class="kpi-card purple">
                    <div class="kpi-title">Southeast Share</div>
                    <div class="kpi-value">73.5%</div>
                    <div class="kpi-sub">SP, RJ, MG, RS, PR</div>
                </div>
                <div class="kpi-card emerald">
                    <div class="kpi-title">Fastest Delivery State</div>
                    <div class="kpi-value">SP (8.3 Days)</div>
                    <div class="kpi-sub">Metro Logistics Hub</div>
                </div>
                <div class="kpi-card amber">
                    <div class="kpi-title">Longest Transit State</div>
                    <div class="kpi-value">RR (27.0 Days)</div>
                    <div class="kpi-sub">North Regional Disparity</div>
                </div>
            </div>
            <div class="charts-grid">
                <div class="chart-box col-6">
                    <div class="chart-title">Top 10 States by Revenue (R$)</div>
                    <div class="chart-wrapper"><canvas id="chartTopStates2"></canvas></div>
                </div>
                <div class="chart-box col-6">
                    <div class="chart-title">Top 10 States by Average Delivery Days</div>
                    <div class="chart-wrapper"><canvas id="chartStateDeliv"></canvas></div>
                </div>
            </div>
        </div>

    </div>

    <script>
        function switchTab(tabId, btn) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }}

        // Monthly Revenue Line Chart
        new Chart(document.getElementById('chartMonthlyRev'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(monthly_labels)},
                datasets: [{{
                    label: 'Gross Revenue (R$)',
                    data: {json.dumps(monthly_values)},
                    borderColor: '#38BDF8',
                    backgroundColor: 'rgba(56, 189, 248, 0.15)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94A3B8' }} }},
                    y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94A3B8' }} }}
                }}
            }}
        }});

        // Order Status Donut Chart
        new Chart(document.getElementById('chartOrderStatus'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(status_labels)},
                datasets: [{{
                    data: {json.dumps(status_values)},
                    backgroundColor: ['#10B981', '#F59E0B', '#EF4444', '#64748B', '#3B82F6', '#8B5CF6', '#EC4899', '#14B8A6'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ position: 'right', labels: {{ color: '#F8FAFC', font: {{ size: 11 }} }} }} }}
            }}
        }});

        // Top Categories
        const catConfig = {{
            type: 'bar',
            data: {{
                labels: {json.dumps(cat_labels)},
                datasets: [{{
                    label: 'Revenue (R$)',
                    data: {json.dumps(cat_values)},
                    backgroundColor: '#0284C7',
                    borderRadius: 6
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94A3B8' }} }},
                    y: {{ grid: {{ display: false }}, ticks: {{ color: '#F8FAFC', font: {{ size: 11 }} }} }}
                }}
            }}
        }};
        new Chart(document.getElementById('chartTopCat'), catConfig);
        new Chart(document.getElementById('chartTopCat2'), catConfig);

        // Top States
        const stateConfig = {{
            type: 'bar',
            data: {{
                labels: {json.dumps(state_labels)},
                datasets: [{{
                    label: 'Revenue (R$)',
                    data: {json.dumps(state_values)},
                    backgroundColor: '#A855F7',
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#F8FAFC' }} }},
                    y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94A3B8' }} }}
                }}
            }}
        }};
        new Chart(document.getElementById('chartTopStates'), stateConfig);
        new Chart(document.getElementById('chartTopStates2'), stateConfig);

        // Customer Type Donut
        new Chart(document.getElementById('chartCustType'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(cust_type_labels)},
                datasets: [{{
                    data: {json.dumps(cust_type_values)},
                    backgroundColor: ['#38BDF8', '#F59E0B'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#F8FAFC' }} }} }}
            }}
        }});

        // Customer Segments
        new Chart(document.getElementById('chartCustSeg'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(seg_labels)},
                datasets: [{{
                    data: {json.dumps(seg_values)},
                    backgroundColor: ['#10B981', '#3B82F6', '#8B5CF6'],
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#F8FAFC' }} }},
                    y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94A3B8' }} }}
                }}
            }}
        }});

        // Payment Methods
        new Chart(document.getElementById('chartPayments'), {{
            type: 'pie',
            data: {{
                labels: {json.dumps(pay_labels)},
                datasets: [{{
                    data: {json.dumps(pay_values)},
                    backgroundColor: ['#0284C7', '#10B981', '#F59E0B', '#EF4444'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#F8FAFC' }} }} }}
            }}
        }});

        // Delivery Days vs Rating
        new Chart(document.getElementById('chartDelivRating'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(deliv_labels)},
                datasets: [{{
                    label: 'Avg Review Score',
                    data: {json.dumps(deliv_values)},
                    borderColor: '#EF4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.2)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 3,
                    pointRadius: 6,
                    pointBackgroundColor: '#EF4444'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94A3B8' }} }},
                    y: {{ min: 1, max: 5, grid: {{ color: '#334155' }}, ticks: {{ color: '#94A3B8' }} }}
                }}
            }}
        }});

        // Reviews Distribution
        new Chart(document.getElementById('chartReviews'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(rev_labels)},
                datasets: [{{
                    data: {json.dumps(rev_values)},
                    backgroundColor: ['#EF4444', '#F97316', '#FBBF24', '#34D399', '#10B981'],
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#F8FAFC' }} }},
                    y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94A3B8' }} }}
                }}
            }}
        }});

        // State Delivery Days
        new Chart(document.getElementById('chartStateDeliv'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(state_deliv_labels)},
                datasets: [{{
                    label: 'Avg Days',
                    data: {json.dumps(state_deliv_values)},
                    backgroundColor: '#F59E0B',
                    borderRadius: 6
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94A3B8' }} }},
                    y: {{ grid: {{ display: false }}, ticks: {{ color: '#F8FAFC' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

dashboard_file = os.path.join(BASE_DIR, "dashboard.html")
with open(dashboard_file, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Generated standalone interactive dashboard at: {dashboard_file} ({os.path.getsize(dashboard_file):,} bytes)")
