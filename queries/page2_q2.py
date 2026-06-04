import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')
query = """
SELECT
    ROUND(SUM(spend), 2)                    AS meta_spend,
    SUM(impressions)                         AS meta_impressions,
    SUM(clicks)                              AS meta_clicks,
    ROUND(AVG(ctr), 4)                       AS meta_ctr,
    ROUND(AVG(cpc), 2)                       AS meta_cpc,
    SUM(purchases)                           AS meta_purchases,
    ROUND(SUM(purchase_revenue), 2)         AS meta_conv_value,
    ROUND(AVG(roas), 2)                      AS platform_roas
FROM meta_ads
"""

df = pd.read_sql(query, conn)
print("--- Meta Ads KPIs ---")
print(df.to_string())