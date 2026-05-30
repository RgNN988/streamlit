import streamlit as st
import pandas as pd
from src.processing import apply_filters, get_data_quality_report
from src.visualizations import bar_chart
from src.styles import page_header

df_full = st.session_state.get("df_full", pd.DataFrame())
f = st.session_state.get("filters", {})

df = apply_filters(
    df_full,
    year_range=f.get("year_range"),
    regions=f.get("regions"),
    states=f.get("states"),
    cities=f.get("cities"),
    segments=f.get("segments"),
    categories=f.get("categories"),
    subcategories=f.get("subcategories"),
)

page_header(
    "Superstore Analytics",
    f"Visão geral do negócio · {len(df):,} registros selecionados",
    "🏠",
)

# ── KPIs ─────────────────────────────────────────────────────────────────────
total_sales   = df["Sales"].sum()
total_orders  = df["Order ID"].nunique()
total_profit  = df["Profit"].sum()
avg_ticket    = df["Sales"].mean()
margin        = (total_profit / total_sales * 100) if total_sales > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Total de Vendas",  f"R$ {total_sales:,.0f}")
c2.metric("📦 Pedidos Únicos",   f"{total_orders:,}")
c3.metric("📈 Lucro Total",      f"R$ {total_profit:,.0f}")
c4.metric("🎯 Ticket Médio",     f"R$ {avg_ticket:,.2f}")
c5.metric("📊 Margem de Lucro",  f"{margin:.1f}%")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Gráficos de visão geral ───────────────────────────────────────────────────
col_l, col_r = st.columns([3, 2])

with col_l:
    st.markdown("#### Evolução Mensal de Vendas")
    trend = (
        df.groupby("Year-Month", as_index=False)["Sales"]
        .sum()
        .sort_values("Year-Month")
    )
    fig = bar_chart(trend, x="Year-Month", y="Sales", title="")
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.markdown("#### Vendas por Categoria")
    cat = df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    for _, row in cat.iterrows():
        pct = row["Sales"] / total_sales * 100 if total_sales > 0 else 0
        st.metric(row["Category"], f"R$ {row['Sales']:,.0f}", f"{pct:.1f}% do total")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Pedidos por Segmento")
    seg = df.groupby("Segment", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    for _, row in seg.iterrows():
        pct = row["Sales"] / total_sales * 100 if total_sales > 0 else 0
        st.metric(row["Segment"], f"R$ {row['Sales']:,.0f}", f"{pct:.1f}%")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Download e qualidade ──────────────────────────────────────────────────────
col_d, col_q = st.columns([1, 2])
with col_d:
    st.markdown("#### ⬇️ Download")
    st.download_button(
        label="Baixar dataset completo (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="superstore_filtrado.csv",
        mime="text/csv",
        use_container_width=True,
    )

with col_q:
    with st.expander("🔍 Qualidade dos Dados & Limitações"):
        report = get_data_quality_report(df_full)
        st.markdown(f"**Total no banco:** {report['total_rows']:,}  |  **Com filtros:** {len(df):,}")
        if report["nulls_per_column"]:
            st.markdown("**Valores nulos:**")
            st.json(report["nulls_per_column"])
        else:
            st.success("Sem valores nulos nas colunas principais.")
        st.info(
            "**Limitações conhecidas:**\n"
            "- `Sales`, `Profit` e `Discount` são strings com vírgula decimal (convertidos automaticamente)\n"
            "- Datas em DD/MM/YYYY (convertidas para datetime)\n"
            "- Simulação de desconto (Q7/Q8) é hipotética — não reflete política real"
        )
