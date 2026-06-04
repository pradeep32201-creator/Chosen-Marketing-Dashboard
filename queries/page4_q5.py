import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    utm_source,
    COUNT(DISTINCT order_id)                        AS total_orders,
    ROUND(SUM(revenue), 2)                          AS total_revenue,
    ROUND(SUM(revenue) / 
          COUNT(DISTINCT order_id), 2)              AS avg_order_value,
    ROUND(MAX(revenue), 2)                          AS max_order_value,
    ROUND(MIN(revenue), 2)                          AS min_order_value
FROM shopify_orders
GROUP BY utm_source
ORDER BY avg_order_value DESC
"""

df = pd.read_sql(query, conn)
print("--- AOV by UTM Source ---")
print(df.to_string())