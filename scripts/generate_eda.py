import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

def main():
    # Setup directories
    os.makedirs('visualizations', exist_ok=True)
    os.makedirs('notebooks', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    print("Loading datasets...")
    # Load timeseries data for faster trend analysis
    df_ts = pd.read_csv('Dataset/processed/inventory_timeseries.csv', sep=';')
    df_ts.columns = df_ts.columns.str.strip()
    
    # Handle sales_idr if it has 'Rp' format
    if df_ts['sales_idr'].dtype == 'O':
        df_ts['sales_idr'] = df_ts['sales_idr'].str.replace('Rp', '', regex=False).str.replace('.', '', regex=False).str.strip().astype(float)
    
    # Dates are in DD/MM/YYYY format
    df_ts['date'] = pd.to_datetime(df_ts['date'], format='%d/%m/%Y')
    
    # Load product dictionary
    df_prod = pd.read_csv('Dataset/processed/product_dictionary.csv', sep=';')
    
    # Load a sample of clean data for current_stock analysis
    # To save memory and time, we'll use the timeseries for sales analysis
    df_clean = pd.read_csv('Dataset/processed/inventory_clean.csv', sep=';', usecols=['product_name', 'current_stock', 'reorder_point', 'recommended_restock'])
    
    # Set plot style
    sns.set_theme(style="whitegrid")
    
    findings = {}

    print("Generating Q1: Top Selling Products...")
    top_selling = df_ts.groupby('product_name')['sales_idr'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_selling.values, y=top_selling.index, palette="viridis")
    plt.title('Top 10 Products by Total Sales (IDR)', fontsize=14)
    plt.xlabel('Total Sales (IDR)')
    plt.ylabel('Product')
    plt.tight_layout()
    plt.savefig('visualizations/top_selling_products.png')
    plt.close()
    findings['top_selling'] = top_selling.index.tolist()

    print("Generating Q2: Slow-Moving Products...")
    slow_moving = df_ts.groupby('product_name')['quantity_sold'].sum().sort_values(ascending=True).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=slow_moving.values, y=slow_moving.index, palette="magma")
    plt.title('Top 10 Slow-Moving Products by Quantity Sold', fontsize=14)
    plt.xlabel('Quantity Sold')
    plt.ylabel('Product')
    plt.tight_layout()
    plt.savefig('visualizations/slow_moving_products.png')
    plt.close()
    findings['slow_moving'] = slow_moving.index.tolist()

    print("Generating Q3: Sales Trends...")
    daily_sales = df_ts.groupby('date')['sales_idr'].sum().reset_index()
    # Group by month for a smoother trend line
    monthly_sales = daily_sales.set_index('date').resample('ME').sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_sales, x='date', y='sales_idr', marker='o', color='b')
    plt.title('Monthly Sales Trend (IDR)', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Total Sales (IDR)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualizations/sales_trend.png')
    plt.close()

    print("Generating Q4 & Q5: Stock Movement & Risks...")
    # Calculate average current stock vs reorder point per product
    stock_analysis = df_clean.groupby('product_name').agg({
        'current_stock': 'mean',
        'reorder_point': 'mean',
        'recommended_restock': 'sum'
    }).sort_values('recommended_restock', ascending=False).head(15)
    
    plt.figure(figsize=(12, 6))
    x = range(len(stock_analysis))
    width = 0.35
    plt.bar([i - width/2 for i in x], stock_analysis['current_stock'], width, label='Avg Current Stock', color='skyblue')
    plt.bar([i + width/2 for i in x], stock_analysis['reorder_point'], width, label='Reorder Point', color='salmon')
    plt.title('Stock Levels vs Reorder Point (Top 15 Most Restocked)', fontsize=14)
    plt.xlabel('Product')
    plt.ylabel('Quantity')
    plt.xticks(x, stock_analysis.index, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig('visualizations/stock_movement.png')
    plt.close()

    # Restock recommendation chart
    plt.figure(figsize=(10, 6))
    top_restock = stock_analysis['recommended_restock'].sort_values(ascending=False).head(10)
    sns.barplot(x=top_restock.values, y=top_restock.index, palette="Reds_r")
    plt.title('Top 10 Products Needing Most Restock (Cumulative)', fontsize=14)
    plt.xlabel('Total Recommended Restock Quantity')
    plt.ylabel('Product')
    plt.tight_layout()
    plt.savefig('visualizations/restock_recommendation.png')
    plt.close()

    print("Generating Jupyter Notebook...")
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Exploratory Data Analysis (EDA) - Smart Inventory Forecasting\n",
                    "This notebook contains the EDA for the preprocessed inventory dataset, focusing on top-selling items, slow-moving items, sales trends, and stock risks."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "import warnings\n",
                    "warnings.filterwarnings('ignore')\n",
                    "\n",
                    "# Set plotting style\n",
                    "sns.set_theme(style='whitegrid')\n",
                    "plt.rcParams['figure.figsize'] = (10, 6)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Load Data\n",
                    "We will load the aggregated timeseries dataset for trend analysis and a sample of the granular clean dataset for stock level analysis."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 2,
                "metadata": {},
                "outputs": [],
                "source": [
                    "df_ts = pd.read_csv('../Dataset/processed/inventory_timeseries.csv')\n",
                    "df_ts['date'] = pd.to_datetime(df_ts['date'])\n",
                    "\n",
                    "df_clean = pd.read_csv('../Dataset/processed/inventory_clean.csv', usecols=['product_name', 'current_stock', 'reorder_point', 'recommended_restock'])\n",
                    "df_ts.head()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Top-Selling Products (Revenue)\n",
                    "Identifying which products bring in the most revenue."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 3,
                "metadata": {},
                "outputs": [],
                "source": [
                    "top_selling = df_ts.groupby('product_name')['sales_idr'].sum().sort_values(ascending=False).head(10)\n",
                    "plt.figure(figsize=(10, 6))\n",
                    "sns.barplot(x=top_selling.values, y=top_selling.index, palette=\"viridis\")\n",
                    "plt.title('Top 10 Products by Total Sales (IDR)')\n",
                    "plt.xlabel('Total Sales (IDR)')\n",
                    "plt.ylabel('Product')\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Slow-Moving Products (Quantity Sold)\n",
                    "Identifying products with the lowest sales volume to avoid overstocking."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 4,
                "metadata": {},
                "outputs": [],
                "source": [
                    "slow_moving = df_ts.groupby('product_name')['quantity_sold'].sum().sort_values(ascending=True).head(10)\n",
                    "plt.figure(figsize=(10, 6))\n",
                    "sns.barplot(x=slow_moving.values, y=slow_moving.index, palette=\"magma\")\n",
                    "plt.title('Top 10 Slow-Moving Products by Quantity Sold')\n",
                    "plt.xlabel('Quantity Sold')\n",
                    "plt.ylabel('Product')\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 4. Sales Trends Over Time\n",
                    "Analyzing monthly sales trends to identify seasonality or growth."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 5,
                "metadata": {},
                "outputs": [],
                "source": [
                    "daily_sales = df_ts.groupby('date')['sales_idr'].sum().reset_index()\n",
                    "monthly_sales = daily_sales.set_index('date').resample('ME').sum().reset_index()\n",
                    "plt.figure(figsize=(12, 6))\n",
                    "sns.lineplot(data=monthly_sales, x='date', y='sales_idr', marker='o', color='b')\n",
                    "plt.title('Monthly Sales Trend (IDR)')\n",
                    "plt.xlabel('Date')\n",
                    "plt.ylabel('Total Sales (IDR)')\n",
                    "plt.xticks(rotation=45)\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 5. Stock Movement and Risk Analysis\n",
                    "Comparing average current stock with reorder points to identify items prone to understocking."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 6,
                "metadata": {},
                "outputs": [],
                "source": [
                    "stock_analysis = df_clean.groupby('product_name').agg({\n",
                    "    'current_stock': 'mean',\n",
                    "    'reorder_point': 'mean',\n",
                    "    'recommended_restock': 'sum'\n",
                    "}).sort_values('recommended_restock', ascending=False).head(15)\n",
                    "\n",
                    "plt.figure(figsize=(12, 6))\n",
                    "x = range(len(stock_analysis))\n",
                    "width = 0.35\n",
                    "plt.bar([i - width/2 for i in x], stock_analysis['current_stock'], width, label='Avg Current Stock', color='skyblue')\n",
                    "plt.bar([i + width/2 for i in x], stock_analysis['reorder_point'], width, label='Reorder Point', color='salmon')\n",
                    "plt.title('Stock Levels vs Reorder Point (Top 15 Most Restocked)')\n",
                    "plt.xlabel('Product')\n",
                    "plt.ylabel('Quantity')\n",
                    "plt.xticks(x, stock_analysis.index, rotation=45, ha='right')\n",
                    "plt.legend()\n",
                    "plt.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open('notebooks/eda_inventory_analysis.ipynb', 'w') as f:
        json.dump(notebook_content, f, indent=2)

    # Save findings for markdown report writing later
    with open('reports/findings.json', 'w') as f:
        json.dump(findings, f)

    print("EDA generation complete. Notebook and visualizations created.")

if __name__ == "__main__":
    main()
