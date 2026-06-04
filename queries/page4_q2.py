import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')


query = """
SELECT
    product,
    COUNT(DISTINCT order_id)                        AS total_orders,
    SUM(quantity)                                   AS total_units,
    ROUND(SUM(revenue), 2)                          AS total_revenue,
    ROUND(SUM(revenue) / 
          COUNT(DISTINCT order_id), 2)              AS avg_order_value,
    ROUND(SUM(revenue) * 100.0 / 
         (SELECT SUM(revenue) 
          FROM shopify_orders), 2)                  AS revenue_pct
FROM shopify_orders
GROUP BY product
ORDER BY total_revenue DESC
"""

df = pd.read_sql(query, conn)
print("--- Revenue by Product ---")
print(df.to_string())