import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    COUNT(DISTINCT order_id)               AS total_orders,
    ROUND(SUM(revenue), 2)                 AS total_revenue,
    ROUND(SUM(revenue) /
          COUNT(DISTINCT order_id), 2)     AS avg_order_value,
    SUM(quantity)                          AS total_units_sold,
    ROUND(SUM(revenue) / SUM(quantity), 2) AS avg_revenue_per_unit
FROM shopify_orders
WHERE order_id IS NOT NULL
AND revenue IS NOT NULL
"""

df = pd.read_sql(query, conn)
print("--- Order KPI Cards ---")
print(df.to_string())