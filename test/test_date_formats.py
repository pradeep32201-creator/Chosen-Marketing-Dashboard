import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

for table, col in [('google_ads','date'), ('meta_ads','date'), 
                   ('shopify_sessions','session_date'), ('shopify_orders','date')]:
    df = pd.read_sql(f"SELECT DISTINCT {col} FROM {table} LIMIT 5", conn)
    print(f"\n{table} - {col}:")
    print(df.values.tolist())