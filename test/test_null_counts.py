import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')


print("\n--- Null Counts ---")
queries = {
    "google_ads spend nulls": "SELECT COUNT(*) FROM google_ads WHERE spend IS NULL",
    "meta_ads spend nulls": "SELECT COUNT(*) FROM meta_ads WHERE spend IS NULL",
    "shopify_orders revenue nulls": "SELECT COUNT(*) FROM shopify_orders WHERE revenue IS NULL",
    "shopify_orders utm_campaign nulls": "SELECT COUNT(*) FROM shopify_orders WHERE utm_campaign IS NULL",
    "shopify_sessions utm_campaign nulls": "SELECT COUNT(*) FROM shopify_sessions WHERE utm_campaign IS NULL",
}
for label, q in queries.items():
    result = pd.read_sql(q, conn).values[0][0]
    print(f"{label}: {result}")