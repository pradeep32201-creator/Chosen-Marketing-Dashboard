import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """
SELECT
    SUM(added_to_cart + reached_checkout + purchased)   AS total_sessions,
    SUM(added_to_cart)                                  AS total_added_to_cart,
    SUM(reached_checkout)                               AS total_reached_checkout,
    SUM(purchased)                                      AS total_purchased,
    ROUND(SUM(added_to_cart) * 100.0 / 
          SUM(added_to_cart + reached_checkout + 
              purchased), 2)                            AS cart_rate,
    ROUND(SUM(reached_checkout) * 100.0 / 
          SUM(added_to_cart), 2)                        AS checkout_rate,
    ROUND(SUM(purchased) * 100.0 / 
          SUM(reached_checkout), 2)                     AS purchase_rate
FROM shopify_sessions
"""

df = pd.read_sql(query, conn)
print("--- Overall Funnel ---")
print(df.to_string())