import pandas as pd
import numpy as np
import os
import uuid

def main():
    input_file = "Dataset/Retail_Transactions_Dataset.csv"
    output_dir = "Dataset/processed"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Loading dataset...")
    # Load only necessary columns to save memory
    usecols = ['Transaction_ID', 'Date', 'Product']
    try:
        df = pd.read_csv(input_file, sep=';', usecols=usecols)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return
    
    print(f"Initial shape: {df.shape}")
    
    # Standardize dates
    print("Standardizing dates...")
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M').dt.date

    # Explode products
    print("Exploding products...")
    # Product looks like "['Ketchup', 'Shaving Cream', 'Light Bulbs']"
    # Remove brackets and single quotes, then split
    df['Product'] = df['Product'].str.strip("[]").str.replace("'", "").str.split(", ")
    df = df.explode('Product')
    df = df.rename(columns={
        'Transaction_ID': 'transaction_id',
        'Date': 'date',
        'Product': 'product_name'
    })
    
    # Remove any leading/trailing whitespace
    df['product_name'] = df['product_name'].str.strip()
    
    # Master Product Data
    print("Generating product dictionary...")
    unique_products = df['product_name'].dropna().unique()
    
    product_dict = []
    
    # Let's define some simple mappings or randomize
    # I'll create a reproducible random generator
    np.random.seed(42)
    
    categories = ['Food & Beverage', 'Household', 'Personal Care', 'Electronics', 'Clothing']
    
    for prod in unique_products:
        prod_id = "PRD-" + str(uuid.uuid4())[:8].upper()
        # assign random category
        cat = np.random.choice(categories)
        # assign random price between 5000 and 150000 in multiples of 500
        price = np.random.randint(10, 301) * 500
        # assign reorder point between 20 and 100
        reorder_point = np.random.randint(20, 101)
        
        product_dict.append({
            'product_name': prod,
            'product_id': prod_id,
            'category': cat,
            'price_idr': price,
            'reorder_point': reorder_point
        })
        
    df_products = pd.DataFrame(product_dict)
    
    # Merge back to transactions
    print("Merging data and calculating synthetic metrics...")
    df = df.merge(df_products, on='product_name', how='left')
    
    # Drop rows without product_id if any
    df = df.dropna(subset=['product_id'])
    
    # Generate quantity_sold
    df['quantity_sold'] = np.random.randint(1, 15, size=len(df))
    df['sales_idr'] = df['quantity_sold'] * df['price_idr']
    
    # Generate dummy inventory logic
    # Assume stock_out is quantity_sold
    df['stock_out'] = df['quantity_sold']
    
    # Random stock_in
    # Usually stock_in doesn't happen every transaction, let's just make it 0 most times, and sometimes random amount
    df['stock_in'] = np.where(np.random.random(size=len(df)) < 0.05, np.random.randint(20, 100, size=len(df)), 0)
    
    # Random current_stock
    df['current_stock'] = np.random.randint(10, 150, size=len(df))
    
    # Calculate recommended restock
    # if current_stock < reorder_point, then reorder_point * 2 - current_stock
    df['recommended_restock'] = np.where(
        df['current_stock'] < df['reorder_point'],
        (df['reorder_point'] * 2) - df['current_stock'],
        0
    )
    
    # Reorder and select final columns
    final_cols = [
        'date', 'transaction_id', 'product_id', 'product_name', 'category', 
        'quantity_sold', 'price_idr', 'sales_idr', 
        'stock_in', 'stock_out', 'current_stock', 'reorder_point', 'recommended_restock'
    ]
    df_clean = df[final_cols]
    
    # Save clean granular data
    print("Saving inventory_clean.csv...")
    df_clean.to_csv(os.path.join(output_dir, 'inventory_clean.csv'), index=False)
    
    # Create timeseries aggregation
    print("Creating timeseries dataset...")
    df_timeseries = df_clean.groupby(['date', 'product_id', 'product_name', 'category']).agg({
        'quantity_sold': 'sum',
        'sales_idr': 'sum',
        'stock_in': 'sum',
        'stock_out': 'sum',
        'price_idr': 'first',
        'reorder_point': 'first'
    }).reset_index()
    
    df_timeseries.to_csv(os.path.join(output_dir, 'inventory_timeseries.csv'), index=False)
    
    # Save product dictionary
    print("Saving product_dictionary.csv...")
    df_products.to_csv(os.path.join(output_dir, 'product_dictionary.csv'), index=False)
    
    print("Data Wrangling Completed Successfully!")

if __name__ == "__main__":
    main()
