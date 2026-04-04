import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from util.style    import inject_css, kpi, insight, section_header, data_row, get_layout, hex_to_rgba, C
from util.data     import load_exp_vinhos, load_exp_espumantes, load_exp_suco, load_exp_uvas
from util.layout   import sidebar
from util.constants import PAIS_COLORS

inject_css(); sidebar()

ev = load_exp_vinhos()
ee = load_exp_espumantes()
es = load_exp_suco()
eu = load_exp_uvas()

st.markdown(
    f'<h1 style="font-family:Playfair Display,serif;2.185rem;font-weight:700;'
    f'color:{C["cream"]};margin:0 0 0.2rem;">✈️ Exportações</h1>'
    f'<div style="0.943rem;color:{C["muted"]};margin-bottom:1.1rem;">'
    f'Vinhos, espumantes, suco e uvas · kg e USD · 1970–2019</div>',
    unsafe_allow_html=True
)

# ── KPIs ──────────────────────────────────────────────────────
ev_yr  = ev.groupby("ano")[["kg","usd"]].sum()
ee_yr  = ee.groupby("ano")[["kg","usd"]].sum()
es_yr  = es.groupby("ano")[["kg","usd"]].sum()
eu_yr  = eu.groupby("ano")[["kg","usd"]].sum()

total_usd_2019 = (ev_yr.loc[2019,"usd"] + ee_yr.loc[2019,"usd"] +
                  es_yr.loc[2019,"usd"] + eu_yr.loc[2019,"usd"])

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(kpi(f"${total_usd_2019/1e6:.1f}M", "Total exportado 2019",
    "Vinhos + espumantes + suco + uvas", C["gold"], "💰"), unsafe_allow_html=True)
with c2: st.markdown(kpi(f"${ee_yr.loc[2019,'usd']/1e6:.1f}M", "Espumantes 2019",
    f"+{(ee_yr.loc[2019,'usd']/ee_yr.loc[2000,'usd']-1)*100:.0f}% desde 2000", C["rose"], "🥂"), unsafe_allow_html=True)
with c3: st.markdown(kpi(f"${es_yr.loc[2019,'usd']/1e6:.1f}M", "Suco de Uva 2019",
    "Maior produto de exportação", C["green"], "🥤"), unsafe_allow_html=True)
with c4: st.markdown(kpi(f"{eu_yr.loc[2019,'kg']/1e3:.0f} t", "Uvas Frescas 2019",
    f"${eu_yr.loc[2019,'usd']/1e6:.1f}M", C["purple"], "🍇"), unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🍷 Vinhos de Mesa", "🥂 Espumantes", "🥤 Suco de Uva", "🍇 Uvas Frescas"])

# ── TAB 1: VINHOS DE MESA ─────────────────────────────────────
with tab1:
    st.markdown(section_header("EXPORTAÇÃO DE VINHOS DE MESA", "Volume e receita por destino"), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ev_yr.index, y=ev_yr["kg"]/1e3,
            name="Volume (ton)", marker_color=hex_to_rgba(C["rose"], 0.75),
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} toneladas<extra></extra>"))
        fig.update_layout(**get_layout(height=280, yaxis_title="Toneladas"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ev_yr.index, y=ev_yr["usd"]/1e6,
            mode="lines+markers", fill="tozeroy",
            line=dict(color=C["gold"], width=2),
            fillcolor=hex_to_rgba(C["gold"], 0.12),
            hovertemplate="<b>%{x}</b><br>$%{y:.1f}M<extra></extra>"))
        fig2.update_layout(**get_layout(height=280, yaxis_title="USD (milhões)"))
        st.plotly_chart(fig2, use_container_width=True)

    # Top destinos 2019
    top_dest = ev[ev["ano"] == 2019].sort_values("usd", ascending=False).head(10)
    st.markdown(section_header("TOP DESTINOS 2019", "Quem compra vinho brasileiro"), unsafe_allow_html=True)
    fig3 = go.Figure(go.Bar(
        y=top_dest["pais"], x=top_dest["usd"]/1e3,
        orientation="h",
        marker_color=[PAIS_COLORS.get(p, C["dim"]) for p in top_dest["pais"]],
        text=[f"${v/1e3:.0f}k" for v in top_dest["usd"]],
        textposition="outside", textfont=dict(color=C["muted"], size=12),
    ))
    ly = get_layout(height=340, xaxis_title="USD (mil)", margin=dict(l=16,r=80,t=20,b=16))
    ly["yaxis"] = dict(**get_layout()["yaxis"], categoryorder="total ascending")
    fig3.update_layout(**ly)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(insight(
        "<strong>O mercado de vinho de mesa é volátil:</strong> o pico de 2009 (~25.000 ton) "
        "foi seguido por colapso em 2010 (~1.300 ton). "
        "A exportação de vinhos de mesa sofre com a competição de Chile, Argentina e Portugal no mercado global. "
        "O foco estratégico da indústria brasileira migrou para espumantes e suco.",
        "alert"
    ), unsafe_allow_html=True)

# ── TAB 2: ESPUMANTES ─────────────────────────────────────────
with tab2:
    st.markdown(section_header("EXPORTAÇÃO DE ESPUMANTES", "O produto premium brasileiro em ascensão"), unsafe_allow_html=True)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=ee_yr.index, y=ee_yr["kg"]/1e3,
        name="Volume (ton)", marker_color=hex_to_rgba(C["gold"], 0.7),
        hovertemplate="<b>%{x}</b><br>%{y:,.1f} ton<extra></extra>"))
    fig4.add_trace(go.Scatter(x=ee_yr.index, y=ee_yr["usd"]/1e6,
        name="Receita (USD M)", mode="lines+markers",
        line=dict(color=C["rose"], width=2), marker=dict(size=6),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>$%{y:.2f}M<extra></extra>"))
    fig4.update_layout(**get_layout(
        height=320,
        yaxis=dict(**get_layout()["yaxis"], title="Toneladas"),
        yaxis2=dict(overlaying="y", side="right", title="USD (M)",
                    gridcolor="rgba(0,0,0,0)",
                    tickfont=dict(color=C["muted"]),
                    title_font=dict(color=C["muted"])),
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
    ))
    st.plotly_chart(fig4, use_container_width=True)

    # Top destinos espumantes
    top_esp_dest = ee[ee["ano"] == 2019].sort_values("usd", ascending=False).head(10)
    c1, c2 = st.columns([3,2])
    with c1:
        fig5 = go.Figure(go.Bar(
            y=top_esp_dest["pais"], x=top_esp_dest["usd"]/1e3,
            orientation="h",
            marker_color=hex_to_rgba(C["gold"], 0.75),
            text=[f"${v/1e3:.0f}k" for v in top_esp_dest["usd"]],
            textposition="outside", textfont=dict(color=C["muted"], size=12),
        ))
        ly2 = get_layout(height=320, xaxis_title="USD (mil)", margin=dict(l=16,r=80,t=20,b=16))
        ly2["yaxis"] = dict(**get_layout()["yaxis"], categoryorder="total ascending")
        fig5.update_layout(**ly2)
        st.plotly_chart(fig5, use_container_width=True)
    with c2:
        st.markdown(insight(
            f"<strong>Espumantes: o produto de maior crescimento.</strong> "
            f"De $0 em 1985 para ${ee_yr.loc[2019,'usd']/1e6:.1f}M em 2019. "
            "O Brasil se especializou em Moscatel e Brut — "
            "competindo com Prosecco italiano e Cava espanhol na América Latina.",
            "growth"
        ), unsafe_allow_html=True)
        st.markdown(insight(
            "<strong>Preço médio por kg cresceu:</strong> "
            f"em 2010 era ${ee_yr.loc[2010,'usd']/max(ee_yr.loc[2010,'kg'],1):.2f}/kg. "
            f"Em 2019 chegou a ${ee_yr.loc[2019,'usd']/max(ee_yr.loc[2019,'kg'],1):.2f}/kg. "
            "O valor unitário dobrou — mais do que volume, a indústria ganhou em qualidade percebida.",
            "wine"
        ), unsafe_allow_html=True)

# ── TAB 3: SUCO DE UVA ────────────────────────────────────────
with tab3:
    st.markdown(section_header("EXPORTAÇÃO DE SUCO", "O campeão de receita"), unsafe_allow_html=True)

    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(x=es_yr.index, y=es_yr["kg"]/1e6,
        mode="lines", fill="tozeroy",
        line=dict(color=C["green"], width=2),
        fillcolor=hex_to_rgba(C["green"], 0.15),
        name="Volume (M kg)",
        hovertemplate="<b>%{x}</b><br>%{y:.1f} M kg<extra></extra>"))
    fig6.add_trace(go.Scatter(x=es_yr.index, y=es_yr["usd"]/1e6,
        mode="lines", line=dict(color=C["gold"], width=2, dash="dash"),
        name="Receita (USD M)", yaxis="y2",
        hovertemplate="<b>%{x}</b><br>$%{y:.1f}M<extra></extra>"))
    fig6.update_layout(**get_layout(
        height=340,
        yaxis=dict(**get_layout()["yaxis"], title="Kg (milhões)"),
        yaxis2=dict(overlaying="y", side="right", title="USD (M)",
                    gridcolor="rgba(0,0,0,0)",
                    tickfont=dict(color=C["muted"]),
                    title_font=dict(color=C["muted"])),
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
    ))
    st.plotly_chart(fig6, use_container_width=True)

    top_suco = es[es["ano"] == 2019].sort_values("usd", ascending=False).head(8)
    fig7 = go.Figure(go.Bar(
        x=[p[:20] for p in top_suco["pais"]], y=top_suco["usd"]/1e6,
        marker_color=hex_to_rgba(C["green"], 0.75),
        text=[f"${v/1e6:.1f}M" for v in top_suco["usd"]],
        textposition="outside", textfont=dict(color=C["muted"]),
    ))
    fig7.update_layout(**get_layout(height=280, yaxis_title="USD (milhões)"))
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown(insight(
        f"<strong>O suco de uva é o maior gerador de receita de exportação:</strong> "
        f"${es_yr.loc[2019,'usd']/1e6:.1f}M em 2019. "
        "O Brasil compete com EUA e Argentina no mercado global. "
        "A concentração em alguns poucos compradores (Estados Unidos, Japão, Europa) "
        "cria risco de dependência, mas também estabilidade contratual de longo prazo.",
        "info"
    ), unsafe_allow_html=True)

# ── TAB 4: UVAS FRESCAS ───────────────────────────────────────
with tab4:
    st.markdown(section_header("EXPORTAÇÃO DE UVAS FRESCAS", "In natura · mercado premium"), unsafe_allow_html=True)

    fig8 = go.Figure()
    fig8.add_trace(go.Bar(x=eu_yr.index, y=eu_yr["kg"]/1e3,
        marker_color=hex_to_rgba(C["purple"], 0.7),
        name="Volume (ton)",
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} ton<extra></extra>"))
    fig8.add_trace(go.Scatter(x=eu_yr.index, y=eu_yr["usd"]/1e6,
        mode="lines+markers", line=dict(color=C["gold"], width=2),
        name="Receita (USD M)", yaxis="y2",
        hovertemplate="<b>%{x}</b><br>$%{y:.1f}M<extra></extra>"))
    fig8.update_layout(**get_layout(
        height=320,
        yaxis=dict(**get_layout()["yaxis"], title="Toneladas"),
        yaxis2=dict(overlaying="y", side="right", title="USD (M)",
                    gridcolor="rgba(0,0,0,0)",
                    tickfont=dict(color=C["muted"]),
                    title_font=dict(color=C["muted"])),
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
    ))
    st.plotly_chart(fig8, use_container_width=True)

    # Price per kg evolution
    eu_yr["usd_per_kg"] = eu_yr["usd"] / eu_yr["kg"].replace(0, np.nan)
    fig9 = go.Figure(go.Scatter(
        x=eu_yr.index, y=eu_yr["usd_per_kg"],
        mode="lines+markers", line=dict(color=C["rose"], width=2),
        hovertemplate="<b>%{x}</b><br>$%{y:.2f}/kg<extra></extra>",
    ))
    fig9.update_layout(**get_layout(height=220, yaxis_title="USD/kg médio",
                                     title=dict(text="Preço médio de exportação de uva fresca")))
    st.plotly_chart(fig9, use_container_width=True)

    st.markdown(insight(
        "<strong>Uvas frescas: mercado de nicho com alto valor unitário.</strong> "
        "O preço por kg é o mais alto entre todos os produtos exportados. "
        "O mercado é dominado por uvas sem sementes (seedless), "
        "que alcançam mercados premium na Europa e nos EUA.",
        "wine"
    ), unsafe_allow_html=True)
