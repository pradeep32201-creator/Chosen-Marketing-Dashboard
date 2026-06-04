import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    city,
    COUNT(DISTINCT order_id)                        AS total_orders,
    ROUND(SUM(revenue), 2)                          AS total_revenue,
    ROUND(SUM(revenue) / 
          COUNT(DISTINCT order_id), 2)              AS avg_order_value,
    ROUND(SUM(revenue) * 100.0 / 
         (SELECT SUM(revenue) 
          FROM shopify_orders), 2)                  AS revenue_pct
FROM shopify_orders
GROUP BY city
ORDER BY total_revenue DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)
print("--- Revenue by City Top 10 ---")
print(df.to_string())