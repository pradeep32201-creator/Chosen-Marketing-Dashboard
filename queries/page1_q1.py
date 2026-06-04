import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    ROUND(SUM(o.revenue), 2)                        AS total_revenue,
    ROUND(SUM(g.spend) + SUM(m.spend), 2)           AS total_spend,
    ROUND(SUM(o.revenue) / 
         (SUM(g.spend) + SUM(m.spend)), 2)          AS blended_roas,
    COUNT(DISTINCT o.order_id)                       AS total_orders,
    ROUND(SUM(o.revenue) / 
          COUNT(DISTINCT o.order_id), 2)             AS avg_order_value,
    ROUND(CAST(SUM(s.purchased) AS FLOAT) / 
          CAST(SUM(s.added_to_cart) AS FLOAT), 4)   AS overall_cvr
FROM shopify_orders o
CROSS JOIN (SELECT SUM(spend) AS spend FROM google_ads) g
CROSS JOIN (SELECT SUM(spend) AS spend FROM meta_ads) m
CROSS JOIN (SELECT 
                SUM(purchased) AS purchased,
                SUM(added_to_cart) AS added_to_cart 
            FROM shopify_sessions) s
"""

df = pd.read_sql(query, conn)
print(df.to_string())