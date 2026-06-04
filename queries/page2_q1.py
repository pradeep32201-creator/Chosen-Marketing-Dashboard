import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    ROUND(SUM(spend), 2)                    AS google_spend,
    SUM(impressions)                         AS google_impressions,
    SUM(clicks)                              AS google_clicks,
    ROUND(AVG(ctr), 4)                       AS google_ctr,
    ROUND(AVG(cpc), 2)                       AS google_cpc,
    SUM(conversions)                         AS google_conversions,
    ROUND(SUM(conv_value), 2)               AS google_conv_value,
    ROUND(AVG(roas), 2)                      AS platform_roas
FROM google_ads
"""

df = pd.read_sql(query, conn)
print("--- Google Ads KPIs ---")
print(df.to_string())