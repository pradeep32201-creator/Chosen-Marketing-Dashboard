import pandas as pd
import sqlite3

conn = sqlite3.connect('marketing_dashboard.db')


query = """
SELECT
    device,
    COUNT(*)                                            AS total_sessions,
    SUM(added_to_cart)                                  AS total_cart,
    SUM(reached_checkout)                               AS total_checkout,
    SUM(purchased)                                      AS total_purchased,
    ROUND(SUM(added_to_cart) * 100.0 /
          COUNT(*), 2)                                  AS cart_rate_pct,
    ROUND(SUM(reached_checkout) * 100.0 /
          SUM(added_to_cart), 2)                        AS checkout_rate_pct,
    ROUND(SUM(purchased) * 100.0 /
          SUM(reached_checkout), 2)                     AS purchase_rate_pct,
    ROUND(SUM(purchased) * 100.0 /
          COUNT(*), 2)                                  AS overall_cvr_pct
FROM shopify_sessions
GROUP BY device
ORDER BY overall_cvr_pct DESC
"""

df = pd.read_sql(query, conn)
print("--- Funnel by Device ---")
print(df.to_string())