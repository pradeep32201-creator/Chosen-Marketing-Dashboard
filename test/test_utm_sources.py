import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

print("\n--- shopify_orders utm_source ---")
df = pd.read_sql("SELECT DISTINCT utm_source, COUNT(*) as count FROM shopify_orders GROUP BY utm_source", conn)
print(df)

print("\n--- shopify_sessions utm_source ---")
df = pd.read_sql("SELECT DISTINCT utm_source, COUNT(*) as count FROM shopify_sessions GROUP BY utm_source", conn)
print(df)