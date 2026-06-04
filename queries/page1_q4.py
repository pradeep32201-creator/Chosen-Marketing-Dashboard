import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """


SELECT
    device,
    COUNT(DISTINCT order_id)        AS total_orders,
    ROUND(SUM(revenue), 2)          AS total_revenue,
    ROUND(SUM(revenue) / 
          COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM shopify_orders
GROUP BY device
ORDER BY total_revenue DESC

"""

df = pd.read_sql(query, conn)
print(df.to_string())