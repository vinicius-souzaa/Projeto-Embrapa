import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from util.style    import inject_css, kpi, insight, section_header, data_row, get_layout, hex_to_rgba, C
from util.data     import load_producao, load_comercializacao
from util.layout   import sidebar
from util.constants import EVENTS, DECADES

inject_css(); sidebar()

prod = load_producao()
com  = load_comercializacao()

st.markdown(
    f'<h1 style="font-family:Playfair Display,serif;font-size:1.9rem;font-weight:700;'
    f'color:{C["cream"]};margin:0 0 0.2rem;">🍷 Produção & Comercialização</h1>'
    f'<div style="font-size:0.82rem;color:{C["muted"]};margin-bottom:1.1rem;">'
    f'Vinhos, sucos e derivados · litros · 1970–2019</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["🍷 Produção por produto", "🛒 Comercialização", "📅 Análise por década"])

# ── TAB 1: PRODUÇÃO ───────────────────────────────────────────
with tab1:
    st.markdown(section_header("PRODUÇÃO", "Todos os produtos — 1970 a 2019"), unsafe_allow_html=True)

    # Top-level categories only
    top_cats = ["VINHO DE MESA", "VINHO FINO DE MESA (VINÍFERA)", "SUCO", "DERIVADOS"]
    cat_colors = [C["rose"], C["purple"], C["green"], C["gold"]]

    fig = go.Figure()
    for cat, color in zip(top_cats, cat_colors):
        sub = prod[prod["categoria"] == cat].groupby("ano")["valor"].sum()
        if len(sub) == 0: continue
        fig.add_trace(go.Scatter(
            x=sub.index, y=[v/1e6 for v in sub.values],
            mode="lines", name=cat.title(),
            line=dict(color=color, width=2),
            hovertemplate=f"<b>%{{x}}</b> · {cat}<br>%{{y:.1f}} M L<extra></extra>",
        ))

    # Geada 2016
    fig.add_vrect(x0=2015.5, x1=2016.5, fillcolor=C["red"], opacity=0.12,
                  annotation_text="⚠️ Geada 2016",
                  annotation_font_color=C["red"], annotation_position="top left")

    fig.update_layout(**get_layout(
        height=420, yaxis_title="Litros (milhões)",
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Subcategories of Vinho de Mesa
    st.markdown(section_header("VINHO DE MESA", "Composição — Tinto, Branco, Rosado"), unsafe_allow_html=True)
    sub_cats = ["Tinto", "Branco", "Rosado"]
    sub_colors = [C["red"], C["cream"], C["rose"]]
    fig2 = go.Figure()
    for cat, color in zip(sub_cats, sub_colors):
        sub = prod[prod["categoria"] == cat].groupby("ano")["valor"].sum()
        if len(sub) == 0: continue
        fig2.add_trace(go.Bar(
            x=sub.index, y=[v/1e6 for v in sub.values],
            name=cat, marker_color=hex_to_rgba(color, 0.8),
            hovertemplate=f"<b>%{{x}}</b> · {cat}<br>%{{y:.1f}} M L<extra></extra>",
        ))
    fig2.add_vrect(x0=2015.5, x1=2016.5, fillcolor=C["red"], opacity=0.12)
    fig2.update_layout(**get_layout(height=300, barmode="stack", yaxis_title="Litros (milhões)",
                                     legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center")))
    st.plotly_chart(fig2, use_container_width=True)

    tinto = prod[prod["categoria"] == "Tinto"].groupby("ano")["valor"].sum()
    branco = prod[prod["categoria"] == "Branco"].groupby("ano")["valor"].sum()
    pct_tinto_2019 = tinto[2019] / (tinto[2019] + branco[2019]) * 100 if 2019 in tinto.index else 0

    st.markdown(insight(
        f"<strong>O Tinto domina, mas o Branco cresce:</strong> em 2019, o vinho tinto representou "
        f"{pct_tinto_2019:.0f}% do vinho de mesa produzido. O vinho branco vem ganhando espaço "
        "especialmente a partir dos anos 2000, acompanhando mudanças no consumo brasileiro.",
        "wine"
    ), unsafe_allow_html=True)

    # Suco de uva breakdown
    st.markdown(section_header("SUCO DE UVA", "Integral vs Concentrado — crescimento explosivo"), unsafe_allow_html=True)
    suco_cats = ["Suco de uva integral", "Suco de uva concentrado"]
    suco_colors = [C["green"], "#8FBC3A"]
    fig3 = go.Figure()
    for cat, color in zip(suco_cats, suco_colors):
        sub = prod[prod["categoria"] == cat].groupby("ano")["valor"].sum()
        if len(sub) == 0: continue
        fig3.add_trace(go.Scatter(
            x=sub.index, y=[v/1e6 for v in sub.values],
            mode="lines+markers", name=cat,
            line=dict(color=color, width=2), marker=dict(size=4),
            hovertemplate=f"<b>%{{x}}</b><br>%{{y:.1f}} M L<extra></extra>",
        ))
    fig3.update_layout(**get_layout(height=280, yaxis_title="Litros (milhões)",
                                     legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center")))
    st.plotly_chart(fig3, use_container_width=True)

    suco = prod[prod["categoria"] == "SUCO"].groupby("ano")["valor"].sum()
    st.markdown(insight(
        f"<strong>O suco de uva é a grande estrela da vitivinicultura brasileira:</strong> "
        f"saltou de {suco.get(1990,0)/1e6:.0f}M L em 1990 para {suco.get(2019,0)/1e6:.0f}M L em 2019. "
        "Crescimento de +430% em 30 anos. O Brasil se consolidou como um dos maiores produtores mundiais de suco de uva.",
        "growth"
    ), unsafe_allow_html=True)

# ── TAB 2: COMERCIALIZAÇÃO ────────────────────────────────────
with tab2:
    st.markdown(section_header("COMERCIALIZAÇÃO", "O que chega ao mercado interno"), unsafe_allow_html=True)

    com_cats = [
        ("VINHO DE MESA",                C["rose"]),
        ("VINHO  FINO DE MESA",          C["purple"]),
        ("ESPUMANTES",                   C["gold"]),
        ("SUCO DE UVAS",                 C["green"]),
        ("OUTROS PRODUTOS COMERCIALIZADOS", C["muted"]),
    ]

    fig4 = go.Figure()
    for cat, color in com_cats:
        sub = com[com["categoria"] == cat].groupby("ano")["valor"].sum()
        if len(sub) == 0: continue
        fig4.add_trace(go.Scatter(
            x=sub.index, y=[v/1e6 for v in sub.values],
            mode="lines", name=cat.title().replace("  "," "),
            line=dict(color=color, width=2),
            hovertemplate=f"<b>%{{x}}</b><br>%{{y:.1f}} M L/kg<extra></extra>",
        ))
    fig4.add_vrect(x0=2015.5, x1=2016.5, fillcolor=C["red"], opacity=0.12,
                   annotation_text="Geada 2016", annotation_font_color=C["red"])
    fig4.update_layout(**get_layout(height=380, yaxis_title="Litros/Kilos (milhões)",
                                     legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center")))
    st.plotly_chart(fig4, use_container_width=True)

    # Espumantes destaque
    esp = com[com["categoria"] == "ESPUMANTES"].groupby("ano")["valor"].sum()
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=esp.index, y=[v/1e6 for v in esp.values],
        mode="lines+markers", fill="tozeroy",
        line=dict(color=C["gold"], width=2.5),
        fillcolor=hex_to_rgba(C["gold"], 0.12),
        hovertemplate="<b>%{x}</b><br>%{y:.2f} M L<extra></extra>",
    ))
    fig5.update_layout(**get_layout(height=260, yaxis_title="Litros (milhões)",
                                     title=dict(text="Espumantes — crescimento 1970–2019", font=dict(color=C["cream"]))))
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown(insight(
        f"<strong>Espumantes: de nicho a fenômeno nacional.</strong> "
        f"Em 2000, comercializavam-se 4,3M L. Em 2019, {esp.get(2019,0)/1e6:.1f}M L — "
        f"crescimento de {(esp.get(2019,0)/esp.get(2000,0)-1)*100:.0f}%. "
        "O Brasil passou a competir internacionalmente com Prosecco e Cava, principalmente na América do Sul.",
        "growth"
    ), unsafe_allow_html=True)

# ── TAB 3: POR DÉCADA ─────────────────────────────────────────
with tab3:
    st.markdown(section_header("ANÁLISE POR DÉCADA", "Como cada período moldou a vitivinicultura"), unsafe_allow_html=True)

    vm = prod[prod["categoria"] == "VINHO DE MESA"].groupby("ano")["valor"].sum()
    suco = prod[prod["categoria"] == "SUCO"].groupby("ano")["valor"].sum()
    dec_labels = ["Anos 70", "Anos 80", "Anos 90", "Anos 2000", "Anos 2010"]

    dec_cols = st.columns(5)
    for i, (dec_start, dec_label) in enumerate(zip([1970,1980,1990,2000,2010], dec_labels)):
        dec_end = dec_start + 9
        mask = (vm.index >= dec_start) & (vm.index <= dec_end)
        sub = vm[mask]
        if len(sub) == 0: continue
        avg = sub.mean() / 1e6
        best = sub.idxmax()
        worst = sub.idxmin()
        dec_colors = [C["muted"], C["rose"], C["purple"], C["green"], C["gold"]]
        color = dec_colors[i]

        dec_cols[i].markdown(f"""
        <div style="background:{C['surface']};border:1px solid {C['border']};
                    border-radius:8px;padding:0.9rem;border-top:2px solid {color};">
            <div style="font-size:0.62rem;color:{C['muted']};text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:0.3rem;">{dec_label}</div>
            <div style="font-family:Playfair Display,serif;font-size:1.5rem;
                        font-weight:700;color:{color};line-height:1;">{avg:.0f}M L</div>
            <div style="font-size:0.7rem;color:{C['muted']};margin-top:0.4rem;">média/ano</div>
            <div style="margin-top:0.5rem;font-size:0.71rem;">
                {data_row("Melhor", str(best), C["green"])}
                {data_row("Pior", str(worst), C["red"])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Radar chart — mix de produtos por década
    prod_decades = {}
    for dec_start, dec_label in zip([1990, 2000, 2010], ["Anos 90", "Anos 2000", "Anos 2010"]):
        mask = (prod["ano"] >= dec_start) & (prod["ano"] <= dec_start + 9)
        sub = prod[mask].groupby("categoria")["valor"].sum()
        for cat in ["VINHO DE MESA", "VINHO FINO DE MESA (VINÍFERA)", "SUCO", "DERIVADOS"]:
            prod_decades.setdefault(cat, {})[dec_label] = sub.get(cat, 0) / 1e6

    fig6 = go.Figure()
    decade_colors_r = [C["rose"], C["gold"], C["green"]]
    for dec_label, color in zip(["Anos 90", "Anos 2000", "Anos 2010"], decade_colors_r):
        cats = list(prod_decades.keys())
        vals = [prod_decades[c].get(dec_label, 0) for c in cats]
        fig6.add_trace(go.Bar(
            x=cats, y=vals, name=dec_label,
            marker_color=hex_to_rgba(color, 0.75),
        ))
    fig6.update_layout(**get_layout(height=320, barmode="group",
                                     yaxis_title="Litros (milhões) — total da década",
                                     legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
                                     xaxis=dict(**get_layout()["xaxis"], tickangle=-15, tickfont=dict(size=10))))
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown(insight(
        "<strong>A transição entre décadas revela uma estratégia:</strong> nos Anos 90 o vinho de mesa "
        "dominava com folga. Nos Anos 2000 o suco de uva explodiu em volume. "
        "Nos Anos 2010 o mix se diversificou com espumantes e vinhos finos — "
        "indicando uma indústria que migrou do volume para o valor.",
        "wine"
    ), unsafe_allow_html=True)
