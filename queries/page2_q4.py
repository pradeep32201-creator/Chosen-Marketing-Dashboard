import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    g.date,
    ROUND(SUM(g.spend), 2)  AS google_spend,
    ROUND(SUM(m.spend), 2)  AS meta_spend
FROM google_ads g
LEFT JOIN meta_ads m ON g.date = m.date
GROUP BY g.date
ORDER BY g.date
"""

df = pd.read_sql(query, conn)
print("--- Daily Spend by Channel ---")
print(df.head(10).to_string())