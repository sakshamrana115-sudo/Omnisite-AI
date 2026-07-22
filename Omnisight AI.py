"""
OmniSight AI — Investment Intelligence Platform
------------------------------------------------
FRONTEND-ONLY INVESTOR DEMO PROTOTYPE.
All data below is hardcoded / simulated. There is no live market data,
no machine learning, no trading engine, and no real financial advice.
Run with:  streamlit run omniscight_ai.py
"""

import time
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="OmniSight AI | Investment Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# GLOBAL THEME / CSS  (dark glassmorphism, neon blue/purple)
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #10142b 0%, #05060f 45%, #020204 100%);
        color: #e8e9f3;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0c1e 0%, #05060f 100%);
        border-right: 1px solid rgba(124, 92, 255, 0.15);
    }
    section[data-testid="stSidebar"] * {
        color: #d8d9f0 !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 0.3px;
    }

    /* Glass card */
    .glass-card {
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(124, 92, 255, 0.22);
        border-radius: 18px;
        padding: 22px 24px;
        backdrop-filter: blur(14px);
        box-shadow: 0 4px 30px rgba(0,0,0,0.35);
        margin-bottom: 18px;
        transition: all 0.25s ease;
    }
    .glass-card:hover {
        border: 1px solid rgba(124, 92, 255, 0.55);
        box-shadow: 0 4px 40px rgba(124, 92, 255, 0.18);
        transform: translateY(-2px);
    }

    .brand-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        background: linear-gradient(90deg, #7c5cff 0%, #35d3ff 60%, #7c5cff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .brand-sub {
        color: #8b8fc0;
        font-size: 0.95rem;
        margin-top: -6px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .pill {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .pill-green { background: rgba(45, 220, 150, 0.15); color: #4ce6a8; border: 1px solid rgba(76,230,168,0.4); }
    .pill-red { background: rgba(255, 90, 110, 0.15); color: #ff7b8f; border: 1px solid rgba(255,123,143,0.4); }
    .pill-blue { background: rgba(90, 140, 255, 0.15); color: #7fb0ff; border: 1px solid rgba(127,176,255,0.4); }
    .pill-purple { background: rgba(160, 90, 255, 0.15); color: #c39bff; border: 1px solid rgba(195,155,255,0.4); }

    .metric-big {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-label {
        color: #8b8fc0;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .ai-bubble {
        background: linear-gradient(135deg, rgba(124,92,255,0.16), rgba(53,211,255,0.08));
        border: 1px solid rgba(124,92,255,0.35);
        border-radius: 16px 16px 16px 4px;
        padding: 16px 18px;
        margin: 8px 0 18px 0;
        color: #e8e9f3;
        line-height: 1.55;
    }
    .user-bubble {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px 16px 4px 16px;
        padding: 12px 18px;
        margin: 8px 0;
        color: #d8d9f0;
        text-align: right;
        display: inline-block;
        float: right;
    }

    .footer-disclaimer {
        margin-top: 60px;
        padding: 18px;
        border-top: 1px solid rgba(255,255,255,0.08);
        color: #6b6f95;
        font-size: 0.78rem;
        text-align: center;
    }

    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(124,92,255,0.4), transparent);
        margin: 22px 0;
        border: none;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(124,92,255,0.18);
        border-radius: 14px;
        padding: 12px 16px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #7c5cff, #35d3ff);
        color: #05060f;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 8px 20px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(124,92,255,0.5);
        transform: translateY(-1px);
    }

    .badge-live {
        display:inline-block; width:8px; height:8px; border-radius:50%;
        background:#4ce6a8; margin-right:6px; box-shadow:0 0 8px #4ce6a8;
        animation: pulse 1.6s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.35; }
        100% { opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# MOCK / HARDCODED DATA
# ============================================================

USER_PROFILE = {
    "name": "Alex Sharma",
    "risk_profile": "Moderate",
    "style": "Long Term Growth",
    "portfolio_value": 2_500_000,
}

HOLDINGS = pd.DataFrame([
    {"Company": "Reliance Industries", "Sector": "Energy / Conglomerate", "Value": 620000, "Allocation": 24.8, "Performance": 12.4},
    {"Company": "TCS",                 "Sector": "Technology",            "Value": 540000, "Allocation": 21.6, "Performance": 9.1},
    {"Company": "HDFC Bank",           "Sector": "Banking / Financials",  "Value": 480000, "Allocation": 19.2, "Performance": 6.7},
    {"Company": "Infosys",             "Sector": "Technology",            "Value": 410000, "Allocation": 16.4, "Performance": -3.2},
    {"Company": "Tata Motors",         "Sector": "Automobile",            "Value": 450000, "Allocation": 18.0, "Performance": 15.8},
])

AI_RESPONSES = {
    "analyze my portfolio": (
        "Your portfolio has strong quality exposure but carries **38% technology "
        "concentration** (TCS + Infosys). A global tech correction could increase "
        "portfolio volatility by an estimated 9-14%. Diversification into defensive "
        "sectors (FMCG, Healthcare) could reduce this concentration risk."
    ),
    "how will oil prices affect me": (
        "Rising oil prices are a **mixed signal** for your holdings. Reliance Industries "
        "(24.8% of your book) benefits from higher refining margins, while Tata Motors "
        "could see input-cost pressure on logistics and raw materials. Net estimated "
        "portfolio impact: **+1.8% to +3.1%** in a moderate oil-shock scenario."
    ),
    "what are my biggest risks": (
        "Three key risk vectors detected:\n\n"
        "1. **Sector concentration** — Technology + Banking = 40.8% of portfolio\n"
        "2. **Single-country exposure** — 100% India-listed equities\n"
        "3. **Rate sensitivity** — HDFC Bank valuation is moderately sensitive to RBI rate policy\n\n"
        "Overall Risk Score: **56/100** (Moderate)"
    ),
    "explain my holdings": (
        "You hold 5 large-cap Indian equities spanning Energy, Technology, Banking and "
        "Automobile sectors. This is a classic **blue-chip growth allocation** — built "
        "for long-term compounding with moderate short-term volatility. Reliance and "
        "Tata Motors are currently your strongest momentum contributors."
    ),
}

GLOBAL_MARKETS = pd.DataFrame([
    {"Market": "US Market (S&P 500)", "Value": "5,712", "Change": "+0.62%", "Direction": "up"},
    {"Market": "Oil Price (Brent)", "Value": "$86.40", "Change": "+2.1%", "Direction": "up"},
    {"Market": "US 10Y Yield", "Value": "4.32%", "Change": "+0.05%", "Direction": "up"},
    {"Market": "USD/INR", "Value": "83.12", "Change": "-0.18%", "Direction": "down"},
])

ALPHA_COMPANIES = pd.DataFrame([
    {"Company": "ABC Semiconductor", "Sector": "Technology", "Hiring": 45, "Patents": "High", "Expansion": "Detected", "Institutional": "Increasing", "Score": 88},
    {"Company": "Nova Green Energy", "Sector": "Energy", "Hiring": 32, "Patents": "Medium", "Expansion": "Planned", "Institutional": "Stable", "Score": 76},
    {"Company": "MedixCare Labs", "Sector": "Healthcare", "Hiring": 28, "Patents": "High", "Expansion": "Detected", "Institutional": "Increasing", "Score": 81},
    {"Company": "Precision Robotics", "Sector": "Manufacturing", "Hiring": 51, "Patents": "Very High", "Expansion": "Detected", "Institutional": "Increasing", "Score": 91},
])

WHALE_COMPANIES = pd.DataFrame([
    {"Company": "Reliance", "Activity": "High accumulation", "Score": 82},
    {"Company": "HDFC Bank", "Activity": "Moderate accumulation", "Score": 64},
    {"Company": "Tata Motors", "Activity": "Increasing interest", "Score": 71},
    {"Company": "TCS", "Activity": "Neutral", "Score": 50},
])

QUANT_SCORES = {
    "Reliance Industries": {"Quality": 88, "Growth": 74, "Value": 66, "Momentum": 80},
    "TCS":                 {"Quality": 92, "Growth": 78, "Value": 70, "Momentum": 85},
    "HDFC Bank":           {"Quality": 85, "Growth": 62, "Value": 72, "Momentum": 58},
    "Infosys":             {"Quality": 87, "Growth": 60, "Value": 68, "Momentum": 44},
    "Tata Motors":         {"Quality": 70, "Growth": 82, "Value": 75, "Momentum": 90},
}

SCENARIOS = {
    "Oil Price +30%": {
        "Transportation": -14, "Energy": +18, "Airlines": -20, "Automobile": -6,
        "risk_delta": 11, "summary": "Higher fuel costs squeeze transport & auto margins while energy majors gain pricing power."
    },
    "Interest Rate +2%": {
        "Banking": +5, "Real Estate": -12, "Technology": -8,
        "risk_delta": 14, "summary": "Higher rates compress growth-stock valuations while lifting bank net interest margins."
    },
    "Global Recession": {
        "Technology": -22, "Banking": -15, "Energy": -10, "Automobile": -18,
        "risk_delta": 27, "summary": "Broad-based demand contraction hits cyclical and growth sectors hardest."
    },
    "Technology Crash": {
        "Technology": -30, "Banking": -4, "Energy": +2,
        "risk_delta": 19, "summary": "A sharp tech selloff disproportionately impacts your 38% technology allocation."
    },
    "Inflation Shock": {
        "Energy": +12, "Banking": -6, "Technology": -10, "Automobile": -8,
        "risk_delta": 16, "summary": "Persistent inflation erodes real returns and pressures discretionary-spending sectors."
    },
}

PRICING_B2C = [
    {"name": "FREE", "price": "₹0", "period": "/month", "features": ["Portfolio tracking", "Basic market news", "1 AI query/day"], "highlight": False},
    {"name": "PLUS", "price": "₹299", "period": "/month", "features": ["Unlimited AI queries", "Market Intelligence Center", "Risk scoring"], "highlight": False},
    {"name": "PRO", "price": "₹999", "period": "/month", "features": ["GNN Event Engine", "Portfolio Simulation", "Alpha Discovery"], "highlight": True},
    {"name": "WEALTH AGENT", "price": "₹2,999", "period": "/month", "features": ["Dedicated AI wealth agent", "Whale tracking", "Quant research suite"], "highlight": False},
]

PRICING_B2B = [
    {"name": "Starter Fund", "price": "₹10 lakh", "period": "/year"},
    {"name": "Professional", "price": "₹50 lakh", "period": "/year"},
    {"name": "Quant Alpha", "price": "₹1 crore", "period": "/year"},
    {"name": "Autonomous Fund OS", "price": "₹3-5 crore", "period": "/year"},
]

# ============================================================
# HELPERS
# ============================================================

def glass_start():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

def glass_end():
    st.markdown('</div>', unsafe_allow_html=True)

def pill(text, kind="blue"):
    return f'<span class="pill pill-{kind}">{text}</span>'

def ai_thinking(seconds=0.9):
    ph = st.empty()
    frames = ["🧠 OmniSight AI is analyzing", "🧠 OmniSight AI is analyzing.", "🧠 OmniSight AI is analyzing..", "🧠 OmniSight AI is analyzing..."]
    end = time.time() + seconds
    i = 0
    while time.time() < end:
        ph.markdown(f"<span style='color:#8b8fc0'>{frames[i % len(frames)]}</span>", unsafe_allow_html=True)
        time.sleep(0.18)
        i += 1
    ph.empty()

def header(title, subtitle):
    st.markdown(f"<h1 style='margin-bottom:0px'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='brand-sub' style='margin-top:2px'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

def footer():
    st.markdown(
        """
        <div class="footer-disclaimer">
        OmniSight AI provides investment intelligence and advisory insights. It does not provide guaranteed returns
        or direct buy/sell recommendations. All data shown in this prototype is simulated for demonstration purposes only.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
with st.sidebar:
    st.markdown('<div class="brand-title">OmniSight AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Investment Intelligence OS</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown(
        f"<span class='badge-live'></span><span style='color:#8b8fc0;font-size:0.85rem'>Live demo session</span>",
        unsafe_allow_html=True,
    )
    st.write("")

    PAGES = [
        "🧠 AI Portfolio Advisor",
        "🌐 Market Intelligence",
        "🕸️ GNN Event Impact Engine",
        "🧪 Portfolio Simulation",
        "🚀 Alpha Discovery",
        "🐋 Whale Tracking",
        "📊 Quant Research",
        "🏛️ B2B Institutional Dashboard",
        "💳 Subscription Plans",
    ]
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='font-size:0.82rem;color:#8b8fc0;'>
        👤 <b style='color:#e8e9f3'>{USER_PROFILE['name']}</b><br/>
        Risk: {USER_PROFILE['risk_profile']}<br/>
        Style: {USER_PROFILE['style']}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# PAGE 1 — AI PORTFOLIO ADVISOR
# ============================================================
if page == PAGES[0]:
    header("AI Portfolio Advisor", "Your personal AI investment assistant")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Portfolio Value", f"₹{USER_PROFILE['portfolio_value']:,}")
    with c2:
        st.metric("Risk Profile", USER_PROFILE["risk_profile"])
    with c3:
        st.metric("Investment Style", USER_PROFILE["style"])
    with c4:
        st.metric("Holdings", len(HOLDINGS))

    st.write("")
    st.subheader("Portfolio Holdings")
    cols = st.columns(len(HOLDINGS))
    for col, (_, row) in zip(cols, HOLDINGS.iterrows()):
        with col:
            glass_start()
            perf_kind = "green" if row["Performance"] >= 0 else "red"
            perf_sign = "+" if row["Performance"] >= 0 else ""
            st.markdown(f"**{row['Company']}**")
            st.markdown(f"<span style='color:#8b8fc0;font-size:0.8rem'>{row['Sector']}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-big'>₹{row['Value']:,}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-label'>Allocation {row['Allocation']}%</div>", unsafe_allow_html=True)
            st.markdown(pill(f"{perf_sign}{row['Performance']}%", perf_kind), unsafe_allow_html=True)
            glass_end()

    st.write("")
    fig = go.Figure(data=[go.Pie(
        labels=HOLDINGS["Company"], values=HOLDINGS["Allocation"], hole=0.55,
        marker=dict(colors=["#7c5cff", "#35d3ff", "#a05cff", "#5c8cff", "#4ce6a8"],
                    line=dict(color="#05060f", width=2)),
        textfont=dict(color="#ffffff"),
    )])
    fig.update_layout(
        title="Allocation Breakdown", template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=380, legend=dict(font=dict(color="#d8d9f0")),
        font=dict(color="#d8d9f0"),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.subheader("💬 AI Advisor Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    example_qs = ["Analyze my portfolio", "How will oil prices affect me?", "What are my biggest risks?", "Explain my holdings"]
    btn_cols = st.columns(4)
    clicked_q = None
    for col, q in zip(btn_cols, example_qs):
        with col:
            if st.button(q, use_container_width=True):
                clicked_q = q

    typed_q = st.chat_input("Ask OmniSight AI about your portfolio...")
    query = clicked_q or typed_q

    if query:
        key = query.lower().strip("?")
        response = AI_RESPONSES.get(key, None)
        if response is None:
            # fuzzy fallback match
            for k, v in AI_RESPONSES.items():
                if k.split()[0] in key:
                    response = v
                    break
        if response is None:
            response = (
                "Based on your current allocation and moderate risk profile, "
                "this looks like a well-diversified long-term growth position. "
                "Ask me about specific risks, sectors, or market events for a deeper analysis."
            )
        st.session_state.chat_history.append(("user", query))
        st.session_state.chat_history.append(("ai", response))

    for role, msg in st.session_state.chat_history[-8:]:
        if role == "user":
            st.markdown(f"<div class='user-bubble'>{msg}</div><div style='clear:both'></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-bubble'>🧠 <b>OmniSight AI</b><br/>{msg}</div>", unsafe_allow_html=True)

    footer()

# ============================================================
# PAGE 2 — MARKET INTELLIGENCE CENTER
# ============================================================
elif page == PAGES[1]:
    header("Market Intelligence Center", "Real-time simulated global market context")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("NIFTY 50", "22,450", "+0.84%")
    with c2:
        st.metric("Market Sentiment", "Positive", "AI-derived score: 71/100")

    st.write("")
    st.subheader("Global Markets")
    cols = st.columns(4)
    for col, (_, row) in zip(cols, GLOBAL_MARKETS.iterrows()):
        with col:
            glass_start()
            st.markdown(f"<div class='metric-label'>{row['Market']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-big'>{row['Value']}</div>", unsafe_allow_html=True)
            kind = "green" if row["Direction"] == "up" else "red"
            st.markdown(pill(row["Change"], kind), unsafe_allow_html=True)
            glass_end()

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.subheader("📰 News Impact Analysis")

    glass_start()
    st.markdown("**EVENT:** Oil prices rise 20%")
    st.write("")
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown("**Transportation sector**")
        st.markdown(pill("Negative impact", "red"), unsafe_allow_html=True)
    with ic2:
        st.markdown("**Energy sector**")
        st.markdown(pill("Positive impact", "green"), unsafe_allow_html=True)
    with ic3:
        st.markdown("**Your portfolio exposure**")
        st.markdown(pill("Medium risk", "purple"), unsafe_allow_html=True)
    st.write("")
    st.markdown(
        "<span style='color:#c8c9e8'>AI Analysis: Rising oil prices increase input costs across logistics-heavy "
        "sectors while boosting margins for upstream energy producers such as Reliance Industries.</span>",
        unsafe_allow_html=True,
    )
    glass_end()

    days = pd.date_range(end=datetime.today(), periods=30)
    trend = 22450 + np.cumsum(np.random.normal(0, 60, size=30))
    fig = go.Figure(go.Scatter(x=days, y=trend, mode="lines", line=dict(color="#35d3ff", width=2),
                                fill="tozeroy", fillcolor="rgba(53,211,255,0.08)"))
    fig.update_layout(
        title="NIFTY 50 — 30 Day Simulated Trend", template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380,
        font=dict(color="#d8d9f0"),
    )
    st.plotly_chart(fig, use_container_width=True)

    footer()

# ============================================================
# PAGE 3 — GNN EVENT IMPACT ENGINE
# ============================================================
elif page == PAGES[2]:
    header("Graph Neural Network Event Engine", "Simulated multi-hop event propagation")

    event_choice = st.selectbox("Select a global event", ["Oil Price Increase", "Interest Rate Hike", "Global Chip Shortage"])

    chains = {
        "Oil Price Increase": ["Oil Prices", "Transportation Costs", "Airlines", "Tata Motors", "Investor Portfolio"],
        "Interest Rate Hike": ["Interest Rates", "Credit Costs", "Real Estate", "HDFC Bank", "Investor Portfolio"],
        "Global Chip Shortage": ["Chip Supply", "Semiconductor Prices", "Electronics Mfg", "Infosys", "Investor Portfolio"],
    }
    chain = chains[event_choice]

    if st.button("▶ Run GNN Propagation Simulation"):
        ai_thinking(1.2)
        st.success("Propagation complete — 4-hop causal path resolved.")

    G = nx.DiGraph()
    for i in range(len(chain) - 1):
        G.add_edge(chain[i], chain[i + 1])

    pos = {node: (i, 0) for i, node in enumerate(chain)}

    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines",
                             line=dict(color="#7c5cff", width=3), hoverinfo="none")

    node_x = [pos[n][0] for n in chain]
    node_y = [pos[n][1] for n in chain]
    colors = ["#35d3ff", "#7c5cff", "#a05cff", "#ff6bd6", "#4ce6a8"]
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text", text=chain, textposition="top center",
        textfont=dict(color="#e8e9f3", size=13, family="Space Grotesk"),
        marker=dict(size=46, color=colors[:len(chain)], line=dict(color="#05060f", width=3),
                    symbol="circle"),
        hoverinfo="text",
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title=f"Event Propagation Graph — {event_choice}",
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False, height=420,
        xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-1, 1]),
        font=dict(color="#d8d9f0"),
    )
    st.plotly_chart(fig, use_container_width=True)

    glass_start()
    st.markdown("**AI Causal Insight**")
    st.markdown(
        f"<span style='color:#c8c9e8'>The GNN engine traced a {len(chain)-1}-hop causal path from "
        f"<b>{chain[0]}</b> to your portfolio via <b>{chain[-2]}</b>. Estimated propagation confidence: "
        f"<b>{random.randint(78, 94)}%</b>.</span>",
        unsafe_allow_html=True,
    )
    glass_end()

    footer()

# ============================================================
# PAGE 4 — PORTFOLIO SIMULATION ENGINE
# ============================================================
elif page == PAGES[3]:
    header("Portfolio Simulation Engine", "\"What if?\" scenario stress-testing")

    scenario = st.selectbox("Choose a scenario", list(SCENARIOS.keys()))
    base_risk = 42

    if st.button("Run Simulation"):
        ai_thinking(1.0)
        data = SCENARIOS[scenario]
        new_risk = base_risk + data["risk_delta"]

        st.subheader("Simulation Result")
        glass_start()
        st.markdown(f"**Scenario:** {scenario}")
        st.markdown(f"<span style='color:#c8c9e8'>{data['summary']}</span>", unsafe_allow_html=True)
        glass_end()

        impact_items = {k: v for k, v in data.items() if k not in ("risk_delta", "summary")}
        cols = st.columns(len(impact_items))
        for col, (sector, impact) in zip(cols, impact_items.items()):
            with col:
                glass_start()
                st.markdown(f"**{sector}**")
                kind = "green" if impact >= 0 else "red"
                sign = "+" if impact >= 0 else ""
                st.markdown(f"<div class='metric-big'>{sign}{impact}%</div>", unsafe_allow_html=True)
                st.markdown(pill("Impact", kind), unsafe_allow_html=True)
                glass_end()

        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            glass_start()
            st.markdown("<div class='metric-label'>Portfolio Risk — Before</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-big'>{base_risk}/100</div>", unsafe_allow_html=True)
            glass_end()
        with c2:
            glass_start()
            st.markdown("<div class='metric-label'>Portfolio Risk — After</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-big'>{new_risk}/100</div>", unsafe_allow_html=True)
            st.markdown(pill(f"Risk increased by {data['risk_delta']}%", "red"), unsafe_allow_html=True)
            glass_end()

        fig = go.Figure(go.Bar(
            x=list(impact_items.keys()), y=list(impact_items.values()),
            marker_color=["#4ce6a8" if v >= 0 else "#ff7b8f" for v in impact_items.values()],
        ))
        fig.update_layout(
            title="Sector Impact Breakdown", template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380,
            font=dict(color="#d8d9f0"),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select a scenario and click **Run Simulation** to see AI-projected portfolio impact.")

    footer()

# ============================================================
# PAGE 5 — ALPHA DISCOVERY ENGINE
# ============================================================
elif page == PAGES[4]:
    header("Alpha Discovery Engine", "AI-surfaced early-stage opportunities")

    sectors = ["All"] + sorted(ALPHA_COMPANIES["Sector"].unique().tolist())
    sector_filter = st.selectbox("Filter by sector", sectors)

    df = ALPHA_COMPANIES if sector_filter == "All" else ALPHA_COMPANIES[ALPHA_COMPANIES["Sector"] == sector_filter]

    for _, row in df.iterrows():
        glass_start()
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {row['Company']}")
            st.markdown(pill(row["Sector"], "blue"), unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-label'>OmniSight Score</div><div class='metric-big'>{row['Score']}/100</div>", unsafe_allow_html=True)

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.markdown("**Hiring Growth**")
            st.markdown(pill(f"+{row['Hiring']}%", "green"), unsafe_allow_html=True)
        with s2:
            st.markdown("**Patent Activity**")
            st.markdown(pill(row["Patents"], "purple"), unsafe_allow_html=True)
        with s3:
            st.markdown("**Factory Expansion**")
            st.markdown(pill(row["Expansion"], "blue"), unsafe_allow_html=True)
        with s4:
            st.markdown("**Institutional Interest**")
            st.markdown(pill(row["Institutional"], "green"), unsafe_allow_html=True)

        st.markdown(
            f"<div class='ai-bubble' style='margin-top:14px'>🧠 <b>AI Insight:</b> {row['Company']} is showing "
            f"early expansion indicators compared with industry peers, driven by hiring velocity and "
            f"{row['Patents'].lower()} patent filing activity.</div>",
            unsafe_allow_html=True,
        )
        glass_end()

    footer()

# ============================================================
# PAGE 6 — WHALE TRACKING
# ============================================================
elif page == PAGES[5]:
    header("Whale Tracking", "Simulated institutional activity monitor")

    st.subheader("Institutional Buying Activity")
    cols = st.columns(len(WHALE_COMPANIES))
    for col, (_, row) in zip(cols, WHALE_COMPANIES.iterrows()):
        with col:
            glass_start()
            st.markdown(f"**{row['Company']}**")
            kind = "green" if row["Score"] > 70 else ("blue" if row["Score"] > 55 else "purple")
            st.markdown(pill(row["Activity"], kind), unsafe_allow_html=True)
            st.markdown(f"<div class='metric-big'>{row['Score']}</div><div class='metric-label'>Accumulation Score</div>", unsafe_allow_html=True)
            glass_end()

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(
            x=WHALE_COMPANIES["Company"], y=WHALE_COMPANIES["Score"],
            marker_color="#7c5cff",
        ))
        fig.update_layout(title="Institutional Ownership Pressure", template="plotly_dark",
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=360,
                           font=dict(color="#d8d9f0"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        weeks = pd.date_range(end=datetime.today(), periods=12, freq="W")
        flow = np.cumsum(np.random.normal(5, 12, size=12))
        fig2 = go.Figure(go.Scatter(x=weeks, y=flow, mode="lines+markers",
                                     line=dict(color="#35d3ff", width=2)))
        fig2.update_layout(title="Simulated Fund Flows (12wk)", template="plotly_dark",
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=360,
                            font=dict(color="#d8d9f0"))
        st.plotly_chart(fig2, use_container_width=True)

    footer()

# ============================================================
# PAGE 7 — QUANT RESEARCH ENGINE
# ============================================================
elif page == PAGES[6]:
    header("Quant Research Engine", "Factor-based scoring across your holdings")

    company = st.selectbox("Select company", list(QUANT_SCORES.keys()))
    scores = QUANT_SCORES[company]
    overall = round(sum(scores.values()) / len(scores))

    c1, c2 = st.columns([1, 1])
    with c1:
        categories = list(scores.keys()) + [list(scores.keys())[0]]
        values = list(scores.values()) + [list(scores.values())[0]]
        fig = go.Figure(go.Scatterpolar(
            r=values, theta=categories, fill="toself",
            line=dict(color="#7c5cff"), fillcolor="rgba(124,92,255,0.25)",
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 100], color="#8b8fc0", gridcolor="rgba(124,92,255,0.2)"),
                angularaxis=dict(color="#d8d9f0", gridcolor="rgba(124,92,255,0.2)"),
            ),
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            title=f"{company} — Factor Radar", height=420,
            font=dict(color="#d8d9f0"), showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        glass_start()
        st.markdown(f"### {company}")
        for factor, val in scores.items():
            st.markdown(f"<div class='metric-label'>{factor}</div>", unsafe_allow_html=True)
            st.progress(val / 100)
            st.markdown(f"<div style='text-align:right;color:#8b8fc0;font-size:0.85rem'>{val}/100</div>", unsafe_allow_html=True)
        glass_end()
        glass_start()
        st.markdown("<div class='metric-label'>Overall OmniSight Score</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-big' style='font-size:2.6rem'>{overall}/100</div>", unsafe_allow_html=True)
        glass_end()

    footer()

# ============================================================
# PAGE 8 — B2B INSTITUTIONAL DASHBOARD
# ============================================================
elif page == PAGES[7]:
    header("OmniSight Institutional Intelligence OS", "Built for hedge funds, PMS firms & small-cap funds")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Reports Generated", "247")
    with c2:
        st.metric("Alpha Opportunities", "36")
    with c3:
        st.metric("Risk Alerts", "12")
    with c4:
        st.metric("AUM Monitored", "₹5,000 Cr")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.subheader("Institutional Feature Suite")

    features = [
        ("🤖", "AI Research Agent", "Autonomous equity research reports generated on-demand across sectors."),
        ("📈", "Quant Research Lab", "Multi-factor scoring, backtesting sandbox, and signal discovery."),
        ("🛡️", "Risk Officer AI", "Continuous portfolio risk monitoring with automated alerting."),
        ("🏛️", "Investment Committee Assistant", "Meeting-ready briefs summarizing exposure, alpha, and risk."),
    ]
    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            glass_start()
            st.markdown(f"<div style='font-size:2rem'>{icon}</div>", unsafe_allow_html=True)
            st.markdown(f"**{title}**")
            st.markdown(f"<span style='color:#8b8fc0;font-size:0.85rem'>{desc}</span>", unsafe_allow_html=True)
            glass_end()

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.subheader("Fund Monitoring Snapshot")
    months = pd.date_range(end=datetime.today(), periods=12, freq="M")
    aum = 4200 + np.cumsum(np.random.normal(70, 40, size=12))
    fig = go.Figure(go.Scatter(x=months, y=aum, mode="lines", fill="tozeroy",
                                line=dict(color="#a05cff", width=2), fillcolor="rgba(160,92,255,0.1)"))
    fig.update_layout(title="Simulated AUM Growth (₹ Cr)", template="plotly_dark",
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380,
                       font=dict(color="#d8d9f0"))
    st.plotly_chart(fig, use_container_width=True)

    footer()

# ============================================================
# PAGE 9 — PRICING
# ============================================================
elif page == PAGES[8]:
    header("Subscription Plans", "Choose the OmniSight tier that fits you")

    st.subheader("Individual Investors")
    cols = st.columns(4)
    for col, plan in zip(cols, PRICING_B2C):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="{'border:1px solid #7c5cff; box-shadow:0 0 30px rgba(124,92,255,0.25);' if plan['highlight'] else ''} text-align:center;">
                {"<span class='pill pill-purple'>MOST POPULAR</span><br/><br/>" if plan['highlight'] else ""}
                <div style="font-family:'Space Grotesk';font-size:1.3rem;font-weight:700;">{plan['name']}</div>
                <div class="metric-big" style="margin-top:8px;">{plan['price']}<span style="font-size:1rem;color:#8b8fc0">{plan['period']}</span></div>
                <hr class='section-divider'/>
                {"<br/>".join(f"✓ {f}" for f in plan['features'])}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.button(f"Choose {plan['name']}", key=f"b2c_{plan['name']}", use_container_width=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.subheader("Institutional / B2B")
    cols2 = st.columns(4)
    for col, plan in zip(cols2, PRICING_B2B):
        with col:
            glass_start()
            st.markdown(f"**{plan['name']}**")
            st.markdown(f"<div class='metric-big'>{plan['price']}<span style='font-size:0.9rem;color:#8b8fc0'>{plan['period']}</span></div>", unsafe_allow_html=True)
            glass_end()

    footer()