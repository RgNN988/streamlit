import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.processing import (
    apply_filters, q6_sales_by_segment_year, q6_pivot,
    q7_discount_simulation, q8_avg_before_after,
    q9_avg_by_segment_year_month, q10_sales_by_category_subcat,
)
from src.visualizations import grouped_bar_chart, line_chart, COLORS
from src.styles import page_header, question_header, insight_box

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

page_header("Perguntas 6 a 10", f"{len(df):,} registros · simulador avançado de desconto disponível", "📈")


def answer_box(text: str):
    st.markdown(f"""
    <div style="background:#0d2137; border:1px solid #58A6FF;
                border-radius:10px; padding:1rem 1.3rem;
                margin-bottom:1.2rem; font-size:0.95rem; color:#E6EDF3; line-height:1.7;">
        <span style="color:#58A6FF; font-weight:700; font-size:0.8rem;
                     text-transform:uppercase; letter-spacing:0.08em;">
            ✅ Resposta da Questão
        </span><br>{text}
    </div>
    """, unsafe_allow_html=True)


# ── Q6 ────────────────────────────────────────────────────────────────────────
question_header("6", "Qual o total de vendas por segmento e por ano?")
result_q6 = q6_sales_by_segment_year(df)
pivot_q6 = q6_pivot(df)

if result_q6.empty:
    st.warning("Sem dados para os filtros selecionados.")
else:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Tabela: Segmento × Ano (R$)**")
        st.dataframe(
            pivot_q6.style.format("R$ {:,.0f}").background_gradient(cmap="Blues"),
            use_container_width=True,
        )
        st.download_button("⬇️ CSV", result_q6.to_csv(index=False).encode("utf-8"),
                           "q6_segmento_ano.csv", mime="text/csv")
    with col2:
        r6 = result_q6.copy()
        r6["Year"] = r6["Year"].astype(str)
        st.plotly_chart(
            grouped_bar_chart(r6, x="Year", y="Sales", color="Segment",
                              title="Vendas por Segmento e Ano"),
            use_container_width=True,
        )

    anos = sorted(result_q6["Year"].unique().tolist())
    if len(anos) >= 2:
        r6a = result_q6.copy()
        r6a["Year"] = r6a["Year"].astype(str)
        ano_ini, ano_fim = str(anos[0]), str(anos[-1])
        crescimento = {}
        for seg in r6a["Segment"].unique():
            vi = r6a[(r6a["Segment"] == seg) & (r6a["Year"] == ano_ini)]["Sales"]
            vf = r6a[(r6a["Segment"] == seg) & (r6a["Year"] == ano_fim)]["Sales"]
            if len(vi) > 0 and len(vf) > 0 and vi.values[0] > 0:
                crescimento[seg] = (vf.values[0] - vi.values[0]) / vi.values[0] * 100
        if crescimento:
            seg_lider = max(crescimento, key=crescimento.get)
            insight_box(
                f"Entre {ano_ini} e {ano_fim}, o maior crescimento foi no segmento "
                f"<b>{seg_lider}</b> (+{crescimento[seg_lider]:.1f}%). A análise por ano "
                f"revela tendências de expansão ou retração por segmento."
            )

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Q7 ────────────────────────────────────────────────────────────────────────
question_header("7", "Quantas vendas teriam 15% de desconto? (regra: vendas > R$ 1.000)")

# Resposta fixa com parâmetro original da questão (threshold = 1000)
res_q7_fixed = q7_discount_simulation(df, threshold=1000)

answer_box(
    f"Aplicando a regra da questão — vendas <b>acima de R$ 1.000</b> recebem <b>15% de desconto</b> "
    f"e as demais recebem <b>10%</b> — do total de <b>{res_q7_fixed['total_orders']:,} pedidos</b>, "
    f"<b>{res_q7_fixed['count_15pct']:,} pedidos ({res_q7_fixed['pct_15pct']}%)</b> receberiam "
    f"15% de desconto, e <b>{res_q7_fixed['count_10pct']:,} pedidos</b> receberiam 10%."
)

c1, c2, c3 = st.columns(3)
c1.metric("📦 Total de Pedidos", f"{res_q7_fixed['total_orders']:,}")
c2.metric("✅ Receberiam 15% (> R$ 1.000)", f"{res_q7_fixed['count_15pct']:,}")
c3.metric("📊 Percentual com 15%", f"{res_q7_fixed['pct_15pct']}%")

col_pie, col_dl = st.columns([2, 1])
with col_pie:
    fig_q7 = go.Figure(go.Pie(
        labels=["15% de desconto", "10% de desconto"],
        values=[res_q7_fixed["count_15pct"], res_q7_fixed["count_10pct"]],
        hole=0.45,
        marker_colors=[COLORS[0], COLORS[2]],
        textinfo="percent",
        textfont=dict(size=14),
        hovertemplate="<b>%{label}</b><br>%{value:,} pedidos (%{percent})<extra></extra>",
    ))
    fig_q7.update_layout(
        title="Pedidos por faixa de desconto",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=10, l=10, r=10),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.2,
            xanchor="center", x=0.5,
            font=dict(size=12),
        ),
        annotations=[dict(
            text=f"{res_q7_fixed['pct_15pct']}%<br>com 15%",
            x=0.5, y=0.5, font_size=14, showarrow=False,
            font=dict(color="#E6EDF3"),
        )],
    )
    st.plotly_chart(fig_q7, use_container_width=True)

with col_dl:
    df_q7_dl = df[["Order ID", "Sales"]].copy()
    df_q7_dl["Desconto Aplicado"] = np.where(df["Sales"] > 1000, "15%", "10%")
    st.download_button("⬇️ CSV Q7", df_q7_dl.to_csv(index=False).encode("utf-8"),
                       "q7_simulacao.csv", mime="text/csv")

insight_box(
    f"<b>{res_q7_fixed['count_15pct']:,} pedidos</b> ({res_q7_fixed['pct_15pct']}% do total) "
    f"superam R$ 1.000 e se qualificam para o desconto premium de 15%. "
    f"Isso representa uma política que incentiva compras de alto valor enquanto mantém "
    f"margem nos pedidos menores."
)

with st.expander("🔬 Simulador Avançado — explore outros limites"):
    threshold_q7 = st.slider("Alterar limite para 15% de desconto (R$)", 500, 3000, 1000, 100, key="q7_thr")
    res_sim = q7_discount_simulation(df, threshold=threshold_q7)
    s1, s2, s3 = st.columns(3)
    s1.metric("Total de Pedidos", f"{res_sim['total_orders']:,}")
    s2.metric(f"Receberiam 15% (> R$ {threshold_q7:,})", f"{res_sim['count_15pct']:,}")
    s3.metric("Percentual com 15%", f"{res_sim['pct_15pct']}%")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Q8 ────────────────────────────────────────────────────────────────────────
question_header("8", "Qual a média de vendas antes e após aplicar 15% de desconto (vendas > R$ 1.000)?")

# Resposta fixa com parâmetros originais da questão
res_q8_fixed = q8_avg_before_after(df, threshold=1000, rate_high=0.15, rate_low=0.10)

answer_box(
    f"Usando a regra da questão — <b>15% de desconto</b> para vendas acima de R$ 1.000 "
    f"e <b>10%</b> para as demais — a média de vendas <b>antes</b> do desconto é "
    f"<b>R$ {res_q8_fixed['avg_before']:,.2f}</b> e <b>após</b> o desconto cai para "
    f"<b>R$ {res_q8_fixed['avg_after']:,.2f}</b>, uma redução de "
    f"<b>R$ {abs(res_q8_fixed['delta']):,.2f} ({abs(res_q8_fixed['delta_pct']):.1f}%)</b>."
)

c1, c2, c3 = st.columns(3)
c1.metric("📊 Média Antes do Desconto", f"R$ {res_q8_fixed['avg_before']:,.2f}")
c2.metric(
    "💸 Média Após Desconto",
    f"R$ {res_q8_fixed['avg_after']:,.2f}",
    delta=f"R$ {res_q8_fixed['delta']:,.2f} ({res_q8_fixed['delta_pct']:.1f}%)",
    delta_color="inverse",
)
c3.metric(
    "📉 Impacto Total Estimado",
    f"R$ {abs(res_q8_fixed['delta'] * len(df)):,.0f}",
    delta="Redução de receita bruta",
    delta_color="inverse",
)

fig_q8 = go.Figure()
fig_q8.add_trace(go.Bar(
    name="Antes do desconto", x=["Média de Vendas"],
    y=[res_q8_fixed["avg_before"]], marker_color=COLORS[0],
))
fig_q8.add_trace(go.Bar(
    name="Após desconto (15%/>1k | 10%/demais)", x=["Média de Vendas"],
    y=[res_q8_fixed["avg_after"]], marker_color=COLORS[2],
))
fig_q8.update_layout(
    title="Média de Vendas: Antes vs. Após Desconto (parâmetros da questão)",
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    barmode="group",
    yaxis_title="Valor Médio (R$)",
    margin=dict(t=50, b=10),
)
st.plotly_chart(fig_q8, use_container_width=True)

insight_box(
    f"A redução média de <b>R$ {abs(res_q8_fixed['delta']):,.2f} por pedido</b> "
    f"({abs(res_q8_fixed['delta_pct']):.1f}%) parece pequena individualmente, mas multiplicada "
    f"pelos {len(df):,} pedidos representa uma renúncia de receita de "
    f"<b>R$ {abs(res_q8_fixed['delta'] * len(df)):,.0f}</b>. "
    f"O impacto real depende se o desconto gera aumento proporcional no volume de vendas."
)

with st.expander("🔬 Simulador Avançado — ajuste os parâmetros"):
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        thr = st.slider("Limite (R$)", 500, 3000, 1000, 100, key="q8_thr")
    with sc2:
        rh = st.slider("Taxa alta (%)", 10, 30, 15, 1, key="q8_rh") / 100
    with sc3:
        rl = st.slider("Taxa baixa (%)", 5, 20, 10, 1, key="q8_rl") / 100
    res_sim8 = q8_avg_before_after(df, threshold=thr, rate_high=rh, rate_low=rl)
    sa1, sa2, sa3 = st.columns(3)
    sa1.metric("Média Antes", f"R$ {res_sim8['avg_before']:,.2f}")
    sa2.metric("Média Após", f"R$ {res_sim8['avg_after']:,.2f}",
               delta=f"{res_sim8['delta_pct']:.1f}%", delta_color="inverse")
    sa3.metric("Impacto Total", f"R$ {abs(res_sim8['delta'] * len(df)):,.0f}")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Q9 ────────────────────────────────────────────────────────────────────────
question_header("9", "Qual a média de vendas por segmento, ano e mês?")
result_q9 = q9_avg_by_segment_year_month(df)

if result_q9.empty:
    st.warning("Sem dados suficientes.")
else:
    # ── Resposta explícita: tabela resumo Segmento × Ano ──────────────────────
    q9_summary = (
        result_q9.groupby(["Segment", "Year"])["Sales"]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"Sales": "Média Mensal (R$)"})
    )
    q9_pivot_display = (
        q9_summary.pivot(index="Segment", columns="Year", values="Média Mensal (R$)")
        .round(2)
    )
    q9_pivot_display.columns = [str(c) for c in q9_pivot_display.columns]

    top_avg = result_q9.loc[result_q9["Sales"].idxmax()]
    top_seg_geral = result_q9.groupby("Segment")["Sales"].mean().idxmax()
    top_seg_val = result_q9.groupby("Segment")["Sales"].mean().max()

    answer_box(
        f"A tabela abaixo mostra a <b>média mensal de vendas</b> por segmento e ano. "
        f"O maior valor de média mensal registrado foi <b>R$ {top_avg['Sales']:,.2f}</b>, "
        f"ocorrido em <b>{top_avg['Period']}</b> no segmento <b>{top_avg['Segment']}</b>. "
        f"Considerando todo o período, o segmento com maior média geral é "
        f"<b>{top_seg_geral}</b> (R$ {top_seg_val:,.2f}/mês em média)."
    )

    col_tbl, col_chart = st.columns([1, 2])
    with col_tbl:
        st.markdown("**Média mensal de vendas por segmento e ano (R$)**")
        st.dataframe(
            q9_pivot_display.style.format("R$ {:,.2f}").background_gradient(cmap="Blues"),
            use_container_width=True,
        )
        st.download_button("⬇️ CSV Q9", result_q9.to_csv(index=False).encode("utf-8"),
                           "q9_media_segmento_mes.csv", mime="text/csv")

    with col_chart:
        anos_disp = sorted(result_q9["Year"].unique().tolist())
        anos_sel = st.multiselect(
            "Filtrar anos no gráfico", options=anos_disp, default=anos_disp, key="q9_years"
        )
        data_q9 = result_q9[result_q9["Year"].isin(anos_sel)] if anos_sel else result_q9
        st.plotly_chart(
            line_chart(data_q9, x="Period", y="Sales", color="Segment",
                       title="Média de Vendas por Segmento ao Longo do Tempo"),
            use_container_width=True,
        )

    insight_box(
        f"Pico de média mensal: <b>R$ {top_avg['Sales']:,.2f}</b> em "
        f"<b>{top_avg['Period']}</b> (segmento <b>{top_avg['Segment']}</b>). "
        f"Segmentos apresentam sazonalidades distintas — padrões ligados a "
        f"ciclos de orçamento corporativo ou comportamento do consumidor."
    )

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ── Q10 ───────────────────────────────────────────────────────────────────────
question_header("10", "Qual o total de vendas por categoria e top 12 subcategorias?")
result_q10 = q10_sales_by_category_subcat(df, top_n=12)

if result_q10.empty:
    st.warning("Sem dados para os filtros selecionados.")
else:
    top_sub = result_q10.iloc[0]
    soma_top12 = result_q10["Sales"].sum()
    soma_total = df.groupby("Sub-Category")["Sales"].sum().sum()
    pct_top12 = soma_top12 / soma_total * 100 if soma_total > 0 else 0

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("🏆 Top Subcategoria", top_sub["Sub-Category"])
        st.metric("Categoria", top_sub["Category"])
        st.metric("Vendas", f"R$ {top_sub['Sales']:,.2f}")
        st.metric("Top 12 concentra", f"{pct_top12:.1f}%")
        st.download_button("⬇️ CSV Q10", result_q10.to_csv(index=False).encode("utf-8"),
                           "q10_categoria_subcat.csv", mime="text/csv")
    with col2:
        st.plotly_chart(
            grouped_bar_chart(
                result_q10, x="Sub-Category", y="Sales", color="Category",
                title="Top 12 Subcategorias por Categoria",
            ),
            use_container_width=True,
        )

    top3_sub = result_q10.head(3)["Sub-Category"].tolist()
    top_cat = result_q10.groupby("Category")["Sales"].sum().idxmax()
    insight_box(
        f"As <b>top 12 subcategorias</b> representam <b>{pct_top12:.1f}%</b> das vendas. "
        f"Pódio: <b>{', '.join(top3_sub)}</b>. "
        f"A categoria <b>{top_cat}</b> tem maior volume agregado. "
        f"Subcategorias de alto valor justificam marketing específico e gestão dedicada de estoque."
    )
