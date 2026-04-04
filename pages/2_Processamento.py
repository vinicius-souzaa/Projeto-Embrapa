import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from util.style    import inject_css, kpi, insight, section_header, data_row, get_layout, hex_to_rgba, C
from util.data     import (load_uvas_americanas, load_uvas_viniferas,
                           load_uvas_mesa, load_uvas_sem_class)
from util.layout   import sidebar

inject_css(); sidebar()

amer  = load_uvas_americanas()
vinif = load_uvas_viniferas()
mesa  = load_uvas_mesa()
sc    = load_uvas_sem_class()

st.markdown(
    f'<h1 style="font-family:Playfair Display,serif;font-size:1.9rem;font-weight:700;'
    f'color:{C["cream"]};margin:0 0 0.2rem;">🍇 Processamento de Uvas</h1>'
    f'<div style="font-size:0.82rem;color:{C["muted"]};margin-bottom:1.1rem;">'
    f'Kilos processados por tipo de uva · 1970–2018</div>',
    unsafe_allow_html=True
)

amer_yr  = amer.groupby("ano")["valor"].sum()
vinif_yr = vinif.groupby("ano")["valor"].sum()
mesa_yr  = mesa.groupby("ano")["valor"].sum()

# KPIs
c1, c2, c3, c4 = st.columns(4)
pct_amer  = amer_yr[2018] / (amer_yr[2018] + vinif_yr[2018] + mesa_yr[2018]) * 100
pct_vinif = vinif_yr[2018] / (amer_yr[2018] + vinif_yr[2018] + mesa_yr[2018]) * 100

with c1: st.markdown(kpi(f"{amer_yr[2018]/1e6:.0f}M kg", "Americanas (2018)",
    f"{pct_amer:.0f}% do total", C["purple"], "🍇"), unsafe_allow_html=True)
with c2: st.markdown(kpi(f"{vinif_yr[2018]/1e6:.0f}M kg", "Viníferas (2018)",
    f"{pct_vinif:.0f}% do total", C["gold"], "🍾"), unsafe_allow_html=True)
with c3: st.markdown(kpi(f"{amer_yr.idxmax()}", "Melhor ano americanas",
    f"{amer_yr.max()/1e6:.0f}M kg", C["rose"], "📈"), unsafe_allow_html=True)
with c4: st.markdown(kpi(f"-{(1-amer_yr[2016]/amer_yr[2015])*100:.0f}%", "Queda em 2016",
    "Geada · ambas categorias", C["red"], "🌨️"), unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🍇 Americanas & Híbridas", "🍷 Viníferas Finas", "📊 Comparativo"])

# ── TAB 1: AMERICANAS ─────────────────────────────────────────
with tab1:
    st.markdown(section_header("UVAS AMERICANAS E HÍBRIDAS",
        "A base da produção de vinho de mesa e suco"), unsafe_allow_html=True)
    st.caption("Principais variedades: Isabel, Concord, Bordô, Niágara, Jacquez, BRS Cora")

    # Top 10 varieties
    top_amer = amer[~amer["categoria"].isin(["TINTAS","BRANCAS","ROSADAS"])]\
        .groupby("categoria")["valor"].sum().sort_values(ascending=False).head(12)

    fig1 = go.Figure(go.Bar(
        y=top_amer.index, x=[v/1e6 for v in top_amer.values],
        orientation="h",
        marker_color=[C["purple"] if i == 0 else hex_to_rgba(C["purple"], 0.6)
                      for i in range(len(top_amer))],
        text=[f"{v/1e6:.0f}M" for v in top_amer.values],
        textposition="outside", textfont=dict(color=C["muted"], size=10),
        hovertemplate="%{y}<br>%{x:.0f} M kg total<extra></extra>",
    ))
    ly = get_layout(height=420, xaxis_title="Kilos (milhões) — total 1970–2018",
                    margin=dict(l=16, r=60, t=30, b=16))
    ly["yaxis"] = dict(**get_layout()["yaxis"], categoryorder="total ascending")
    fig1.update_layout(**ly)
    st.plotly_chart(fig1, use_container_width=True)

    # Evolution top 5 varieties
    top5 = top_amer.head(5).index.tolist()
    fig2 = go.Figure()
    colors5 = [C["purple"], C["rose"], C["gold"], C["green"], C["muted"]]
    for var, color in zip(top5, colors5):
        sub = amer[amer["categoria"] == var].groupby("ano")["valor"].sum()
        if len(sub) == 0: continue
        fig2.add_trace(go.Scatter(
            x=sub.index, y=[v/1e6 for v in sub.values],
            mode="lines", name=var.strip(),
            line=dict(color=color, width=1.8),
            hovertemplate=f"<b>%{{x}}</b> · {var.strip()}<br>%{{y:.0f}} M kg<extra></extra>",
        ))
    fig2.add_vrect(x0=2015.5, x1=2016.5, fillcolor=C["red"], opacity=0.12)
    fig2.update_layout(**get_layout(height=300, yaxis_title="Kilos (milhões)",
                                     legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center")))
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(insight(
        "<strong>Isabel é a rainha das americanas:</strong> a variedade mais processada por ampla margem, "
        "presente em praticamente todos os anos da série. As uvas americanas são mais resistentes às doenças "
        "e ao clima do Rio Grande do Sul, tornando-as a base econômica da vitivinicultura familiar.",
        "wine"
    ), unsafe_allow_html=True)

# ── TAB 2: VINÍFERAS ──────────────────────────────────────────
with tab2:
    st.markdown(section_header("UVAS VINÍFERAS", "Variedades europeias — vinhos finos brasileiros"), unsafe_allow_html=True)
    st.caption("Principais: Cabernet Sauvignon, Merlot, Chardonnay, Moscato, Pinot Noir, Tannat")

    top_vinif = vinif[~vinif["categoria"].isin(["TINTAS","BRANCAS","ROSADAS"])]\
        .groupby("categoria")["valor"].sum().sort_values(ascending=False).head(12)

    fig3 = go.Figure(go.Bar(
        y=top_vinif.index, x=[v/1e6 for v in top_vinif.values],
        orientation="h",
        marker_color=[C["gold"] if i == 0 else hex_to_rgba(C["gold"], 0.6)
                      for i in range(len(top_vinif))],
        text=[f"{v/1e6:.1f}M" for v in top_vinif.values],
        textposition="outside", textfont=dict(color=C["muted"], size=10),
    ))
    ly2 = get_layout(height=420, xaxis_title="Kilos (milhões) — total 1970–2018",
                     margin=dict(l=16, r=60, t=30, b=16))
    ly2["yaxis"] = dict(**get_layout()["yaxis"], categoryorder="total ascending")
    fig3.update_layout(**ly2)
    st.plotly_chart(fig3, use_container_width=True)

    # Growth of fine varieties
    cab_sauv = vinif[vinif["categoria"].str.contains("Cabernet Sauvignon", na=False)]\
        .groupby("ano")["valor"].sum()
    merlot   = vinif[vinif["categoria"].str.contains("Merlot", na=False)]\
        .groupby("ano")["valor"].sum()
    moscato  = vinif[vinif["categoria"].str.contains("Moscato", na=False)]\
        .groupby("ano")["valor"].sum()

    fig4 = go.Figure()
    for name, sub, color in [("Cabernet Sauvignon", cab_sauv, C["red"]),
                               ("Merlot", merlot, C["rose"]),
                               ("Moscato", moscato, C["gold"])]:
        if len(sub) > 0:
            fig4.add_trace(go.Scatter(
                x=sub.index, y=[v/1e3 for v in sub.values],
                mode="lines", name=name, line=dict(color=color, width=2),
                hovertemplate=f"<b>%{{x}}</b> · {name}<br>%{{y:.0f}} mil kg<extra></extra>",
            ))
    fig4.update_layout(**get_layout(height=280, yaxis_title="Kilos (mil)",
                                     legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center")))
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(insight(
        "<strong>As viníferas cresceram 400% em 40 anos:</strong> de menos de 50M kg nos anos 70 "
        "para mais de 150M kg nos anos 2010. O Cabernet Sauvignon lidera entre as tintas, "
        "enquanto o Moscato domina as brancas — base dos espumantes moscatel brasileiros.",
        "growth"
    ), unsafe_allow_html=True)

# ── TAB 3: COMPARATIVO ────────────────────────────────────────
with tab3:
    st.markdown(section_header("COMPARATIVO", "Americanas vs Viníferas — evolução relativa"), unsafe_allow_html=True)

    # Proportional stacked area
    total_yr = amer_yr + vinif_yr + mesa_yr
    pct_amer_yr  = amer_yr  / total_yr * 100
    pct_vinif_yr = vinif_yr / total_yr * 100
    pct_mesa_yr  = mesa_yr  / total_yr * 100

    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=pct_amer_yr.index, y=pct_amer_yr.values,
        mode="lines", fill="tozeroy", name="Americanas/Híbridas",
        line=dict(color=C["purple"], width=0), fillcolor=hex_to_rgba(C["purple"], 0.6),
    ))
    fig5.add_trace(go.Scatter(
        x=pct_vinif_yr.index, y=(pct_amer_yr + pct_vinif_yr).values,
        mode="lines", fill="tonexty", name="Viníferas",
        line=dict(color=C["gold"], width=0), fillcolor=hex_to_rgba(C["gold"], 0.6),
    ))
    fig5.add_trace(go.Scatter(
        x=pct_mesa_yr.index, y=(pct_amer_yr + pct_vinif_yr + pct_mesa_yr).values,
        mode="lines", fill="tonexty", name="Mesa",
        line=dict(color=C["rose"], width=0), fillcolor=hex_to_rgba(C["rose"], 0.4),
    ))
    fig5.update_layout(**get_layout(
        height=340, yaxis_title="% do total processado",
        yaxis_range=[0, 100],
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
    ))
    st.plotly_chart(fig5, use_container_width=True)

    # Total volume comparison
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=amer_yr.index, y=[v/1e6 for v in amer_yr.values],
        mode="lines", name="Americanas", line=dict(color=C["purple"], width=2),
    ))
    fig6.add_trace(go.Scatter(
        x=vinif_yr.index, y=[v/1e6 for v in vinif_yr.values],
        mode="lines", name="Viníferas", line=dict(color=C["gold"], width=2),
    ))
    fig6.add_vrect(x0=2015.5, x1=2016.5, fillcolor=C["red"], opacity=0.12,
                   annotation_text="Geada 2016", annotation_font_color=C["red"])
    fig6.update_layout(**get_layout(height=280, yaxis_title="Kilos (milhões)",
                                     legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center")))
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown(insight(
        "<strong>A geada de 2016 atingiu ambas as categorias com intensidade similar:</strong> "
        f"americanas caíram de {amer_yr.get(2015,0)/1e6:.0f}M para {amer_yr.get(2016,0)/1e6:.0f}M kg (−{(1-amer_yr.get(2016,0)/amer_yr.get(2015,1))*100:.0f}%), "
        f"viníferas de {vinif_yr.get(2015,0)/1e6:.0f}M para {vinif_yr.get(2016,0)/1e6:.0f}M kg. "
        "A recuperação total veio já em 2017, demonstrando a resiliência da Serra Gaúcha.",
        "alert"
    ), unsafe_allow_html=True)
