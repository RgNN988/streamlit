import streamlit as st
from src.connection import load_raw_data
from src.processing import clean_data
from src.styles import inject_css

st.set_page_config(
    page_title="Superstore Analytics | ITAJR",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Dados ────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def get_clean_data():
    return clean_data(load_raw_data())

with st.spinner("Conectando ao Supabase..."):
    df_full = get_clean_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1.2rem 0;
                border-bottom: 1px solid rgba(255,255,255,0.08);
                margin-bottom: 0.8rem;'>
        <div style='font-size:1.05rem; font-weight:700; color:#E6EDF3; letter-spacing:-0.01em;'>
            📊 Superstore Analytics
        </div>
        <div style='font-size:0.72rem; color:#8B949E; margin-top:0.2rem;'>
            Python ITA Júnior 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Filtros**")

    years_available = sorted(df_full["Year"].dropna().astype(int).unique().tolist())
    year_range = st.select_slider(
        "Período (ano)",
        options=years_available,
        value=(years_available[0], years_available[-1]),
    )

    all_regions = sorted(df_full["Region"].dropna().unique().tolist())
    regions = st.multiselect("Região", options=all_regions)

    available_states = (
        sorted(df_full[df_full["Region"].isin(regions)]["State"].dropna().unique().tolist())
        if regions else sorted(df_full["State"].dropna().unique().tolist())
    )
    states = st.multiselect("Estado", options=available_states)

    available_cities = (
        sorted(df_full[df_full["State"].isin(states)]["City"].dropna().unique().tolist())
        if states else sorted(df_full["City"].dropna().unique().tolist())
    )
    cities = st.multiselect("Cidade", options=available_cities)

    all_segments = sorted(df_full["Segment"].dropna().unique().tolist())
    segments = st.multiselect("Segmento", options=all_segments)

    all_categories = sorted(df_full["Category"].dropna().unique().tolist())
    categories = st.multiselect("Categoria", options=all_categories)

    available_subcats = (
        sorted(df_full[df_full["Category"].isin(categories)]["Sub-Category"].dropna().unique().tolist())
        if categories else sorted(df_full["Sub-Category"].dropna().unique().tolist())
    )
    subcategories = st.multiselect("Subcategoria", options=available_subcats)

    st.markdown("---")
    top_n = st.slider("Top N (rankings)", min_value=5, max_value=20, value=10)

    st.markdown("---")
    total_records = len(df_full)
    st.markdown(f"""
    <div style='font-size:0.72rem; color:#8B949E; line-height:1.7;'>
        🗄️ {total_records:,} registros no banco<br>
        🔄 Cache renovado a cada hora
    </div>
    """, unsafe_allow_html=True)

# Persistir filtros no session_state
st.session_state["filters"] = {
    "year_range": year_range if len(year_range) == 2 else None,
    "regions": regions or None,
    "states": states or None,
    "cities": cities or None,
    "segments": segments or None,
    "categories": categories or None,
    "subcategories": subcategories or None,
    "top_n": top_n,
}
st.session_state["df_full"] = df_full

# ── Navegação ────────────────────────────────────────────────────────────────
home   = st.Page("pages/home.py",   title="Visão Geral",    icon="🏠", default=True)
p1_5   = st.Page("pages/q1_5.py",   title="Perguntas 1-5",  icon="📊")
p6_10  = st.Page("pages/q6_10.py",  title="Perguntas 6-10", icon="📈")

pg = st.navigation([home, p1_5, p6_10])
pg.run()
