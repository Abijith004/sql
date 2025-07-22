import sqlite3
import pandas as pd
import os

# Ensure 'data' folder exists
data_path = 'data'
db_path = 'sample.db'

# Load CSVs
customers_df = pd.read_csv(os.path.join(data_path, 'customers.csv'))
orders_df = pd.read_csv(os.path.join(data_path, 'orders.csv'))
products_df = pd.read_csv(os.path.join(data_path, 'products.csv'))

# Create SQLite DB
conn = sqlite3.connect(db_path)

# Write tables
customers_df.to_sql('customers', conn, if_exists='replace', index=False)
orders_df.to_sql('orders', conn, if_exists='replace', index=False)
products_df.to_sql('products', conn, if_exists='replace', index=False)

print(f"✅ Data loaded into {db_path}")
conn.close()
