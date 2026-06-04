import pandas as pd
import sqlite3

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    'Sessions to Cart'          AS funnel_stage,
    ROUND((1 - SUM(added_to_cart) * 1.0 /
          COUNT(*)) * 100, 2)   AS dropoff_pct
FROM shopify_sessions

UNION ALL

SELECT
    'Cart to Checkout'          AS funnel_stage,
    ROUND((1 - SUM(reached_checkout) * 1.0 /
          SUM(added_to_cart)) * 100, 2) AS dropoff_pct
FROM shopify_sessions

UNION ALL

SELECT
    'Checkout to Purchase'      AS funnel_stage,
    ROUND((1 - SUM(purchased) * 1.0 /
          SUM(reached_checkout)) * 100, 2) AS dropoff_pct
FROM shopify_sessions
"""

df = pd.read_sql(query, conn)
print("--- Drop Off Rates ---")
print(df.to_string())