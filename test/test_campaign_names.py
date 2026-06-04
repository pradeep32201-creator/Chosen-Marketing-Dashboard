import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

print("\n--- google_ads campaigns ---")
df = pd.read_sql("SELECT DISTINCT campaign_name FROM google_ads", conn)
print(df)

print("\n--- meta_ads campaigns ---")
df = pd.read_sql("SELECT DISTINCT campaign_name FROM meta_ads", conn)
print(df)

print("\n--- shopify_orders utm_campaign ---")
df = pd.read_sql("SELECT DISTINCT utm_campaign FROM shopify_orders", conn)
print(df)