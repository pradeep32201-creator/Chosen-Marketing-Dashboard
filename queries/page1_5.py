import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

query = """


SELECT
    COUNT(*)                                    AS total_orders,
    SUM(CASE WHEN utm_campaign = 'unattributed' 
        THEN 1 ELSE 0 END)                      AS unattributed_orders,
    ROUND(SUM(CASE WHEN utm_campaign = 'unattributed' 
        THEN 1 ELSE 0 END) * 100.0 / 
        COUNT(*), 1)                            AS unattributed_pct
FROM shopify_orders

"""

df = pd.read_sql(query, conn)
print(df.to_string())