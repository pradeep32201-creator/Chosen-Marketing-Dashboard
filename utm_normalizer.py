import sqlite3
conn = sqlite3.connect('marketing_dashboard.db')
cur = conn.cursor()

cur.execute("UPDATE shopify_orders SET utm_campaign = 'unattributed' WHERE utm_campaign IS NULL")
cur.execute("UPDATE shopify_session SET utm_campaign = 'unattributed' WHERE utm_campaign IS NULL")
cur.execute("UPDATE shopify_orders SET utm_source = 'google' WHERE utm_campaign IN ('Brand search — CHOSEN', 'Google shopping — all products', 'Competitor keywords', 'Remarketing — display')")

conn.commit()
print("Done")