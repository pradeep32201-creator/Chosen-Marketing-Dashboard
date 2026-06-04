import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="CHOSEN | Marketing OS",
    page_icon="✦",
    layout="wide"
)

# ── CSS ──────────────────────────────────────────────────
st.markdown("""

            
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

/* BASE */
html, body { background: #060610 !important; }
.stApp { background: #060610 !important; }
[data-testid="stAppViewContainer"] { background: #060610 !important; }
[data-testid="stMain"] { background: #060610 !important; }
[data-testid="stMainBlockContainer"] {
    background: #060610 !important;
    padding: 2rem 2.5rem !important;
    max-width: 100% !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #08080f !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
    padding: 0 !important;
    min-width: 210px !important;
    max-width: 210px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebarContent"] { padding: 0 !important; }

/* PAGE TITLE — must be bright white */
[data-testid="stMainBlockContainer"] h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0 !important;
}

/* SUBHEADINGS */
[data-testid="stMainBlockContainer"] h2,
[data-testid="stMainBlockContainer"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: #c0c0d0 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    padding-bottom: 8px !important;
    margin-bottom: 12px !important;
}

/* BODY TEXT — scoped away from sidebar */
[data-testid="stMainBlockContainer"] p,
[data-testid="stMainBlockContainer"] span,
[data-testid="stMainBlockContainer"] label {
    font-family: 'DM Mono', monospace !important;
    color: #808090 !important;
}

/* CAPTION — make it visible but subtle */
[data-testid="stCaptionContainer"] p {
    color: #7070a0 !important;
    font-size: 10px !important;
    letter-spacing: 0.08em !important;
    font-family: 'DM Mono', monospace !important;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background: #0e0e1a !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-top: 2px solid rgba(99,102,241,0.6) !important;
    border-radius: 10px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] > div {
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #707090 !important;
}
[data-testid="stMetricValue"] > div {
    font-family: 'DM Mono', monospace !important;
    font-size: 22px !important;
    font-weight: 500 !important;
    color: #f0f0f8 !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stMetricDelta"] > div {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
}

/* DIVIDER */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.04) !important;
    margin: 1.2rem 0 !important;
}

/* MULTISELECT — kill the red, make dark */
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background: #0e0e1a !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 8px !important;
}
[data-baseweb="tag"] {
    background-color: #16162a !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 4px !important;
}
[data-baseweb="tag"] span { color: #6060a0 !important; font-size: 10px !important; }
[data-baseweb="tag"] [role="presentation"] { color: #404060 !important; }

/* DATE INPUT */
[data-testid="stDateInput"] input {
    background: #0e0e1a !important;
    color: #6060a0 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
}

/* SIDEBAR TEXT */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    color: #404060 !important;
}

/* NAV BUTTONS — normal state */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    background: transparent !important;
    border: none !important;
    border-left: 2px solid transparent !important;
    border-radius: 0 !important;
    color: #909090 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.04em !important;
    text-align: left !important;
    padding: 11px 20px !important;
    width: 100% !important;
    box-shadow: none !important;
    outline: none !important;
}
/* NAV BUTTONS — hover */
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    background: rgba(99,102,241,0.07) !important;
    border-left-color: rgba(99,102,241,0.5) !important;
    color: #a0a0d0 !important;
}
/* NAV BUTTONS — active/focus (just-clicked) */
[data-testid="stSidebar"] [data-testid="stButton"] > button:active,
[data-testid="stSidebar"] [data-testid="stButton"] > button:focus {
    background: rgba(99,102,241,0.12) !important;
    border-left-color: #6366f1 !important;
    color: #d0d0ff !important;
    box-shadow: none !important;
    outline: none !important;
}

/* PLOTLY */
[data-testid="stPlotlyChart"] {
    background: #0a0a18 !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    padding: 4px !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1a1a2e; border-radius: 2px; }

/* HIDE streamlit chrome */
[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }

/* Filter section labels: Channel, Device, Campaign, Date Range */
[data-testid="stSidebar"] label > div,
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] .stMarkdown p {
    color: #a0a0b8 !important;
    font-size: 11px !important;
}

/* Filter tag text (google ×, meta ×, etc.) */
[data-baseweb="tag"] span {
    color: #9090b8 !important;
    font-size: 11px !important;
}

/* Nav buttons text */
[data-testid="stSidebar"] button {
    color: #8888aa !important;
}
[data-testid="stSidebar"] button:hover {
    color: #c0c0e0 !important;
    background: rgba(99,102,241,0.08) !important;
}

/* Sidebar plain text: SKINCARE · INDIA, MARKETING OS, PAGES, FILTERS */
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
    color: #7070a0 !important;
    font-size: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Database ──────────────────────────────────────────────
@st.cache_data
def run_query(query):
    conn = sqlite3.connect('marketing_dashboard.db')
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:

    # Brand
    st.markdown("""
    <div style='padding:28px 20px 24px 20px; border-bottom:1px solid rgba(255,255,255,0.04);'>
        <div style='font-family:"DM Mono",monospace; font-size:9px; letter-spacing:0.3em;
                    color:#606080; margin-bottom:6px;'>SKINCARE · INDIA</div>
        <div style='font-family:"Syne",sans-serif; font-size:20px; font-weight:800;
                    color:#f0f0f0; letter-spacing:-0.02em; line-height:1;'>CHOSEN</div>
        <div style='font-family:"DM Mono",monospace; font-size:9px; letter-spacing:0.15em;
                    color:#606080; margin-top:4px;'>MARKETING OS</div>
    </div>
    """, unsafe_allow_html=True)

    # Nav label
    st.markdown("""
    <div style='padding:20px 20px 8px 20px;'>
        <span style='font-size:8px; letter-spacing:0.25em; color:#505070;
                     font-family:"DM Mono",monospace;'>PAGES</span>
    </div>
    """, unsafe_allow_html=True)

    # Session state for active page
    if "page" not in st.session_state:
        st.session_state.page = "Executive Summary"

    nav_items = [
        ("Executive Summary",   "01"),
        ("Channel Performance", "02"),
        ("Funnel Analysis",     "03"),
        ("Order Intelligence",  "04"),
        ("Campaign Deep Dive",  "05"),
    ]

    for label, num in nav_items:
        btn_label = f"{num}  {label}"
        if st.button(btn_label, key=f"nav_{label}", use_container_width=True):
            st.session_state.page = label
            st.rerun()

    page = st.session_state.page

    # Filters label
    st.markdown("""
    <div style='margin:16px 0 0 0; border-top:1px solid rgba(255,255,255,0.04);
                padding:16px 20px 8px 20px;'>
        <span style='font-size:8px; letter-spacing:0.25em; color:#505070;
                     font-family:"DM Mono",monospace;'>FILTERS</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Date Range
    min_date = pd.to_datetime("2025-02-01")
    max_date = pd.to_datetime("2025-04-30")
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # ── Channel
    channel = st.multiselect(
        "Channel",
        options=["google", "meta", "organic", "direct"],
        default=["google", "meta", "organic", "direct"]
    )

    # ── Device
    device = st.multiselect(
        "Device",
        options=["mobile", "desktop", "tablet"],
        default=["mobile", "desktop", "tablet"]
    )

    # ── Campaigns
    campaigns_df = run_query("""
        SELECT campaign_name FROM google_ads
        UNION
        SELECT campaign_name FROM meta_ads
        ORDER BY campaign_name
    """)
    all_campaigns = campaigns_df['campaign_name'].tolist()
    selected_campaigns = st.multiselect(
        "Campaign",
        options=all_campaigns,
        default=all_campaigns
    )

start_date = str(date_range[0])
end_date   = str(date_range[1]) if len(date_range) > 1 else str(date_range[0])

# ════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════════
if page == "Executive Summary":
    st.title("📊 Executive Summary")
    st.caption(f"Showing data from {start_date} to {end_date}")
    st.markdown("---")

    # ── KPI Cards ────────────────────────────────────────
    kpi = run_query(f"""
    SELECT
        ROUND(SUM(o.revenue), 2)                        AS total_revenue,
        ROUND(g.spend + m.spend, 2)                     AS total_spend,
        ROUND(SUM(o.revenue) / (g.spend + m.spend), 2)  AS blended_roas,
        COUNT(DISTINCT o.order_id)                       AS total_orders,
        ROUND(SUM(o.revenue) /
              COUNT(DISTINCT o.order_id), 2)             AS avg_order_value,
        ROUND(CAST(s.purchased AS FLOAT) /
              CAST(s.added_to_cart AS FLOAT) * 100, 2)  AS overall_cvr
    FROM shopify_orders o,
        (SELECT ROUND(SUM(spend),2) AS spend FROM google_ads
         WHERE date BETWEEN '{start_date}' AND '{end_date}') g,
        (SELECT ROUND(SUM(spend),2) AS spend FROM meta_ads
         WHERE date BETWEEN '{start_date}' AND '{end_date}') m,
        (SELECT SUM(purchased) AS purchased,
                SUM(added_to_cart) AS added_to_cart
         FROM shopify_sessions
         WHERE session_date BETWEEN '{start_date}' AND '{end_date}') s
    WHERE o.date BETWEEN '{start_date}' AND '{end_date}'
    AND o.utm_source IN {str(channel).replace('[','(').replace(']',')')}
""")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.metric("💰 Total Revenue",
                  f"₹{kpi['total_revenue'][0]:,.0f}")
    with c2:
        st.metric("📢 Total Spend",
                  f"₹{kpi['total_spend'][0]:,.0f}")
    with c3:
        st.metric("📈 Blended ROAS",
                  f"{kpi['blended_roas'][0]}x")
    with c4:
        st.metric("🛒 Total Orders",
                  f"{kpi['total_orders'][0]:,.0f}")
    with c5:
        st.metric("🧾 Avg Order Value",
                  f"₹{kpi['avg_order_value'][0]:,.0f}")
    with c6:
        st.metric("🎯 Overall CVR",
                  f"{kpi['overall_cvr'][0]}%")

    st.markdown("---")

    # ── Row 2 — Line Chart + Donut ────────────────────────
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📅 Daily Revenue vs Spend")
        daily = run_query(f"""
            SELECT
                o.date,
                ROUND(SUM(o.revenue), 2)                AS daily_revenue,
                ROUND(COALESCE(g.daily_spend, 0) +
                      COALESCE(m.daily_spend, 0), 2)    AS daily_spend
            FROM shopify_orders o
            LEFT JOIN (
                SELECT date, SUM(spend) AS daily_spend
                FROM google_ads
                WHERE date BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY date
            ) g ON o.date = g.date
            LEFT JOIN (
                SELECT date, SUM(spend) AS daily_spend
                FROM meta_ads
                WHERE date BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY date
            ) m ON o.date = m.date
            WHERE o.date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY o.date
            ORDER BY o.date
        """)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=daily['date'], y=daily['daily_revenue'],
            name='Revenue', line=dict(color='#4CAF50', width=2),
            fill='tozeroy', fillcolor='rgba(76,175,80,0.1)'
        ))
        fig1.add_trace(go.Scatter(
            x=daily['date'], y=daily['daily_spend'],
            name='Spend', line=dict(color='#FF5722', width=2),
            fill='tozeroy', fillcolor='rgba(255,87,34,0.1)'
        ))
        fig1.update_layout(
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', y=1.1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("🔵 Revenue by Source")
        source = run_query(f"""
            SELECT
                utm_source,
                ROUND(SUM(revenue), 2) AS total_revenue
            FROM shopify_orders
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
            GROUP BY utm_source
            ORDER BY total_revenue DESC
        """)
        fig2 = px.pie(
            source,
            values='total_revenue',
            names='utm_source',
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig2.update_layout(
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ── Row 3 — Device Bar Chart ──────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📱 Revenue by Device")
        dev = run_query(f"""
            SELECT
                device,
                COUNT(DISTINCT order_id)        AS total_orders,
                ROUND(SUM(revenue), 2)           AS total_revenue,
                ROUND(SUM(revenue) /
                      COUNT(DISTINCT order_id), 2) AS avg_order_value
            FROM shopify_orders
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            AND device IN {str(device).replace('[','(').replace(']',')')}
            GROUP BY device
            ORDER BY total_revenue DESC
        """)
        fig3 = px.bar(
            dev,
            x='device',
            y='total_revenue',
            color='device',
            text='total_revenue',
            color_discrete_sequence=['#667eea', '#f093fb', '#4facfe']
        )
        fig3.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig3.update_layout(
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("⚠️ Data Quality")
        quality = run_query(f"""
            SELECT
                COUNT(*)                                        AS total_orders,
                SUM(CASE WHEN utm_campaign = 'unattributed'
                    THEN 1 ELSE 0 END)                         AS unattributed_orders,
                ROUND(SUM(CASE WHEN utm_campaign = 'unattributed'
                    THEN 1 ELSE 0 END) * 100.0 /
                    COUNT(*), 1)                               AS unattributed_pct,
                SUM(CASE WHEN utm_source = 'direct'
                    THEN 1 ELSE 0 END)                         AS direct_orders,
                SUM(CASE WHEN utm_source = 'organic'
                    THEN 1 ELSE 0 END)                         AS organic_orders
            FROM shopify_orders
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
        """)
        st.markdown("### Attribution Summary")
        q1, q2 = st.columns(2)
        with q1:
            st.metric("Total Orders", quality['total_orders'][0])
            st.metric("Unattributed", quality['unattributed_orders'][0])
        with q2:
            st.metric("Direct Orders", quality['direct_orders'][0])
            st.metric("Organic Orders", quality['organic_orders'][0])

        unatt_pct = quality['unattributed_pct'][0]
        if unatt_pct == 0:
            st.success("✅ All orders are attributed")
        elif unatt_pct < 10:
            st.warning(f"⚠️ {unatt_pct}% orders unattributed")
        else:
            st.error(f"🔴 {unatt_pct}% orders unattributed — action needed")

# ════════════════════════════════════════════════════════
# PAGE 2 — CHANNEL PERFORMANCE
# ════════════════════════════════════════════════════════
elif page == "Channel Performance":
    st.title("📢 Channel Performance")
    st.caption(f"Showing data from {start_date} to {end_date}")
    st.markdown("---")

    # ── Google & Meta KPI Cards ──────────────────────────
    google_kpi = run_query(f"""
        SELECT
            ROUND(SUM(spend), 2)        AS spend,
            SUM(impressions)             AS impressions,
            SUM(clicks)                  AS clicks,
            ROUND(AVG(ctr), 2)           AS ctr,
            ROUND(AVG(cpc), 2)           AS cpc,
            SUM(conversions)             AS conversions,
            ROUND(SUM(conv_value), 2)    AS conv_value,
            ROUND(AVG(roas), 2)          AS platform_roas
        FROM google_ads
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
    """)

    meta_kpi = run_query(f"""
        SELECT
            ROUND(SUM(spend), 2)            AS spend,
            SUM(impressions)                 AS impressions,
            SUM(clicks)                      AS clicks,
            ROUND(AVG(ctr), 2)               AS ctr,
            ROUND(AVG(cpc), 2)               AS cpc,
            SUM(purchases)                   AS purchases,
            ROUND(SUM(purchase_revenue), 2)  AS conv_value,
            ROUND(AVG(roas), 2)              AS platform_roas
        FROM meta_ads
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
    """)

    col_g, col_m = st.columns(2)

    with col_g:
        st.markdown("### 🟡 Google Ads")
        g1, g2, g3 = st.columns(3)
        g1.metric("Spend", f"₹{google_kpi['spend'][0]:,.0f}")
        g2.metric("Platform ROAS", f"{google_kpi['platform_roas'][0]}×")
        g3.metric("CPC", f"₹{google_kpi['cpc'][0]}")
        g4, g5, g6 = st.columns(3)
        g4.metric("Clicks", f"{int(google_kpi['clicks'][0]):,}")
        g5.metric("CTR", f"{google_kpi['ctr'][0]}%")
        g6.metric("Conversions", f"{int(google_kpi['conversions'][0]):,}")

    with col_m:
        st.markdown("### 🟣 Meta Ads")
        m1, m2, m3 = st.columns(3)
        m1.metric("Spend", f"₹{meta_kpi['spend'][0]:,.0f}")
        m2.metric("Platform ROAS", f"{meta_kpi['platform_roas'][0]}×")
        m3.metric("CPC", f"₹{meta_kpi['cpc'][0]}")
        m4, m5, m6 = st.columns(3)
        m4.metric("Clicks", f"{int(meta_kpi['clicks'][0]):,}")
        m5.metric("CTR", f"{meta_kpi['ctr'][0]}%")
        m6.metric("Purchases", f"{int(meta_kpi['purchases'][0]):,}")

    st.markdown("---")

    # ── Platform ROAS vs Actual ROAS ─────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Platform ROAS vs Actual ROAS")
        roas_df = run_query(f"""
            SELECT 'Google' AS channel,
                ROUND(AVG(g.roas), 2)                   AS platform_roas,
                ROUND(SUM(o.revenue) / SUM(g.spend), 2) AS actual_roas
            FROM google_ads g
            LEFT JOIN shopify_orders o
                ON g.date = o.date AND o.utm_source = 'google'
            WHERE g.date BETWEEN '{start_date}' AND '{end_date}'

            UNION ALL

            SELECT 'Meta' AS channel,
                ROUND(AVG(m.roas), 2)                   AS platform_roas,
                ROUND(SUM(o.revenue) / SUM(m.spend), 2) AS actual_roas
            FROM meta_ads m
            LEFT JOIN shopify_orders o
                ON m.date = o.date AND o.utm_source = 'meta'
            WHERE m.date BETWEEN '{start_date}' AND '{end_date}'
        """)

        import plotly.graph_objects as go

        fig_roas = go.Figure()
        fig_roas.add_trace(go.Bar(
            name='Platform Reported',
            x=roas_df['channel'],
            y=roas_df['platform_roas'],
            marker_color='#444466',
            text=roas_df['platform_roas'].apply(lambda x: f"{x}×"),
            textposition='outside'
        ))
        fig_roas.add_trace(go.Bar(
            name='Shopify Actual',
            x=roas_df['channel'],
            y=roas_df['actual_roas'],
            marker_color=['#f59e0b', '#6366f1'],
            text=roas_df['actual_roas'].apply(lambda x: f"{x}×"),
            textposition='outside'
        ))
        fig_roas.update_layout(
            barmode='group',
            height=320,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            legend=dict(orientation='h', y=1.12),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title='ROAS'),
            margin=dict(t=40, b=20)
        )
        st.plotly_chart(fig_roas, use_container_width=True)
        st.caption("⚠️ Meta overclaims by ~6.9× · Google underclaims by ~6.3× — always verify against Shopify")

    with col2:
        st.subheader("📅 Daily Spend by Channel")
        daily_spend = run_query(f"""
            SELECT g.date,
                ROUND(SUM(g.spend), 2) AS google_spend,
                ROUND(SUM(m.spend), 2) AS meta_spend
            FROM google_ads g
            LEFT JOIN meta_ads m ON g.date = m.date
            WHERE g.date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY g.date
            ORDER BY g.date
        """)

        fig_spend = go.Figure()
        fig_spend.add_trace(go.Bar(
            name='Google',
            x=daily_spend['date'],
            y=daily_spend['google_spend'],
            marker_color='#f59e0b',
            opacity=0.85
        ))
        fig_spend.add_trace(go.Bar(
            name='Meta',
            x=daily_spend['date'],
            y=daily_spend['meta_spend'],
            marker_color='#6366f1',
            opacity=0.85
        ))
        fig_spend.update_layout(
            barmode='stack',
            height=320,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            legend=dict(orientation='h', y=1.12),
            xaxis=dict(showgrid=False, tickangle=-45),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title='Spend (₹)'),
            margin=dict(t=40, b=20)
        )
        st.plotly_chart(fig_spend, use_container_width=True)

    st.markdown("---")

    # ── Campaign Level Table ──────────────────────────────
    st.subheader("📋 Campaign Performance Table")

    camp_df = run_query(f"""
        SELECT
            'Google' AS channel,
            g.campaign_name,
            g.campaign_type,
            ROUND(SUM(g.spend), 2)          AS total_spend,
            ROUND(SUM(o.revenue), 2)         AS actual_revenue,
            ROUND(SUM(o.revenue) / SUM(g.spend), 2) AS actual_roas,
            ROUND(AVG(g.cpc), 2)             AS avg_cpc,
            ROUND(AVG(g.ctr), 2)             AS avg_ctr,
            SUM(g.clicks)                    AS total_clicks,
            SUM(g.conversions)               AS conversions
        FROM google_ads g
        LEFT JOIN shopify_orders o
            ON g.date = o.date
            AND o.utm_source = 'google'
            AND g.campaign_name = o.utm_campaign
        WHERE g.date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY g.campaign_name, g.campaign_type

        UNION ALL

        SELECT
            'Meta' AS channel,
            m.campaign_name,
            m.creative_format AS campaign_type,
            ROUND(SUM(m.spend), 2)          AS total_spend,
            ROUND(SUM(o.revenue), 2)         AS actual_revenue,
            ROUND(SUM(o.revenue) / SUM(m.spend), 2) AS actual_roas,
            ROUND(AVG(m.cpc), 2)             AS avg_cpc,
            ROUND(AVG(m.ctr), 2)             AS avg_ctr,
            SUM(m.clicks)                    AS total_clicks,
            SUM(m.purchases)                 AS conversions
        FROM meta_ads m
        LEFT JOIN shopify_orders o
            ON m.date = o.date
            AND o.utm_source = 'meta'
            AND m.campaign_name = o.utm_campaign
        WHERE m.date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY m.campaign_name, m.creative_format
        ORDER BY actual_roas DESC
    """)

    def color_roas(val):
        if val >= 2.0:
            return 'color: #4ade80; font-weight: bold'
        elif val >= 1.0:
            return 'color: #fbbf24'
        else:
            return 'color: #f87171; font-weight: bold'

    def color_channel(val):
        if val == 'Google':
            return 'color: #f59e0b'
        return 'color: #6366f1'

    styled = (
        camp_df.style
        .map(color_roas, subset=['actual_roas'])
        .map(color_channel, subset=['channel'])
        .format({
            'total_spend': '₹{:,.0f}',
            'actual_revenue': '₹{:,.0f}',
            'actual_roas': '{:.2f}×',
            'avg_cpc': '₹{:.2f}',
            'avg_ctr': '{:.2f}%',
        })
        .set_properties(**{
            'background-color': '#111118',
            'color': '#ccc',
            'border': '1px solid rgba(255,255,255,0.06)'
        })
    )

    st.dataframe(styled, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════
# PAGE 3 — FUNNEL ANALYSIS
# ════════════════════════════════════════════════════════
elif page == "Funnel Analysis":
    st.title("🔻 Funnel Analysis")
    st.caption(f"Showing data from {start_date} to {end_date}")
    st.markdown("---")

    # ── Overall Funnel ────────────────────────────────────
    funnel_df = run_query(f"""
        SELECT
            COUNT(*)                        AS total_sessions,
            SUM(added_to_cart)              AS total_cart,
            SUM(reached_checkout)           AS total_checkout,
            SUM(purchased)                  AS total_purchased,
            ROUND(SUM(added_to_cart) * 100.0 / COUNT(*), 2)         AS cart_rate,
            ROUND(SUM(reached_checkout) * 100.0 / SUM(added_to_cart), 2) AS checkout_rate,
            ROUND(SUM(purchased) * 100.0 / SUM(reached_checkout), 2)    AS purchase_rate
        FROM shopify_sessions
        WHERE session_date BETWEEN '{start_date}' AND '{end_date}'
        AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
    """)

    # ── Funnel KPI cards ─────────────────────────────────
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Total Sessions",   f"{int(funnel_df['total_sessions'][0]):,}")
    f2.metric("Added to Cart",    f"{int(funnel_df['total_cart'][0]):,}",
              delta=f"{funnel_df['cart_rate'][0]}% of sessions")
    f3.metric("Reached Checkout", f"{int(funnel_df['total_checkout'][0]):,}",
              delta=f"{funnel_df['checkout_rate'][0]}% of cart")
    f4.metric("Purchased",        f"{int(funnel_df['total_purchased'][0]):,}",
              delta=f"{funnel_df['purchase_rate'][0]}% of checkout")

    st.markdown("---")

    col1, col2 = st.columns(2)

    # ── Funnel chart ─────────────────────────────────────
    with col1:
        st.subheader("📉 Overall Funnel")

        import plotly.graph_objects as go

        stages = ["Sessions", "Add to Cart", "Checkout", "Purchased"]
        values = [
            int(funnel_df['total_sessions'][0]),
            int(funnel_df['total_cart'][0]),
            int(funnel_df['total_checkout'][0]),
            int(funnel_df['total_purchased'][0]),
        ]

        fig_funnel = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker=dict(color=["#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe"]),
            connector=dict(line=dict(color="rgba(255,255,255,0.05)", width=1)),
            textfont=dict(color="#ffffff", size=12)
        ))
        fig_funnel.update_layout(
            height=340,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            margin=dict(t=20, b=20, l=10, r=10)
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

    # ── Drop-off rates ────────────────────────────────────
    with col2:
        st.subheader("⚠️ Drop-off at Each Stage")

        dropoff_df = run_query(f"""
            SELECT
                ROUND((1 - SUM(added_to_cart) * 1.0 / COUNT(*)) * 100, 2)
                    AS sessions_to_cart_drop,
                ROUND((1 - SUM(reached_checkout) * 1.0 / SUM(added_to_cart)) * 100, 2)
                    AS cart_to_checkout_drop,
                ROUND((1 - SUM(purchased) * 1.0 / SUM(reached_checkout)) * 100, 2)
                    AS checkout_to_purchase_drop
            FROM shopify_sessions
            WHERE session_date BETWEEN '{start_date}' AND '{end_date}'
            AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
        """)

        drops = [
            ("Sessions → Cart",       dropoff_df['sessions_to_cart_drop'][0],    "Biggest leak — product-market fit or ad relevance issue"),
            ("Cart → Checkout",       dropoff_df['cart_to_checkout_drop'][0],     "Shipping cost or trust issue"),
            ("Checkout → Purchase",   dropoff_df['checkout_to_purchase_drop'][0], "Payment friction or last-minute hesitation"),
        ]

        for label, pct, note in drops:
            color = "#f87171" if pct > 75 else "#fbbf24" if pct > 50 else "#4ade80"
            st.markdown(f"""
            <div style='margin-bottom:18px;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:5px;'>
                    <span style='font-size:12px; color:#ccc;'>{label}</span>
                    <span style='font-size:13px; font-weight:700; color:{color}; font-family:"DM Mono",monospace;'>{pct}% drop</span>
                </div>
                <div style='background:rgba(255,255,255,0.05); border-radius:3px; height:6px;'>
                    <div style='width:{pct}%; background:{color}; border-radius:3px; height:100%;'></div>
                </div>
                <div style='font-size:10px; color:#555; margin-top:4px; font-family:"DM Mono",monospace;'>{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Funnel by Channel ─────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📊 Funnel by Channel")

        channel_funnel = run_query(f"""
            SELECT
                utm_source,
                COUNT(*)                                            AS sessions,
                SUM(added_to_cart)                                  AS cart,
                SUM(reached_checkout)                               AS checkout,
                SUM(purchased)                                      AS purchased,
                ROUND(SUM(purchased) * 100.0 / COUNT(*), 2)        AS overall_cvr
            FROM shopify_sessions
            WHERE session_date BETWEEN '{start_date}' AND '{end_date}'
            AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
            GROUP BY utm_source
            ORDER BY overall_cvr DESC
        """)

        # CVR comparison — much more readable than raw counts
        fig_ch = go.Figure()
        for metric, label, color in [
            ('cart',     'Add to Cart', '#6366f1'),
            ('checkout', 'Checkout',    '#818cf8'),
            ('purchased','Purchased',   '#4ade80'),
        ]:
            pct = (channel_funnel[metric] / channel_funnel['sessions'] * 100).round(2)
            fig_ch.add_trace(go.Bar(
                name=label,
                x=channel_funnel['utm_source'],
                y=pct,
                marker_color=color,
                text=pct.apply(lambda x: f"{x}%"),
                textposition='outside',
                textfont=dict(size=10)
            ))
        fig_ch.update_layout(
            barmode='group',
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            legend=dict(orientation='h', y=1.12),
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.06)',
                title='% of Sessions'
            ),
            margin=dict(t=30, b=10)
        )
        st.plotly_chart(fig_ch, use_container_width=True)

        # Sessions volume as small reference below
        st.markdown("<div style='font-size:10px; color:#555; font-family:DM Mono,monospace; margin-top:-10px;'>Session volume — " +
            " · ".join([f"{row['utm_source']}: {int(row['sessions']):,}" for _, row in channel_funnel.iterrows()]) +
            "</div>", unsafe_allow_html=True)

    # ── Funnel by Device ──────────────────────────────────
    with col4:
        st.subheader("📱 Funnel by Device")

        device_funnel = run_query(f"""
            SELECT
                device,
                COUNT(*)                                            AS sessions,
                ROUND(SUM(added_to_cart) * 100.0 / COUNT(*), 2)    AS cart_rate,
                ROUND(SUM(reached_checkout) * 100.0 / SUM(added_to_cart), 2) AS checkout_rate,
                ROUND(SUM(purchased) * 100.0 / SUM(reached_checkout), 2)     AS purchase_rate,
                ROUND(SUM(purchased) * 100.0 / COUNT(*), 2)        AS overall_cvr
            FROM shopify_sessions
            WHERE session_date BETWEEN '{start_date}' AND '{end_date}'
            AND device IN {str(device).replace('[','(').replace(']',')')}
            GROUP BY device
            ORDER BY overall_cvr DESC
        """)

        fig_dev = go.Figure()
        for metric, color in [('cart_rate','#6366f1'),('checkout_rate','#818cf8'),('purchase_rate','#4ade80')]:
            fig_dev.add_trace(go.Bar(
                name=metric.replace('_',' ').title(),
                x=device_funnel['device'],
                y=device_funnel[metric],
                marker_color=color,
                text=device_funnel[metric].apply(lambda x: f"{x}%"),
                textposition='outside',
                textfont=dict(size=10)
            ))
        fig_dev.update_layout(
            barmode='group',
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            legend=dict(orientation='h', y=1.12),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title='Rate %'),
            margin=dict(t=30, b=10)
        )
        st.plotly_chart(fig_dev, use_container_width=True)

    st.markdown("---")

    # ── Top Campaigns by Purchase Rate ───────────────────
    st.subheader("🏆 Top Campaigns by Purchase Rate")

    camp_funnel = run_query(f"""
        SELECT
            utm_campaign,
            utm_source,
            COUNT(*)                                        AS sessions,
            SUM(purchased)                                  AS purchased,
            ROUND(SUM(purchased) * 100.0 / COUNT(*), 2)    AS purchase_rate,
            ROUND(SUM(added_to_cart) * 100.0 / COUNT(*), 2) AS cart_rate
        FROM shopify_sessions
        WHERE session_date BETWEEN '{start_date}' AND '{end_date}'
        AND utm_campaign != 'unattributed'
        AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
        GROUP BY utm_campaign, utm_source
        ORDER BY purchase_rate DESC
    """)

    st.dataframe(
        camp_funnel.style
        .map(lambda v: 'color:#4ade80; font-weight:bold' if v >= 3
             else ('color:#fbbf24' if v >= 2 else 'color:#f87171'),
             subset=['purchase_rate'])
        .format({'purchase_rate': '{:.2f}%', 'cart_rate': '{:.2f}%'})
        .set_properties(**{
            'background-color': '#111118',
            'color': '#ccc',
            'border': '1px solid rgba(255,255,255,0.06)'
        }),
        use_container_width=True,
        hide_index=True
    )

# ════════════════════════════════════════════════════════
# PAGE 4 — ORDER INTELLIGENCE
# ════════════════════════════════════════════════════════
elif page == "Order Intelligence":
    st.title("🛒 Order Intelligence")
    st.caption(f"Showing data from {start_date} to {end_date}")
    st.markdown("---")

    # ── KPI Cards ─────────────────────────────────────────
    order_kpi = run_query(f"""
        SELECT
            COUNT(DISTINCT order_id)                        AS total_orders,
            ROUND(SUM(revenue), 2)                          AS total_revenue,
            ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value,
            SUM(quantity)                                   AS total_units,
            ROUND(SUM(revenue) / SUM(quantity), 2)          AS avg_rev_per_unit
        FROM shopify_orders
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
        AND device IN {str(device).replace('[','(').replace(']',')')}
        AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
    """)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Orders",      f"{int(order_kpi['total_orders'][0]):,}")
    k2.metric("Total Revenue",     f"₹{order_kpi['total_revenue'][0]:,.0f}")
    k3.metric("Avg Order Value",   f"₹{order_kpi['avg_order_value'][0]:,.0f}")
    k4.metric("Units Sold",        f"{int(order_kpi['total_units'][0]):,}")
    k5.metric("Rev / Unit",        f"₹{order_kpi['avg_rev_per_unit'][0]:,.0f}")

    st.markdown("---")

    # ── Row 1: Revenue by Product + Revenue by City ───────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Revenue by Product")

        product_df = run_query(f"""
            SELECT
                product,
                COUNT(DISTINCT order_id)                        AS orders,
                SUM(quantity)                                   AS units,
                ROUND(SUM(revenue), 2)                          AS revenue,
                ROUND(SUM(revenue) * 100.0 /
                    (SELECT SUM(revenue) FROM shopify_orders
                     WHERE date BETWEEN '{start_date}' AND '{end_date}'), 2) AS pct
            FROM shopify_orders
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            AND device IN {str(device).replace('[','(').replace(']',')')}
            AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
            GROUP BY product
            ORDER BY revenue DESC
        """)

        import plotly.express as px
        fig_prod = px.bar(
            product_df,
            x='revenue',
            y='product',
            orientation='h',
            text=product_df['pct'].apply(lambda x: f"{x}%"),
            color='revenue',
            color_continuous_scale=[[0, '#1e1e3a'], [1, '#6366f1']],
        )
        fig_prod.update_traces(
            textposition='outside',
            textfont=dict(size=10, color='#aaa'),
            marker_line_width=0
        )
        fig_prod.update_layout(
            height=320,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title='Revenue (₹)'),
            yaxis=dict(showgrid=False, title='', autorange='reversed'),
            margin=dict(t=10, b=10, l=10, r=60)
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    with col2:
        st.subheader("🏙️ Revenue by City — Top 10")

        city_df = run_query(f"""
            SELECT
                city,
                COUNT(DISTINCT order_id)    AS orders,
                ROUND(SUM(revenue), 2)      AS revenue,
                ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS aov
            FROM shopify_orders
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            AND device IN {str(device).replace('[','(').replace(']',')')}
            AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
            GROUP BY city
            ORDER BY revenue DESC
            LIMIT 10
        """)

        fig_city = px.bar(
            city_df,
            x='revenue',
            y='city',
            orientation='h',
            text=city_df['revenue'].apply(lambda x: f"₹{x:,.0f}"),
            color='revenue',
            color_continuous_scale=[[0, '#1a2e1a'], [1, '#10b981']],
        )
        fig_city.update_traces(
            textposition='outside',
            textfont=dict(size=10, color='#aaa'),
            marker_line_width=0
        )
        fig_city.update_layout(
            height=320,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title='Revenue (₹)'),
            yaxis=dict(showgrid=False, title='', autorange='reversed'),
            margin=dict(t=10, b=10, l=10, r=80)
        )
        st.plotly_chart(fig_city, use_container_width=True)

    st.markdown("---")

    # ── Row 2: Orders Over Time + AOV by Source ───────────
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📅 Orders & Revenue Over Time")

        time_df = run_query(f"""
            SELECT
                date,
                COUNT(DISTINCT order_id)                        AS orders,
                ROUND(SUM(revenue), 2)                          AS revenue,
                ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS aov
            FROM shopify_orders
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            AND device IN {str(device).replace('[','(').replace(']',')')}
            AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
            GROUP BY date
            ORDER BY date
        """)

        import plotly.graph_objects as go
        fig_time = go.Figure()
        fig_time.add_trace(go.Bar(
            x=time_df['date'],
            y=time_df['revenue'],
            name='Revenue',
            marker_color='#6366f1',
            opacity=0.7,
            yaxis='y'
        ))
        fig_time.add_trace(go.Scatter(
            x=time_df['date'],
            y=time_df['orders'],
            name='Orders',
            line=dict(color='#4ade80', width=2),
            mode='lines+markers',
            marker=dict(size=4),
            yaxis='y2'
        ))
        fig_time.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            legend=dict(orientation='h', y=1.12),
            xaxis=dict(showgrid=False, tickangle=-45),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.06)',
                title='Revenue (₹)'
            ),
            yaxis2=dict(
                overlaying='y',
                side='right',
                title='Orders',
                showgrid=False
            ),
            margin=dict(t=30, b=10)
        )
        st.plotly_chart(fig_time, use_container_width=True)

    with col4:
        st.subheader("💳 AOV by UTM Source")

        aov_df = run_query(f"""
            SELECT
                utm_source,
                COUNT(DISTINCT order_id)                        AS orders,
                ROUND(SUM(revenue), 2)                          AS revenue,
                ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS aov,
                ROUND(MAX(revenue), 2)                          AS max_order,
                ROUND(MIN(revenue), 2)                          AS min_order
            FROM shopify_orders
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            AND utm_source IN {str(channel).replace('[','(').replace(']',')')}
            GROUP BY utm_source
            ORDER BY aov DESC
        """)

        fig_aov = px.bar(
            aov_df,
            x='utm_source',
            y='aov',
            text=aov_df['aov'].apply(lambda x: f"₹{x:,.0f}"),
            color='aov',
            color_continuous_scale=[[0, '#1a2020'], [1, '#f59e0b']],
        )
        fig_aov.update_traces(
            textposition='outside',
            textfont=dict(size=11, color='#aaa'),
            marker_line_width=0
        )
        fig_aov.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            coloraxis_showscale=False,
            xaxis=dict(showgrid=False, title=''),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title='Avg Order Value (₹)'),
            margin=dict(t=30, b=10)
        )
        st.plotly_chart(fig_aov, use_container_width=True)

    st.markdown("---")

    # ── Row 3: Revenue by Device ──────────────────────────
    st.subheader("📱 Revenue by Device")

    dev_df = run_query(f"""
        SELECT
            device,
            COUNT(DISTINCT order_id)                        AS orders,
            ROUND(SUM(revenue), 2)                          AS revenue,
            ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS aov,
            ROUND(SUM(revenue) * 100.0 /
                (SELECT SUM(revenue) FROM shopify_orders
                 WHERE date BETWEEN '{start_date}' AND '{end_date}'), 2) AS pct
        FROM shopify_orders
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
        AND device IN {str(device).replace('[','(').replace(']',')')}
        GROUP BY device
        ORDER BY revenue DESC
    """)

    d1, d2, d3 = st.columns(3)
    for col_obj, (_, row) in zip([d1, d2, d3], dev_df.iterrows()):
        col_obj.metric(
            f"{'📱' if row['device']=='mobile' else '💻' if row['device']=='desktop' else '📲'} {row['device'].title()}",
            f"₹{row['revenue']:,.0f}",
            delta=f"{row['pct']}% of revenue · AOV ₹{row['aov']:,.0f}"
        )

# ════════════════════════════════════════════════════════
# PAGE 5 — CAMPAIGN DEEP DIVE
# ════════════════════════════════════════════════════════
elif page == "Campaign Deep Dive":
    st.title("🎯 Campaign Deep Dive")
    st.caption(f"Showing data from {start_date} to {end_date}")
    st.markdown("---")

    # ── Full Campaign Table ───────────────────────────────
    camp_df = run_query(f"""
        SELECT
            'Google' AS channel,
            g.campaign_name,
            g.campaign_type,
            ROUND(SUM(g.spend), 2)                          AS total_spend,
            ROUND(SUM(o.revenue), 2)                        AS actual_revenue,
            ROUND(SUM(o.revenue) / SUM(g.spend), 2)         AS actual_roas,
            ROUND(AVG(g.roas), 2)                           AS platform_roas,
            ROUND(AVG(g.cpc), 2)                            AS avg_cpc,
            ROUND(AVG(g.ctr), 2)                            AS avg_ctr,
            SUM(g.clicks)                                   AS clicks,
            SUM(g.conversions)                              AS conversions,
            COUNT(DISTINCT o.order_id)                      AS actual_orders
        FROM google_ads g
        LEFT JOIN shopify_orders o
            ON g.date = o.date
            AND o.utm_source = 'google'
            AND g.campaign_name = o.utm_campaign
        WHERE g.date BETWEEN '{start_date}' AND '{end_date}'
        AND g.campaign_name IN {str(selected_campaigns).replace('[','(').replace(']',')')}
        GROUP BY g.campaign_name, g.campaign_type

        UNION ALL

        SELECT
            'Meta' AS channel,
            m.campaign_name,
            m.creative_format                               AS campaign_type,
            ROUND(SUM(m.spend), 2)                          AS total_spend,
            ROUND(SUM(o.revenue), 2)                        AS actual_revenue,
            ROUND(SUM(o.revenue) / SUM(m.spend), 2)         AS actual_roas,
            ROUND(AVG(m.roas), 2)                           AS platform_roas,
            ROUND(AVG(m.cpc), 2)                            AS avg_cpc,
            ROUND(AVG(m.ctr), 2)                            AS avg_ctr,
            SUM(m.clicks)                                   AS clicks,
            SUM(m.purchases)                                AS conversions,
            COUNT(DISTINCT o.order_id)                      AS actual_orders
        FROM meta_ads m
        LEFT JOIN shopify_orders o
            ON m.date = o.date
            AND o.utm_source = 'meta'
            AND m.campaign_name = o.utm_campaign
        WHERE m.date BETWEEN '{start_date}' AND '{end_date}'
        AND m.campaign_name IN {str(selected_campaigns).replace('[','(').replace(']',')')}
        GROUP BY m.campaign_name, m.creative_format
        ORDER BY actual_roas DESC
    """)

    # ── Best / Worst highlight cards ──────────────────────
    if not camp_df.empty:
        best = camp_df.iloc[0]
        worst = camp_df.iloc[-1]

        c_best, c_worst = st.columns(2)
        with c_best:
            st.markdown(f"""
            <div style='background:rgba(74,222,128,0.06); border:1px solid rgba(74,222,128,0.2);
                        border-radius:10px; padding:14px 18px;'>
                <div style='font-size:9px; color:#4ade80; letter-spacing:0.15em;
                            font-family:"DM Mono",monospace; margin-bottom:6px;'>TOP PERFORMER</div>
                <div style='font-size:14px; color:#e0e0e0; font-weight:600;
                            margin-bottom:4px;'>{best['campaign_name']}</div>
                <div style='font-size:11px; color:#4ade80; font-family:"DM Mono",monospace;'>
                    {best['actual_roas']}× ROAS &nbsp;·&nbsp;
                    ₹{best['actual_revenue']:,.0f} revenue &nbsp;·&nbsp;
                    {best['channel']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_worst:
            st.markdown(f"""
            <div style='background:rgba(248,113,113,0.06); border:1px solid rgba(248,113,113,0.2);
                        border-radius:10px; padding:14px 18px;'>
                <div style='font-size:9px; color:#f87171; letter-spacing:0.15em;
                            font-family:"DM Mono",monospace; margin-bottom:6px;'>NEEDS ATTENTION</div>
                <div style='font-size:14px; color:#e0e0e0; font-weight:600;
                            margin-bottom:4px;'>{worst['campaign_name']}</div>
                <div style='font-size:11px; color:#f87171; font-family:"DM Mono",monospace;'>
                    {worst['actual_roas']}× ROAS &nbsp;·&nbsp;
                    ₹{worst['actual_revenue']:,.0f} revenue &nbsp;·&nbsp;
                    {worst['channel']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── ROAS Comparison Chart ─────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Actual ROAS by Campaign")

        import plotly.graph_objects as go

        colors = camp_df['actual_roas'].apply(
            lambda x: '#4ade80' if x >= 2.0 else '#fbbf24' if x >= 1.0 else '#f87171'
        )

        fig_roas = go.Figure(go.Bar(
            x=camp_df['actual_roas'],
            y=camp_df['campaign_name'],
            orientation='h',
            marker_color=colors,
            text=camp_df['actual_roas'].apply(lambda x: f"{x}×"),
            textposition='outside',
            textfont=dict(size=10, color='#aaa')
        ))
        fig_roas.add_vline(
            x=1.0,
            line_dash="dash",
            line_color="rgba(255,255,255,0.2)",
            annotation_text="Break-even",
            annotation_font_color="#555",
            annotation_font_size=10
        )
        fig_roas.add_vline(
            x=2.0,
            line_dash="dash",
            line_color="rgba(74,222,128,0.3)",
            annotation_text="Profitable",
            annotation_font_color="#4ade80",
            annotation_font_size=10
        )
        fig_roas.update_layout(
            height=360,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title='Actual ROAS'),
            yaxis=dict(showgrid=False, autorange='reversed'),
            margin=dict(t=10, b=20, l=10, r=60)
        )
        st.plotly_chart(fig_roas, use_container_width=True)

    with col2:
        st.subheader("💰 Spend vs Revenue by Campaign")

        import plotly.express as px

        fig_sv = go.Figure()
        fig_sv.add_trace(go.Bar(
            name='Spend',
            x=camp_df['campaign_name'],
            y=camp_df['total_spend'],
            marker_color='#334155',
            text=camp_df['total_spend'].apply(lambda x: f"₹{x:,.0f}"),
            textposition='outside',
            textfont=dict(size=9, color='#666')
        ))
        fig_sv.add_trace(go.Bar(
            name='Revenue',
            x=camp_df['campaign_name'],
            y=camp_df['actual_revenue'],
            marker_color='#6366f1',
            text=camp_df['actual_revenue'].apply(lambda x: f"₹{x:,.0f}"),
            textposition='outside',
            textfont=dict(size=9, color='#aaa')
        ))
        fig_sv.update_layout(
            barmode='group',
            height=360,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#aaa',
            legend=dict(orientation='h', y=1.1),
            xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=9)),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title='₹'),
            margin=dict(t=30, b=20)
        )
        st.plotly_chart(fig_sv, use_container_width=True)

    st.markdown("---")

    # ── Platform vs Actual ROAS per Campaign ─────────────
    st.subheader("🔍 Platform Reported vs Shopify-Verified ROAS")

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name='Platform Reported',
        x=camp_df['campaign_name'],
        y=camp_df['platform_roas'],
        marker_color='#334155',
        text=camp_df['platform_roas'].apply(lambda x: f"{x}×"),
        textposition='outside',
        textfont=dict(size=9, color='#666')
    ))
    fig_comp.add_trace(go.Bar(
        name='Shopify Actual',
        x=camp_df['campaign_name'],
        y=camp_df['actual_roas'],
        marker_color='#f59e0b',
        text=camp_df['actual_roas'].apply(lambda x: f"{x}×"),
        textposition='outside',
        textfont=dict(size=9, color='#aaa')
    ))
    fig_comp.update_layout(
        barmode='group',
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#aaa',
        legend=dict(orientation='h', y=1.1),
        xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title='ROAS'),
        margin=dict(t=30, b=20)
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    st.caption("Platform numbers are self-reported — always cross-check with Shopify revenue")

    st.markdown("---")

    # ── Full Sortable Campaign Table ──────────────────────
    st.subheader("📋 Full Campaign Table")

    def tag_status(val):
        if val >= 2.0:
            return 'color: #4ade80; font-weight: bold'
        elif val >= 1.0:
            return 'color: #fbbf24'
        return 'color: #f87171; font-weight: bold'

    def tag_channel(val):
        return 'color: #f59e0b' if val == 'Google' else 'color: #6366f1'

    st.dataframe(
        camp_df.style
        .map(tag_status, subset=['actual_roas'])
        .map(tag_channel, subset=['channel'])
        .format({
            'total_spend':    '₹{:,.0f}',
            'actual_revenue': '₹{:,.0f}',
            'actual_roas':    '{:.2f}×',
            'platform_roas':  '{:.2f}×',
            'avg_cpc':        '₹{:.2f}',
            'avg_ctr':        '{:.2f}%',
        })
        .set_properties(**{
            'background-color': '#111118',
            'color': '#ccc',
            'border': '1px solid rgba(255,255,255,0.06)'
        }),
        use_container_width=True,
        hide_index=True
    )