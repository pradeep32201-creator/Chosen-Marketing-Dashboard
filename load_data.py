import pandas as pd
import sqlite3

conn = sqlite3.connect('marketing_dashboard.db')

pd.read_csv('google_ads.csv').to_sql('google_ads', conn, if_exists='append', index=False)
pd.read_csv('meta_ads.csv').to_sql('meta_ads', conn, if_exists='append', index=False)
pd.read_csv('shopify_sessions.csv').to_sql('shopify_sessions', conn, if_exists='append', index=False)
pd.read_csv('shopify_orders.csv').to_sql('shopify_orders', conn, if_exists='append', index=False)