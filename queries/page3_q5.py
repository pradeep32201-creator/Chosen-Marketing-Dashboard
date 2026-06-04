import pandas as pd
import sqlite3

conn = sqlite3.connect('marketing_dashboard.db')



query = """
SELECT
    utm_campaign,
    utm_source,
    COUNT(*)                                        AS total_sessions,
    SUM(purchased)                                  AS total_purchased,
    ROUND(SUM(purchased) * 100.0 /
          COUNT(*), 2)                              AS purchase_rate_pct,
    ROUND(SUM(added_to_cart) * 100.0 /
          COUNT(*), 2)                              AS cart_rate_pct
FROM shopify_sessions
WHERE utm_campaign != 'unattributed'
GROUP BY utm_campaign, utm_source
ORDER BY purchase_rate_pct DESC
"""

df = pd.read_sql(query, conn)
print("--- Top Campaigns by Purchase Rate ---")
print(df.to_string())