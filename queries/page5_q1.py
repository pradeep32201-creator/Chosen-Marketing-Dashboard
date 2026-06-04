import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    'Google'                                AS channel,
    g.campaign_name,
    ROUND(SUM(g.spend), 2)                  AS total_spend,
    ROUND(SUM(o.revenue), 2)                AS actual_revenue,
    ROUND(SUM(o.revenue) /
          SUM(g.spend), 2)                  AS actual_roas,
    ROUND(AVG(g.roas), 2)                   AS platform_roas,
    ROUND(AVG(g.cpc), 2)                    AS avg_cpc,
    ROUND(AVG(g.ctr), 4)                    AS avg_ctr,
    SUM(g.impressions)                      AS total_impressions,
    SUM(g.clicks)                           AS total_clicks,
    SUM(g.conversions)                      AS total_conversions,
    COUNT(DISTINCT o.order_id)              AS actual_orders
FROM google_ads g
LEFT JOIN shopify_orders o
    ON g.date = o.date
    AND o.utm_source = 'google'
    AND g.campaign_name = o.utm_campaign
GROUP BY g.campaign_name

UNION ALL

SELECT
    'Meta'                                  AS channel,
    m.campaign_name,
    ROUND(SUM(m.spend), 2)                  AS total_spend,
    ROUND(SUM(o.revenue), 2)                AS actual_revenue,
    ROUND(SUM(o.revenue) /
          SUM(m.spend), 2)                  AS actual_roas,
    ROUND(AVG(m.roas), 2)                   AS platform_roas,
    ROUND(AVG(m.cpc), 2)                    AS avg_cpc,
    ROUND(AVG(m.ctr), 4)                    AS avg_ctr,
    SUM(m.impressions)                      AS total_impressions,
    SUM(m.clicks)                           AS total_clicks,
    SUM(m.purchases)                        AS total_conversions,
    COUNT(DISTINCT o.order_id)              AS actual_orders
FROM meta_ads m
LEFT JOIN shopify_orders o
    ON m.date = o.date
    AND o.utm_source = 'meta'
    AND m.campaign_name = o.utm_campaign
GROUP BY m.campaign_name
ORDER BY actual_roas DESC
"""

df = pd.read_sql(query, conn)
print("--- Campaign Overview Table ---")
print(df.to_string())