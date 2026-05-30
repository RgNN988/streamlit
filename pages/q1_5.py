import streamlit as st
import pandas as pd
from src.processing import (
    apply_filters, q1_city_office_supplies, q2_sales_by_date,
    q3_sales_by_state, q4_top_cities, q5_sales_by_segment,
)
from src.visualizations import bar_chart, bar_chart_h, pie_chart
from src.styles import page_header, question_header, insight_box

df_full = st.session_state.get("df_full", pd.DataFrame())
f = st.session_state.get("filters", {})
top_n = f.get("top_n", 10)

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

page_header("Perguntas 1 a 5", f"{len(df):,} registros · use os filtros na barra lateral", "📊")

# ── Q1 ────────────────────────────────────────────────────────────────────────
question_header("1", "Qual cidade tem maior valor de vendas para a categoria Office Supplies?")
result_q1 = q1_city_office_supplies(df)

if result_q1.empty:
    st.warning("Sem dados de Office Supplies para os filtros selecionados.")
else:
    top = result_q1.iloc[0]
    pct = top["Sales"] / result_q1["Sales"].sum() * 100

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("🏆 Cidade Campeã", top["City"])
        st.metric("Total de Vendas", f"R$ {top['Sales']:,.2f}")
        st.metric("Participação na Categoria", f"{pct:.1f}%")
        st.download_button("⬇️ CSV", result_q1.to_csv(index=False).encode("utf-8"),
                           "q1_office_supplies.csv", mime="text/csv")
    with col2:
        st.plotly_chart(
            bar_chart(result_q1.head(10), x="City", y="Sales", title="Top 10 Cidades — Office Supplies"),
            use_container_width=True,
        )
    insight_box(
        f"<b>{top['City']}</b> lidera Office Supplies com <b>R$ {top['Sales']:,.2f}</b> "
        f"({pct:.1f}% da categoria). Isso indica concentração de demanda por materiais de escritório "
        f"nessa localidade, sugerindo oportunidade de distribuição dedicada."
    )

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Q2 ────────────────────────────────────────────────────────────────────────
question_header("2", "Qual o total de vendas por data de pedido?")
result_q2 = q2_sales_by_date(df)

if result_q2.empty:
    st.warning("Sem dados para o período selecionado.")
else:
    pico = result_q2.loc[result_q2["Sales"].idxmax()]
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Total Geral", f"R$ {result_q2['Sales'].sum():,.0f}")
        st.metric("Melhor Mês", pico["Year-Month"])
        st.metric("Vendas no Pico", f"R$ {pico['Sales']:,.2f}")
        st.download_button("⬇️ CSV", result_q2.to_csv(index=False).encode("utf-8"),
                           "q2_vendas_por_data.csv", mime="text/csv")
    with col2:
        st.plotly_chart(
            bar_chart(result_q2, x="Year-Month", y="Sales", title="Vendas por Mês/Ano"),
            use_container_width=True,
        )
    insight_box(
        f"Maior volume em <b>{pico['Year-Month']}</b> com <b>R$ {pico['Sales']:,.2f}</b>. "
        f"O gráfico revela sazonalidade: picos recorrentes podem indicar datas comemorativas "
        f"ou ciclos de compras corporativas — informação vital para planejamento de estoque."
    )

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Q3 ────────────────────────────────────────────────────────────────────────
question_header("3", "Qual o total de vendas por estado?")
result_q3 = q3_sales_by_state(df)

if result_q3.empty:
    st.warning("Sem dados para os filtros selecionados.")
else:
    top_s = result_q3.iloc[0]
    pct_s = top_s["Sales"] / result_q3["Sales"].sum() * 100
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("🏆 Estado Líder", top_s["State"])
        st.metric("Vendas", f"R$ {top_s['Sales']:,.2f}")
        st.metric("Participação", f"{pct_s:.1f}%")
        st.download_button("⬇️ CSV", result_q3.to_csv(index=False).encode("utf-8"),
                           "q3_vendas_por_estado.csv", mime="text/csv")
    with col2:
        # ascending → estado líder aparece no TOPO do gráfico horizontal
        q3_chart = result_q3.head(15).sort_values("Sales", ascending=True)
        st.plotly_chart(
            bar_chart_h(q3_chart, x="Sales", y="State",
                        title="Top 15 Estados por Total de Vendas"),
            use_container_width=True,
        )
    top3 = result_q3.head(3)["State"].tolist()
    insight_box(
        f"<b>{top_s['State']}</b> lidera com <b>R$ {top_s['Sales']:,.2f}</b> "
        f"({pct_s:.1f}% do total). Pódio: <b>{', '.join(top3)}</b>. "
        f"Essa concentração regional deve direcionar esforços comerciais e decisões logísticas."
    )

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Q4 ────────────────────────────────────────────────────────────────────────
question_header("4", f"Quais as Top {top_n} cidades com maior total de vendas?")
result_q4 = q4_top_cities(df, top_n=top_n)

if result_q4.empty:
    st.warning("Sem dados para os filtros selecionados.")
else:
    top_c = result_q4.iloc[0]
    soma_top = result_q4["Sales"].sum()
    soma_total = df.groupby("City")["Sales"].sum().sum()
    pct_top = soma_top / soma_total * 100 if soma_total > 0 else 0

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(f"🏆 1ª Cidade", top_c["City"])
        st.metric("Vendas", f"R$ {top_c['Sales']:,.2f}")
        st.metric(f"Top {top_n} concentra", f"{pct_top:.1f}% das vendas")
        st.dataframe(
            result_q4.rename(columns={"City": "Cidade", "Sales": "Vendas (R$)"})
            .style.format({"Vendas (R$)": "{:,.2f}"}),
            use_container_width=True, hide_index=True,
        )
        st.download_button("⬇️ CSV", result_q4.to_csv(index=False).encode("utf-8"),
                           "q4_top_cidades.csv", mime="text/csv")
    with col2:
        st.plotly_chart(
            bar_chart(result_q4, x="City", y="Sales", title=f"Top {top_n} Cidades"),
            use_container_width=True,
        )
    insight_box(
        f"As <b>top {top_n} cidades</b> concentram <b>{pct_top:.1f}%</b> das vendas "
        f"(R$ {soma_top:,.0f}). Alta concentração urbana de receita indica que ações "
        f"focadas nessas cidades têm potencial de retorno elevado sobre o investimento."
    )

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Q5 ────────────────────────────────────────────────────────────────────────
question_header("5", "Qual segmento possui o maior total de vendas?")
result_q5 = q5_sales_by_segment(df)

if result_q5.empty:
    st.warning("Sem dados para os filtros selecionados.")
else:
    top_seg = result_q5.iloc[0]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("🏆 Segmento Líder", top_seg["Segment"])
        st.metric("Vendas", f"R$ {top_seg['Sales']:,.2f}")
        st.metric("Participação", f"{top_seg['Percentual']}%")
        st.dataframe(
            result_q5.rename(columns={"Segment": "Segmento", "Sales": "Vendas (R$)", "Percentual": "%"})
            .style.format({"Vendas (R$)": "{:,.2f}", "%": "{:.1f}"}),
            use_container_width=True, hide_index=True,
        )
        st.download_button("⬇️ CSV", result_q5.to_csv(index=False).encode("utf-8"),
                           "q5_segmento.csv", mime="text/csv")
    with col2:
        st.plotly_chart(
            pie_chart(result_q5, names="Segment", values="Sales",
                      title="Distribuição por Segmento"),
            use_container_width=True,
        )
    perfil = (
        "consumidores individuais são o principal motor de receita"
        if top_seg["Segment"] == "Consumer"
        else "o segmento corporativo tem alta penetração em empresas"
    )
    insight_box(
        f"<b>{top_seg['Segment']}</b> domina com <b>{top_seg['Percentual']}%</b> "
        f"(R$ {top_seg['Sales']:,.0f}). Isso significa que {perfil}, o que deve "
        f"guiar estratégias de precificação, mix de produtos e canais de venda."
    )
