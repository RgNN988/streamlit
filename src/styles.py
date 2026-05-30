import streamlit as st

# Dark palette tokens
BG_MAIN   = "#0D1117"
BG_CARD   = "#1C2333"
BG_SIDE   = "#161B27"
BORDER    = "rgba(255,255,255,0.08)"
ACCENT    = "#58A6FF"
TEXT_PRI  = "#E6EDF3"
TEXT_SEC  = "#8B949E"


def inject_css():
    st.markdown(f"""
    <style>
    /* ── Esconde apenas o branding — header fica intacto (mantém toggle da sidebar) ── */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stDecoration"] {{display: none;}}

    /* ── Padding do conteúdo principal ── */
    [data-testid="stAppViewContainer"] > .main > .block-container {{
        padding: 1.5rem 2.5rem 2rem 2.5rem !important;
        max-width: 100% !important;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background-color: {BG_SIDE} !important;
        border-right: 1px solid {BORDER} !important;
    }}
    [data-testid="stSidebar"] label {{
        color: {TEXT_SEC} !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: {BORDER} !important;
    }}

    /* ── Cards de métricas ── */
    [data-testid="metric-container"] {{
        background: {BG_CARD} !important;
        border-radius: 10px !important;
        padding: 1rem 1.2rem !important;
        border: 1px solid {BORDER} !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {TEXT_SEC} !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    [data-testid="stMetricValue"] {{
        color: {TEXT_PRI} !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }}

    /* ── Expanders ── */
    [data-testid="stExpander"] {{
        background: {BG_CARD} !important;
        border-radius: 10px !important;
        border: 1px solid {BORDER} !important;
    }}

    /* ── Dataframes ── */
    [data-testid="stDataFrame"] {{
        border-radius: 10px !important;
        overflow: hidden;
        border: 1px solid {BORDER} !important;
    }}

    /* ── Botões de download ── */
    [data-testid="stDownloadButton"] button {{
        background: {BG_CARD} !important;
        color: {ACCENT} !important;
        border: 1px solid rgba(88,166,255,0.3) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.15s;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        background: rgba(88,166,255,0.12) !important;
        border-color: {ACCENT} !important;
    }}

    /* ── Divisor ── */
    .divider {{
        border: none;
        height: 1px;
        background: {BORDER};
        margin: 2rem 0;
    }}
    </style>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = "📊"):
    st.markdown(f"""
    <div style="padding: 0.5rem 0 1.2rem 0;
                border-bottom: 1px solid rgba(255,255,255,0.08);
                margin-bottom: 1.5rem;">
        <h1 style="margin:0; font-size:1.9rem; font-weight:700; color:{TEXT_PRI};">
            {icon}&nbsp;{title}
        </h1>
        <p style="margin:0.35rem 0 0 0; color:{TEXT_SEC}; font-size:0.88rem;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)


def question_header(number: str, title: str):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.9rem;
                margin: 2rem 0 0.6rem 0;">
        <div style="background:{ACCENT}; color:#0D1117;
                    width:2rem; height:2rem; border-radius:50%;
                    display:flex; align-items:center; justify-content:center;
                    font-weight:800; font-size:0.85rem; flex-shrink:0;">
            {number}
        </div>
        <h3 style="margin:0; color:{TEXT_PRI}; font-size:1rem; font-weight:600;">
            {title}
        </h3>
    </div>
    <hr style="border:none; border-top:1px solid rgba(255,255,255,0.08);
               margin:0.4rem 0 1rem 0;">
    """, unsafe_allow_html=True)


def insight_box(text: str):
    st.markdown(f"""
    <div style="background:{BG_CARD};
                border-left:3px solid {ACCENT};
                border-radius:0 8px 8px 0;
                padding:0.9rem 1.1rem;
                margin-top:0.8rem;
                font-size:0.88rem;
                color:#C9D1D9;
                line-height:1.65;">
        <span style="color:{ACCENT}; font-weight:600;">💡 Insight:</span><br>{text}
    </div>
    """, unsafe_allow_html=True)
