import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')


query = """
SELECT
    date,
    COUNT(DISTINCT order_id)                        AS total_orders,
    ROUND(SUM(revenue), 2)                          AS daily_revenue,
    ROUND(SUM(revenue) / 
          COUNT(DISTINCT order_id), 2)              AS daily_aov
FROM shopify_orders
GROUP BY date
ORDER BY date
"""

df = pd.read_sql(query, conn)
print("--- Orders Over Time ---")
print(df.head(10).to_string())