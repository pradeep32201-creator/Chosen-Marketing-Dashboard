import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_dashboard.db')

queries = {
    "KPI Cards": """
        SELECT
            ROUND(SUM(o.revenue), 2) AS total_revenue,
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(SUM(o.revenue) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
        FROM shopify_orders o
    """,
    "Revenue by Source": """
        SELECT utm_source, ROUND(SUM(revenue), 2) AS total_revenue
        FROM shopify_orders
        GROUP BY utm_source
        ORDER BY total_revenue DESC
    """,
    "Revenue by Device": """
        SELECT device, ROUND(SUM(revenue), 2) AS total_revenue
        FROM shopify_orders
        GROUP BY device
        ORDER BY total_revenue DESC
    """
}

for name, query in queries.items():
    print(f"\n--- {name} ---")
    print(pd.read_sql(query, conn))