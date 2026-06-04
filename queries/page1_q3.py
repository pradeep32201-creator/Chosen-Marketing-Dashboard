import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """

SELECT
    utm_source,
    COUNT(DISTINCT order_id)        AS total_orders,
    ROUND(SUM(revenue), 2)          AS total_revenue,
    ROUND(SUM(revenue) * 100.0 / 
         (SELECT SUM(revenue) 
          FROM shopify_orders), 2)  AS revenue_pct
FROM shopify_orders
GROUP BY utm_source
ORDER BY total_revenue DESC

"""

df = pd.read_sql(query, conn)
print(df.to_string())