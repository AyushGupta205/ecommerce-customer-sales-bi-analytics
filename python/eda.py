"""
E-Commerce Data Analytics Pipeline - Exploratory Data Analysis (EDA) & Visuals
=============================================================================
Author: Senior Data Analyst & BI Developer
Project: E-Commerce Customer, Sales & Business Intelligence Analytics

This module computes statistical metrics and generates visual charts across
Executive KPIs, Sales, Customers, Geography, Delivery Performance, and Reviews.
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Styling configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'screenshots')


def format_currency(x, pos):
    if x >= 1e6:
        return f'R$ {x*1e-6:.1f}M'
    elif x >= 1e3:
        return f'R$ {x*1e-3:.0f}K'
    else:
        return f'R$ {x:.0f}'


def generate_executive_overview_visual(df_master, df_items_prod):
    """
    Renders Page 1: Executive Overview Dashboard Visual
    """
    fig = plt.figure(figsize=(16, 9), facecolor='#F4F6F9')
    gs = fig.add_gridspec(3, 3, height_ratios=[0.7, 1.2, 1.2], hspace=0.35, wspace=0.25)
    
    # Title Banner
    fig.text(0.05, 0.95, "EXECUTIVE OVERVIEW | E-COMMERCE BUSINESS INTELLIGENCE", fontsize=18, fontweight='bold', color='#1A202C')
    fig.text(0.05, 0.92, "High-Level Sales, Delivery Performance, Order Status & Customer KPIs (2016 - 2018)", fontsize=11, color='#718096')

    # KPI 1: Total Revenue
    tot_rev = df_master['total_order_revenue'].sum()
    ax_kpi1 = fig.add_subplot(gs[0, 0])
    ax_kpi1.axis('off')
    ax_kpi1.text(0.5, 0.65, f"R$ {tot_rev:,.2f}", ha='center', va='center', fontsize=18, fontweight='bold', color='#2B6CB0')
    ax_kpi1.text(0.5, 0.25, "TOTAL GROSS REVENUE\n(Product + Freight)", ha='center', va='center', fontsize=9, color='#4A5568')

    # KPI 2: Total Orders & AOV
    ax_kpi2 = fig.add_subplot(gs[0, 1])
    ax_kpi2.set_facecolor('#FFFFFF')
    tot_orders = df_master['order_id'].nunique()
    aov = tot_rev / tot_orders
    ax_kpi2.text(0.5, 0.65, f"{tot_orders:,} Orders | R$ {aov:.2f} AOV", ha='center', va='center', fontsize=15, fontweight='bold', color='#2D3748')
    ax_kpi2.text(0.5, 0.25, "TOTAL ORDERS & AVERAGE ORDER VALUE", ha='center', va='center', fontsize=9, color='#4A5568')
    ax_kpi2.axis('off')

    # KPI 3: Delivery Rate & Satisfaction
    ax_kpi3 = fig.add_subplot(gs[0, 2])
    ax_kpi3.set_facecolor('#FFFFFF')
    deliv_rate = (df_master['order_status'] == 'delivered').mean() * 100
    avg_score = df_master['review_score'].mean()
    ax_kpi3.text(0.5, 0.65, f"{deliv_rate:.1f}% Deliv | ★ {avg_score:.2f} / 5.0", ha='center', va='center', fontsize=15, fontweight='bold', color='#38A169')
    ax_kpi3.text(0.5, 0.25, "DELIVERY FULFILLMENT & AVG REVIEW SCORE", ha='center', va='center', fontsize=9, color='#4A5568')
    ax_kpi3.axis('off')

    # Chart 1: Monthly Revenue Trend
    ax1 = fig.add_subplot(gs[1, :2])
    monthly_rev = df_master.groupby('order_year_month')['total_order_revenue'].sum().reset_index()
    monthly_rev = monthly_rev[monthly_rev['order_year_month'] >= '2017-01']  # exclude early ramp-up
    ax1.plot(monthly_rev['order_year_month'], monthly_rev['total_order_revenue'], marker='o', color='#3182CE', linewidth=2.5, markersize=5)
    ax1.fill_between(monthly_rev['order_year_month'], monthly_rev['total_order_revenue'], color='#3182CE', alpha=0.1)
    ax1.set_title("Monthly Gross Revenue Trend (2017 - 2018)", fontsize=12, fontweight='bold', color='#2D3748', pad=10)
    ax1.set_xticklabels(monthly_rev['order_year_month'], rotation=45, ha='right', fontsize=8)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(format_currency))
    ax1.set_ylabel("Revenue (BRL)", fontsize=9)

    # Chart 2: Order Status Breakdown
    ax2 = fig.add_subplot(gs[1, 2])
    status_counts = df_master['order_status'].value_counts().head(4)
    colors = ['#38A169', '#E53E3E', '#DD6B20', '#3182CE']
    ax2.pie(status_counts, labels=status_counts.index.str.title(), autopct='%1.1f%%', colors=colors, startangle=140, 
            wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2))
    ax2.set_title("Order Status Distribution", fontsize=12, fontweight='bold', color='#2D3748')

    # Chart 3: Top 7 Categories by Revenue
    ax3 = fig.add_subplot(gs[2, :2])
    top_cat = df_items_prod.groupby('product_category_name_english')['revenue'].sum().nlargest(7).reset_index()
    sns.barplot(data=top_cat, y='product_category_name_english', x='revenue', ax=ax3, palette='Blues_r')
    ax3.set_title("Top 7 Product Categories by Gross Revenue", fontsize=12, fontweight='bold', color='#2D3748', pad=10)
    ax3.xaxis.set_major_formatter(ticker.FuncFormatter(format_currency))
    ax3.set_xlabel("Revenue (BRL)", fontsize=9)
    ax3.set_ylabel("")

    # Chart 4: Top 5 States by Revenue
    ax4 = fig.add_subplot(gs[2, 2])
    top_states = df_master.groupby('customer_state')['total_order_revenue'].sum().nlargest(5).reset_index()
    sns.barplot(data=top_states, x='customer_state', y='total_order_revenue', ax=ax4, palette='crest')
    ax4.set_title("Top 5 Customer States Revenue", fontsize=12, fontweight='bold', color='#2D3748', pad=10)
    ax4.yaxis.set_major_formatter(ticker.FuncFormatter(format_currency))
    ax4.set_xlabel("State", fontsize=9)
    ax4.set_ylabel("")

    plt.tight_layout(rect=[0.03, 0.02, 0.97, 0.90])
    out_path = os.path.join(SCREENSHOTS_DIR, 'executive_overview.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    logger.info("Saved: %s", out_path)


def generate_sales_product_visual(df_items_prod):
    """
    Renders Page 2: Sales & Product Analysis Visual
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 9), facecolor='#F4F6F9')
    fig.suptitle("SALES & PRODUCT INTELLIGENCE DASHBOARD", fontsize=18, fontweight='bold', color='#1A202C', y=0.96)
    
    # 1. Top 10 Categories by Revenue
    cat_summary = df_items_prod.groupby('product_category_name_english').agg(
        revenue=('revenue', 'sum'),
        items_sold=('order_item_id', 'count'),
        avg_price=('price', 'mean')
    ).reset_index()
    
    top10_cat = cat_summary.nlargest(10, 'revenue')
    sns.barplot(data=top10_cat, y='product_category_name_english', x='revenue', ax=axes[0, 0], palette='Blues_r')
    axes[0, 0].set_title("Top 10 Categories by Gross Revenue", fontsize=12, fontweight='bold')
    axes[0, 0].xaxis.set_major_formatter(ticker.FuncFormatter(format_currency))
    axes[0, 0].set_ylabel("")
    axes[0, 0].set_xlabel("Gross Revenue (BRL)")

    # 2. Volume vs Price (Top 15 Categories)
    top15_cat = cat_summary.nlargest(15, 'revenue')
    sns.scatterplot(data=top15_cat, x='items_sold', y='avg_price', size='revenue', sizes=(50, 400), 
                    hue='avg_price', palette='viridis', ax=axes[0, 1], legend=False)
    for _, row in top15_cat.head(6).iterrows():
        axes[0, 1].text(row['items_sold']+100, row['avg_price'], row['product_category_name_english'][:12], fontsize=8)
    axes[0, 1].set_title("Item Volume vs Average Item Price (Top Categories)", fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel("Total Items Sold")
    axes[0, 1].set_ylabel("Avg Item Price (BRL)")

    # 3. Freight Share by Top 8 Categories
    top8 = df_items_prod[df_items_prod['product_category_name_english'].isin(top10_cat['product_category_name_english'].head(8))]
    freight_comp = top8.groupby('product_category_name_english')[['price', 'freight_value']].sum().reset_index()
    freight_comp = freight_comp.melt(id_vars='product_category_name_english', value_vars=['price', 'freight_value'],
                                     var_name='Component', value_name='Value')
    freight_comp['Component'] = freight_comp['Component'].replace({'price': 'Product Price', 'freight_value': 'Freight Cost'})
    sns.barplot(data=freight_comp, y='product_category_name_english', x='Value', hue='Component', ax=axes[1, 0], palette=['#2B6CB0', '#ED8936'])
    axes[1, 0].set_title("Product Price vs Freight Cost Contribution", fontsize=12, fontweight='bold')
    axes[1, 0].xaxis.set_major_formatter(ticker.FuncFormatter(format_currency))
    axes[1, 0].set_ylabel("")
    axes[1, 0].set_xlabel("Total Value (BRL)")
    axes[1, 0].legend(loc='lower right')

    # 4. Item Price Distribution Boxplot
    sns.boxplot(data=top10_cat.head(6).merge(df_items_prod, on='product_category_name_english'), 
                y='product_category_name_english', x='price', ax=axes[1, 1], palette='Set2', showfliers=False)
    axes[1, 1].set_title("Price Distribution across Top 6 Categories (excl. extreme outliers)", fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel("Item Price (BRL)")
    axes[1, 1].set_ylabel("")

    plt.tight_layout(rect=[0.03, 0.03, 0.97, 0.93])
    out_path = os.path.join(SCREENSHOTS_DIR, 'sales_product_analysis.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    logger.info("Saved: %s", out_path)


def generate_customer_intelligence_visual(df_master, df_customers):
    """
    Renders Page 3: Customer Intelligence Visual
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 9), facecolor='#F4F6F9')
    fig.suptitle("CUSTOMER INTELLIGENCE & VALUE SEGMENTATION DASHBOARD", fontsize=18, fontweight='bold', color='#1A202C', y=0.96)
    
    # 1. New vs Repeat Customers Donut Chart
    cust_orders_count = df_customers.groupby('customer_unique_id')['customer_order_count'].first()
    repeat_counts = pd.Series([ (cust_orders_count == 1).sum(), (cust_orders_count > 1).sum() ], 
                              index=['One-Time Customer (96.9%)', 'Repeat Customer (3.1%)'])
    axes[0, 0].pie(repeat_counts, labels=repeat_counts.index, autopct='%1.1f%%', colors=['#4299E1', '#48BB78'],
                   startangle=140, wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2))
    axes[0, 0].set_title("Customer Retention Breakdown (New vs Repeat)", fontsize=12, fontweight='bold')

    # 2. Customer Value Segmentation (Spend Share vs Customer Share)
    seg_summary = df_customers.groupby('customer_value_segment', observed=False).agg(
        customer_count=('customer_unique_id', 'nunique'),
        total_spend=('customer_total_spend', 'sum')
    ).reset_index()
    seg_summary['Customer Share %'] = (seg_summary['customer_count'] / seg_summary['customer_count'].sum()) * 100
    seg_summary['Revenue Share %'] = (seg_summary['total_spend'] / seg_summary['total_spend'].sum()) * 100
    
    seg_melt = seg_summary.melt(id_vars='customer_value_segment', value_vars=['Customer Share %', 'Revenue Share %'],
                                var_name='Metric', value_name='Percentage')
    sns.barplot(data=seg_melt, x='customer_value_segment', y='Percentage', hue='Metric', ax=axes[0, 1], palette=['#4A5568', '#3182CE'])
    axes[0, 1].set_title("Customer Share vs Revenue Share by Value Segment", fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel("Percentage (%)")
    axes[0, 1].set_xlabel("Value Segment")
    axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=15)

    # 3. Top 10 Highest Spending Customers
    top_spenders = df_customers.sort_values('customer_total_spend', ascending=False).drop_duplicates('customer_unique_id').head(10)
    top_spenders['short_id'] = 'Cust ' + top_spenders['customer_unique_id'].str[:8]
    sns.barplot(data=top_spenders, y='short_id', x='customer_total_spend', ax=axes[1, 0], palette='crest_r')
    axes[1, 0].set_title("Top 10 Customers by Total Lifetime Spend", fontsize=12, fontweight='bold')
    axes[1, 0].xaxis.set_major_formatter(ticker.FuncFormatter(format_currency))
    axes[1, 0].set_xlabel("Lifetime Spend (BRL)")
    axes[1, 0].set_ylabel("Customer ID")

    # 4. Preferred Payment Types by Value Segment
    pay_dist = df_master.groupby(['customer_value_segment', 'primary_payment_type'], observed=False)['order_id'].count().reset_index()
    sns.barplot(data=pay_dist, x='customer_value_segment', y='order_id', hue='primary_payment_type', ax=axes[1, 1], palette='tab10')
    axes[1, 1].set_title("Payment Method Preference across Customer Value Tiers", fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel("Customer Value Segment")
    axes[1, 1].set_ylabel("Order Count")
    axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=15)
    axes[1, 1].legend(title="Payment Type", loc='upper left')

    plt.tight_layout(rect=[0.03, 0.03, 0.97, 0.93])
    out_path = os.path.join(SCREENSHOTS_DIR, 'customer_intelligence.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    logger.info("Saved: %s", out_path)


def generate_delivery_experience_visual(df_master):
    """
    Renders Page 4: Delivery & Customer Experience Dashboard Visual
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 9), facecolor='#F4F6F9')
    fig.suptitle("DELIVERY LOGISTICS & CUSTOMER SATISFACTION DASHBOARD", fontsize=18, fontweight='bold', color='#1A202C', y=0.96)
    
    deliv_orders = df_master[df_master['order_status'] == 'delivered'].copy()
    
    # 1. Delivery Time vs Average Review Score
    deliv_orders['delivery_bracket'] = pd.cut(
        deliv_orders['delivery_days'],
        bins=[0, 5, 10, 15, 20, 30, 60, 200],
        labels=['0-5 Days', '6-10 Days', '11-15 Days', '16-20 Days', '21-30 Days', '31-60 Days', '60+ Days']
    )
    bracket_score = deliv_orders.groupby('delivery_bracket', observed=False)['review_score'].mean().reset_index()
    sns.barplot(data=bracket_score, x='delivery_bracket', y='review_score', ax=axes[0, 0], palette='RdYlGn')
    axes[0, 0].set_title("Average Customer Review Score by Delivery Duration", fontsize=12, fontweight='bold')
    axes[0, 0].set_ylim(1, 5)
    axes[0, 0].set_ylabel("Average Review Rating (1-5)")
    axes[0, 0].set_xlabel("Delivery Time (Days)")
    for p in axes[0, 0].patches:
        axes[0, 0].annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height() - 0.4),
                            ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    # 2. Overall Review Score Distribution
    score_counts = df_master['review_score'].dropna().value_counts().sort_index(ascending=False).reset_index()
    score_counts.columns = ['Score', 'Count']
    score_counts['Pct'] = (score_counts['Count'] / score_counts['Count'].sum()) * 100
    sns.barplot(data=score_counts, x='Score', y='Pct', ax=axes[0, 1], palette='Blues_r')
    axes[0, 1].set_title("Customer Review Score Distribution (% of total reviews)", fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel("Star Rating")
    axes[0, 1].set_ylabel("Percentage (%)")
    for p in axes[0, 1].patches:
        axes[0, 1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1),
                            ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 3. Monthly Average Delivery Duration Trend
    monthly_deliv = deliv_orders.groupby('order_year_month')['delivery_days'].mean().reset_index()
    monthly_deliv = monthly_deliv[monthly_deliv['order_year_month'] >= '2017-01']
    axes[1, 0].plot(monthly_deliv['order_year_month'], monthly_deliv['delivery_days'], marker='s', color='#E53E3E', linewidth=2.5)
    axes[1, 0].axhline(deliv_orders['delivery_days'].mean(), color='gray', linestyle='--', label=f"Average ({deliv_orders['delivery_days'].mean():.1f} d)")
    axes[1, 0].set_title("Monthly Average Delivery Lead Time (Days)", fontsize=12, fontweight='bold')
    axes[1, 0].set_xticklabels(monthly_deliv['order_year_month'], rotation=45, ha='right', fontsize=8)
    axes[1, 0].set_ylabel("Delivery Days")
    axes[1, 0].legend()

    # 4. On-Time vs Delayed Delivery vs Review Score
    delay_review = deliv_orders.groupby('is_delayed').agg(
        avg_review=('review_score', 'mean'),
        pct_5_star=('review_score', lambda x: (x == 5).mean() * 100),
        pct_1_star=('review_score', lambda x: (x == 1).mean() * 100)
    ).reset_index()
    delay_review['Status'] = delay_review['is_delayed'].replace({0: 'On-Time / Early', 1: 'Delayed vs Estimate'})
    
    delay_melt = delay_review.melt(id_vars='Status', value_vars=['pct_5_star', 'pct_1_star'], var_name='Rating Tier', value_name='Pct')
    delay_melt['Rating Tier'] = delay_melt['Rating Tier'].replace({'pct_5_star': '5-Star Reviews %', 'pct_1_star': '1-Star Reviews %'})
    sns.barplot(data=delay_melt, x='Status', y='Pct', hue='Rating Tier', ax=axes[1, 1], palette=['#48BB78', '#E53E3E'])
    axes[1, 1].set_title("Satisfaction Impact: On-Time vs Delayed Deliveries", fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel("Percentage of Reviews (%)")
    axes[1, 1].set_xlabel("")

    plt.tight_layout(rect=[0.03, 0.03, 0.97, 0.93])
    out_path = os.path.join(SCREENSHOTS_DIR, 'delivery_customer_experience.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    logger.info("Saved: %s", out_path)


def generate_geographic_visual(df_master):
    """
    Renders Page 5: Geographic & Regional Analysis Visual
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 9), facecolor='#F4F6F9')
    fig.suptitle("GEOGRAPHIC & REGIONAL PERFORMANCE DASHBOARD", fontsize=18, fontweight='bold', color='#1A202C', y=0.96)
    
    state_agg = df_master.groupby('customer_state').agg(
        orders=('order_id', 'nunique'),
        revenue=('total_order_revenue', 'sum'),
        avg_delivery_days=('delivery_days', 'mean'),
        avg_review=('review_score', 'mean')
    ).reset_index()
    state_agg['aov'] = state_agg['revenue'] / state_agg['orders']
    
    # 1. Top 10 States by Order Volume
    top10_orders = state_agg.nlargest(10, 'orders')
    sns.barplot(data=top10_orders, y='customer_state', x='orders', ax=axes[0, 0], palette='Blues_r')
    axes[0, 0].set_title("Top 10 Brazilian States by Order Volume", fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel("Order Count")
    axes[0, 0].set_ylabel("State")

    # 2. Average Order Value (AOV) across Top 10 States
    top10_aov = state_agg[state_agg['orders'] >= 500].nlargest(10, 'aov')
    sns.barplot(data=top10_aov, y='customer_state', x='aov', ax=axes[0, 1], palette='crest')
    axes[0, 1].set_title("Highest Average Order Value (AOV) by State (Min 500 Orders)", fontsize=12, fontweight='bold')
    axes[0, 1].xaxis.set_major_formatter(ticker.FuncFormatter(format_currency))
    axes[0, 1].set_xlabel("AOV (BRL)")
    axes[0, 1].set_ylabel("State")

    # 3. Delivery Lead Time across States (Fastest vs Slowest)
    extreme_states = pd.concat([state_agg[state_agg['orders'] >= 100].nsmallest(5, 'avg_delivery_days'),
                                state_agg[state_agg['orders'] >= 100].nlargest(5, 'avg_delivery_days')]).drop_duplicates()
    extreme_states = extreme_states.sort_values('avg_delivery_days')
    sns.barplot(data=extreme_states, y='customer_state', x='avg_delivery_days', ax=axes[1, 0], palette='RdYlGn_r')
    axes[1, 0].set_title("Average Delivery Days by State (Fastest vs Slowest)", fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel("Avg Delivery Days")
    axes[1, 0].set_ylabel("State")

    # 4. Regional Revenue Concentration
    top5_rev = state_agg.nlargest(5, 'revenue')
    other_rev = state_agg['revenue'].sum() - top5_rev['revenue'].sum()
    rev_pie_data = pd.concat([top5_rev[['customer_state', 'revenue']], 
                              pd.DataFrame([{'customer_state': 'Other 22 States', 'revenue': other_rev}])])
    axes[1, 1].pie(rev_pie_data['revenue'], labels=rev_pie_data['customer_state'], autopct='%1.1f%%',
                   colors=sns.color_palette('tab10', len(rev_pie_data)), startangle=140,
                   wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2))
    axes[1, 1].set_title("Gross Revenue Concentration (Top 5 States vs Others)", fontsize=12, fontweight='bold')

    plt.tight_layout(rect=[0.03, 0.03, 0.97, 0.93])
    out_path = os.path.join(SCREENSHOTS_DIR, 'geographic_analysis.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    logger.info("Saved: %s", out_path)


def run_all_eda():
    logger.info("Starting Full EDA Execution and Visualization Export...")
    df_master = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'analytics_master_orders.csv'))
    df_items = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'fact_order_items_clean.csv'))
    df_products = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_products_clean.csv'))
    df_customers = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'dim_customers_clean.csv'))
    
    df_items_prod = df_items.merge(df_products[['product_id', 'product_category_name_english']], on='product_id', how='left')

    generate_executive_overview_visual(df_master, df_items_prod)
    generate_sales_product_visual(df_items_prod)
    generate_customer_intelligence_visual(df_master, df_customers)
    generate_delivery_experience_visual(df_master)
    generate_geographic_visual(df_master)
    
    logger.info("All 5 dashboard visualization screenshots generated successfully.")


if __name__ == '__main__':
    run_all_eda()
