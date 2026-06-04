import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')


query = """
WITH campaign_data AS (
    SELECT
        'Google'                            AS channel,
        g.campaign_name,
        ROUND(SUM(g.spend), 2)              AS total_spend,
        ROUND(SUM(o.revenue), 2)            AS actual_revenue,
        ROUND(SUM(o.revenue) /
              SUM(g.spend), 2)              AS actual_roas
    FROM google_ads g
    LEFT JOIN shopify_orders o
        ON g.date = o.date
        AND o.utm_source = 'google'
        AND g.campaign_name = o.utm_campaign
    GROUP BY g.campaign_name

    UNION ALL

    SELECT
        'Meta'                              AS channel,
        m.campaign_name,
        ROUND(SUM(m.spend), 2)              AS total_spend,
        ROUND(SUM(o.revenue), 2)            AS actual_revenue,
        ROUND(SUM(o.revenue) /
              SUM(m.spend), 2)              AS actual_roas
    FROM meta_ads m
    LEFT JOIN shopify_orders o
        ON m.date = o.date
        AND o.utm_source = 'meta'
        AND m.campaign_name = o.utm_campaign
    GROUP BY m.campaign_name
)
SELECT
    channel,
    campaign_name,
    total_spend,
    actual_revenue,
    actual_roas,
    CASE
        WHEN actual_roas >= 2.0  THEN '🟢 Profitable'
        WHEN actual_roas >= 1.0  THEN '🟡 Breaking Even'
        ELSE                          '🔴 Loss Making'
    END AS campaign_status
FROM campaign_data
ORDER BY actual_roas DESC
"""

df = pd.read_sql(query, conn)
print("--- Best vs Worst Campaigns ---")
print(df.to_string())