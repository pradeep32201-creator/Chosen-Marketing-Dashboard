import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')


query = """
SELECT
    'Google' AS channel,
    ROUND(AVG(g.roas), 2)                   AS platform_reported_roas,
    ROUND(SUM(o.revenue) / SUM(g.spend), 2) AS actual_roas
FROM google_ads g
LEFT JOIN shopify_orders o
    ON g.date = o.date
    AND o.utm_source = 'google'

UNION ALL

SELECT
    'Meta' AS channel,
    ROUND(AVG(m.roas), 2)                   AS platform_reported_roas,
    ROUND(SUM(o.revenue) / SUM(m.spend), 2) AS actual_roas
FROM meta_ads m
LEFT JOIN shopify_orders o
    ON m.date = o.date
    AND o.utm_source = 'meta'
"""

df = pd.read_sql(query, conn)
print("--- Platform ROAS vs Actual ROAS ---")
print(df.to_string())