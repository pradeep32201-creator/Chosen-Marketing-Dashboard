import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    'Google'                                AS channel,
    campaign_name,
    ROUND(SUM(spend), 2)                    AS total_spend
FROM google_ads
GROUP BY campaign_name

UNION ALL

SELECT
    'Meta'                                  AS channel,
    campaign_name,
    ROUND(SUM(spend), 2)                    AS total_spend
FROM meta_ads
GROUP BY campaign_name
ORDER BY total_spend DESC
"""

df = pd.read_sql(query, conn)
print("--- Campaign Spend ---")
print(df.to_string())