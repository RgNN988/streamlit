import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLORS = [
    "#58A6FF", "#3FB950", "#F78166", "#D2A8FF",
    "#FFA657", "#79C0FF", "#56D364", "#FF7B72",
]
PRIMARY = "#58A6FF"
TEMPLATE = "plotly_dark"

_LAYOUT_BASE = dict(
    template=TEMPLATE,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=50, b=10, l=10, r=10),
    font=dict(color="#C9D1D9"),
)


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    orientation: str = "v",
    color: str = None,
    top_n: int = None,
    color_seq=None,
) -> go.Figure:
    data = df.copy()
    if top_n:
        data = data.head(top_n)

    kwargs = dict(
        x=x,
        y=y,
        orientation=orientation,
        title=title,
        color_discrete_sequence=color_seq or [PRIMARY],
        template=TEMPLATE,
        labels={y: "Vendas (R$)", x: x},
    )
    if color:
        kwargs["color"] = color
        kwargs["color_discrete_sequence"] = color_seq or COLORS

    fig = px.bar(data, **kwargs)
    if orientation == "v":
        fig.update_traces(hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>")
    else:
        fig.update_traces(hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>")
    fig.update_layout(
        **_LAYOUT_BASE,
        showlegend=bool(color),
        xaxis_tickangle=-35 if orientation == "v" else 0,
    )
    return fig


def bar_chart_h(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    n = len(df)
    # gradiente azul: barras menores mais escuras, maior mais brilhante
    opacity = [0.3 + 0.7 * i / max(n - 1, 1) for i in range(n)]
    colors = [f"rgba(88, 166, 255, {o:.2f})" for o in opacity]

    fig = go.Figure(go.Bar(
        x=df[x],
        y=df[y],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"R$ {v / 1_000:.0f}k" for v in df[x]],
        textposition="outside",
        textfont=dict(size=11, color="#C9D1D9"),
        hovertemplate="<b>%{y}</b><br>R$ %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title=title,
        template=TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(color="#C9D1D9"),
        height=max(380, n * 28),
        margin=dict(t=50, b=10, l=10, r=90),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            tickformat="$.2s",
            range=[0, df[x].max() * 1.22],
        ),
        yaxis=dict(showgrid=False, tickfont=dict(size=12)),
    )
    return fig


def pie_chart(df: pd.DataFrame, names: str, values: str, title: str) -> go.Figure:
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        color_discrete_sequence=COLORS,
        template=TEMPLATE,
        hole=0.4,
    )
    fig.update_traces(
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
    )
    fig.update_layout(**_LAYOUT_BASE)
    return fig


def line_chart(
    df: pd.DataFrame, x: str, y: str, color: str, title: str
) -> go.Figure:
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        markers=True,
        template=TEMPLATE,
        color_discrete_sequence=COLORS,
        labels={y: "Vendas Médias (R$)", x: x},
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>%{x}<br>R$ %{y:,.2f}<extra></extra>"
    )
    fig.update_layout(**_LAYOUT_BASE, xaxis_tickangle=-35)
    return fig


def grouped_bar_chart(
    df: pd.DataFrame, x: str, y: str, color: str, title: str, barmode: str = "group"
) -> go.Figure:
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        barmode=barmode,
        title=title,
        template=TEMPLATE,
        color_discrete_sequence=COLORS,
        labels={y: "Vendas (R$)", x: x},
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>%{x}<br>R$ %{y:,.2f}<extra></extra>"
    )
    fig.update_layout(**_LAYOUT_BASE, xaxis_tickangle=-35)
    return fig
