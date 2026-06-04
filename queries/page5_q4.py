import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')


query = """
SELECT
    date,
    campaign_name,
    'Google'                                AS channel,
    ROUND(SUM(spend), 2)                    AS daily_spend,
    ROUND(AVG(roas), 2)                     AS daily_platform_roas,
    SUM(clicks)                             AS daily_clicks
FROM google_ads
GROUP BY date, campaign_name

UNION ALL

SELECT
    date,
    campaign_name,
    'Meta'                                  AS channel,
    ROUND(SUM(spend), 2)                    AS daily_spend,
    ROUND(AVG(roas), 2)                     AS daily_platform_roas,
    SUM(clicks)                             AS daily_clicks
FROM meta_ads
GROUP BY date, campaign_name
ORDER BY date, channel
"""

df = pd.read_sql(query, conn)
print("--- Daily Campaign Trend ---")
print(df.head(10).to_string())