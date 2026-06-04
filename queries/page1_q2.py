import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    o.date,
    ROUND(SUM(o.revenue), 2)                        AS daily_revenue,
    ROUND(COALESCE(g.daily_spend, 0) + 
          COALESCE(m.daily_spend, 0), 2)             AS daily_spend
FROM shopify_orders o
LEFT JOIN (
    SELECT date, SUM(spend) AS daily_spend 
    FROM google_ads 
    GROUP BY date
) g ON o.date = g.date
LEFT JOIN (
    SELECT date, SUM(spend) AS daily_spend 
    FROM meta_ads 
    GROUP BY date
) m ON o.date = m.date
GROUP BY o.date
ORDER BY o.date

"""

df = pd.read_sql(query, conn)
print(df.to_string())