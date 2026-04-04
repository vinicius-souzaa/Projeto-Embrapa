import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from util.style    import inject_css, kpi, insight, section_header, data_row, get_layout, hex_to_rgba, C
from util.data     import (load_imp_vinhos, load_imp_espumantes,
                           load_imp_suco, load_imp_uvas, load_imp_passas)
from util.layout   import sidebar
from util.constants import PAIS_COLORS

inject_css(); sidebar()

iv  = load_imp_vinhos()
ie  = load_imp_espumantes()
is_ = load_imp_suco()
iu  = load_imp_uvas()
ip  = load_imp_passas()

st.markdown(
    f'<h1 style="font-family:Playfair Display,serif;font-size:1.9rem;font-weight:700;'
    f'color:{C["cream"]};margin:0 0 0.2rem;">🛬 Importações</h1>'
    f'<div style="font-size:0.82rem;color:{C["muted"]};margin-bottom:1.1rem;">'
    f'Quem compete com o produto brasileiro · kg e USD · 1970–2019</div>',
    unsafe_allow_html=True
)

iv_yr  = iv.groupby("ano")[["kg","usd"]].sum()
ie_yr  = ie.groupby("ano")[["kg","usd"]].sum()
is_yr  = is_.groupby("ano")[["kg","usd"]].sum()
iu_yr  = iu.groupby("ano")[["kg","usd"]].sum()
ip_yr  = ip.groupby("ano")[["kg","usd"]].sum()

# ── KPIs ──────────────────────────────────────────────────────
total_imp_2019 = (iv_yr.loc[2019,"usd"] + ie_yr.loc[2019,"usd"] +
                  is_yr.loc[2019,"usd"] + iu_yr.loc[2019,"usd"] + ip_yr.loc[2019,"usd"])

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(kpi(f"${total_imp_2019/1e6:.0f}M", "Total importado 2019",
    "Todos os produtos de uva", C["red"], "💸"), unsafe_allow_html=True)
with c2: st.markdown(kpi(f"${iv_yr.loc[2019,'usd']/1e6:.0f}M", "Vinhos de Mesa 2019",
    "Chile + Portugal + Argentina", C["rose"], "🍷"), unsafe_allow_html=True)
with c3: st.markdown(kpi(f"${ie_yr.loc[2019,'usd']/1e6:.0f}M", "Espumantes importados 2019",
    "Itália + França lideram", C["gold"], "🥂"), unsafe_allow_html=True)
with c4:
    arg_pct = iv[iv["pais"] == "Argentina"].groupby("ano")["usd"].sum()
    arg_share = arg_pct.get(2019, 0) / iv_yr.loc[2019, "usd"] * 100 if iv_yr.loc[2019,"usd"] > 0 else 0
    st.markdown(kpi(f"{arg_share:.0f}%", "Argentina no vinho de mesa 2019",
        "Vizinha domina segmento de entrada", C["purple"], "🇦🇷"), unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🍷 Vinhos Importados", "🥂 Espumantes Importados", "🇦🇷 Dependência Argentina", "⚖️ Balança Comercial"])

# ── TAB 1: VINHOS IMPORTADOS ──────────────────────────────────
with tab1:
    st.markdown(section_header("VINHOS DE MESA IMPORTADOS", "50 anos de concorrência externa"), unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=iv_yr.index, y=iv_yr["kg"]/1e6,
        name="Volume (M kg)", marker_color=hex_to_rgba(C["red"], 0.7),
        hovertemplate="<b>%{x}</b><br>%{y:.1f} M kg<extra></extra>"))
    fig.add_trace(go.Scatter(x=iv_yr.index, y=iv_yr["usd"]/1e6,
        mode="lines", line=dict(color=C["gold"], width=2),
        name="Receita (USD M)", yaxis="y2",
        hovertemplate="<b>%{x}</b><br>$%{y:.0f}M<extra></extra>"))

    # Mark 1994 Plano Real
    fig.add_vline(x=1994, line_color=C["gold"], line_dash="dot",
                  annotation_text="Plano Real 1994", annotation_font_color=C["gold"])

    fig.update_layout(**get_layout(
        height=340,
        yaxis=dict(**get_layout()["yaxis"], title="Kg (milhões)"),
        yaxis2=dict(overlaying="y", side="right", title="USD (M)",
                    gridcolor="rgba(0,0,0,0)", tickfont=dict(color=C["muted"]),
                    title_font=dict(color=C["muted"])),
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Top países
    top_imp = iv[iv["ano"] == 2019].sort_values("kg", ascending=False).head(8)
    fig2 = go.Figure(go.Bar(
        y=top_imp["pais"], x=top_imp["kg"]/1e6,
        orientation="h",
        marker_color=[PAIS_COLORS.get(p, C["dim"]) for p in top_imp["pais"]],
        text=[f"{v/1e6:.1f}M kg" for v in top_imp["kg"]],
        textposition="outside", textfont=dict(color=C["muted"], size=10),
    ))
    ly = get_layout(height=320, xaxis_title="Kg (milhões) — 2019", margin=dict(l=16,r=80,t=20,b=16))
    ly["yaxis"] = dict(**get_layout()["yaxis"], categoryorder="total ascending")
    fig2.update_layout(**ly)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(insight(
        "<strong>O Chile domina as importações de vinho:</strong> 52,7M kg em 2019 — "
        "mais que Portugal, Argentina e Itália juntos. "
        "A abertura comercial de 1994 (Plano Real) foi o ponto de inflexão — "
        "o volume importado explodiu nos anos seguintes, pressionando o produtor brasileiro.",
        "alert"
    ), unsafe_allow_html=True)

# ── TAB 2: ESPUMANTES IMPORTADOS ──────────────────────────────
with tab2:
    st.markdown(section_header("ESPUMANTES IMPORTADOS", "Itália, França e Argentina dominam"), unsafe_allow_html=True)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=ie_yr.index, y=ie_yr["kg"]/1e3,
        mode="lines", fill="tozeroy",
        line=dict(color=C["gold"], width=2),
        fillcolor=hex_to_rgba(C["gold"], 0.12),
        name="Volume (ton)",
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} ton<extra></extra>"))
    fig3.add_trace(go.Scatter(x=ie_yr.index, y=ie_yr["usd"]/1e6,
        mode="lines", line=dict(color=C["rose"], width=2, dash="dot"),
        name="Receita (USD M)", yaxis="y2",
        hovertemplate="<b>%{x}</b><br>$%{y:.0f}M<extra></extra>"))
    fig3.update_layout(**get_layout(
        height=300,
        yaxis=dict(**get_layout()["yaxis"], title="Toneladas"),
        yaxis2=dict(overlaying="y", side="right", title="USD (M)",
                    gridcolor="rgba(0,0,0,0)", tickfont=dict(color=C["muted"]),
                    title_font=dict(color=C["muted"])),
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
    ))
    st.plotly_chart(fig3, use_container_width=True)

    top_esp_imp = ie[ie["ano"] == 2019].sort_values("usd", ascending=False).head(8)
    fig4 = go.Figure(go.Bar(
        x=[p[:18] for p in top_esp_imp["pais"]], y=top_esp_imp["usd"]/1e6,
        marker_color=[PAIS_COLORS.get(p, hex_to_rgba(C["gold"], 0.7)) for p in top_esp_imp["pais"]],
        text=[f"${v/1e6:.1f}M" for v in top_esp_imp["usd"]],
        textposition="outside", textfont=dict(color=C["muted"]),
    ))
    fig4.update_layout(**get_layout(height=260, yaxis_title="USD (milhões)"))
    st.plotly_chart(fig4, use_container_width=True)

    ita_usd = ie[ie["pais"] == "Itália"].groupby("ano")["usd"].sum()
    fr_usd  = ie[ie["pais"] == "França"].groupby("ano")["usd"].sum()
    st.markdown(insight(
        f"<strong>Itália e França lideram valor, Argentina lidera volume.</strong> "
        f"O Prosecco italiano (${ita_usd.get(2019,0)/1e6:.1f}M) e o Champagne francês "
        f"(${fr_usd.get(2019,0)/1e6:.1f}M) competem no segmento premium. "
        "Mas o crescimento dos espumantes brasileiros vem reduzindo essa dependência — "
        "especialmente no segmento de consumo diário.",
        "info"
    ), unsafe_allow_html=True)

# ── TAB 3: DEPENDÊNCIA ARGENTINA ─────────────────────────────
with tab3:
    st.markdown(section_header("ARGENTINA", "O vizinho que abastece o Brasil"), unsafe_allow_html=True)
    st.caption("A Argentina é fornecedora-chave em múltiplas categorias: vinho, espumante, suco e uva fresca")

    arg_v  = iv[iv["pais"] == "Argentina"].groupby("ano")[["kg","usd"]].sum()
    arg_e  = ie[ie["pais"] == "Argentina"].groupby("ano")[["kg","usd"]].sum()
    arg_s  = is_[is_["pais"] == "Argentina"].groupby("ano")[["kg","usd"]].sum()
    arg_u  = iu[iu["pais"] == "Argentina"].groupby("ano")[["kg","usd"]].sum()

    fig5 = go.Figure()
    for name, sub, color in [
        ("Vinho de Mesa", arg_v, C["rose"]),
        ("Espumantes",    arg_e, C["gold"]),
        ("Suco",          arg_s, C["green"]),
        ("Uvas Frescas",  arg_u, C["purple"]),
    ]:
        if len(sub) == 0: continue
        fig5.add_trace(go.Scatter(
            x=sub.index, y=sub["usd"]/1e6,
            mode="lines", name=name, line=dict(color=color, width=2),
            hovertemplate=f"<b>%{{x}}</b> · {name}<br>${{y:.1f}}M<extra></extra>",
        ))
    fig5.update_layout(**get_layout(height=340, yaxis_title="USD (milhões) importados da Argentina",
                                     legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center")))
    st.plotly_chart(fig5, use_container_width=True)

    total_arg_2019 = (arg_v.loc[2019,"usd"] if 2019 in arg_v.index else 0) + \
                     (arg_e.loc[2019,"usd"] if 2019 in arg_e.index else 0) + \
                     (arg_s.loc[2019,"usd"] if 2019 in arg_s.index else 0) + \
                     (arg_u.loc[2019,"usd"] if 2019 in arg_u.index else 0)

    st.markdown(insight(
        f"<strong>A Argentina é o principal fornecedor regional:</strong> "
        f"${total_arg_2019/1e6:.0f}M em importações totais em 2019. "
        "A proximidade geográfica, o câmbio favorável e a tradição vinícola argentina "
        "garantem vantagem competitiva, especialmente no segmento de vinhos de mesa de entrada.",
        "wine"
    ), unsafe_allow_html=True)

# ── TAB 4: BALANÇA COMERCIAL ──────────────────────────────────
with tab4:
    st.markdown(section_header("BALANÇA COMERCIAL", "Brasil exporta menos do que importa em quase todos os produtos"), unsafe_allow_html=True)

    from util.data import load_exp_vinhos, load_exp_espumantes, load_exp_suco, load_exp_uvas
    ev_yr2 = load_exp_vinhos().groupby("ano")[["kg","usd"]].sum()
    ee_yr2 = load_exp_espumantes().groupby("ano")[["kg","usd"]].sum()
    es_yr2 = load_exp_suco().groupby("ano")[["kg","usd"]].sum()

    # Wine trade balance
    bal_v = ev_yr2["usd"] - iv_yr["usd"]
    bal_e = ee_yr2["usd"] - ie_yr["usd"]
    bal_s = es_yr2["usd"] - is_yr["usd"]

    fig6 = go.Figure()
    for name, bal, color in [
        ("Vinhos de Mesa", bal_v, C["rose"]),
        ("Espumantes",     bal_e, C["gold"]),
        ("Suco de Uva",    bal_s, C["green"]),
    ]:
        bal_clean = bal.fillna(0)
        fig6.add_trace(go.Scatter(
            x=bal_clean.index, y=bal_clean.values/1e6,
            mode="lines", name=name, line=dict(color=color, width=2),
            hovertemplate=f"<b>%{{x}}</b> · {name}<br>${{y:+.1f}}M<extra></extra>",
        ))
    fig6.add_hline(y=0, line_color=C["cream"], line_dash="dot", opacity=0.4)
    fig6.update_layout(**get_layout(height=360, yaxis_title="Saldo (USD M) — positivo=superávit",
                                     legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center")))
    st.plotly_chart(fig6, use_container_width=True)

    bal_v_2019 = bal_v.get(2019, 0)
    bal_e_2019 = bal_e.get(2019, 0)
    bal_s_2019 = bal_s.get(2019, 0)

    c1, c2, c3 = st.columns(3)
    c1.markdown(kpi(f"${bal_v_2019/1e6:+.0f}M", "Vinhos de Mesa 2019",
        "Déficit — Chile e Portugal dominam", C["red"], "📊"), unsafe_allow_html=True)
    c2.markdown(kpi(f"${bal_e_2019/1e6:+.0f}M", "Espumantes 2019",
        "Ainda deficitário mas melhorando", C["gold"] if bal_e_2019 > -5e6 else C["red"], "📊"), unsafe_allow_html=True)
    c3.markdown(kpi(f"${bal_s_2019/1e6:+.0f}M", "Suco de Uva 2019",
        "Superávit — Brasil exporta mais", C["green"] if bal_s_2019 > 0 else C["red"], "📊"), unsafe_allow_html=True)

    st.markdown(insight(
        f"<strong>O suco de uva é o único produto com superávit consistente.</strong> "
        f"No vinho, o déficit chegou a ${bal_v.min()/1e6:.0f}M (ano {bal_v.idxmin()}). "
        "A estratégia da indústria gaúcha de focar em espumantes e suco de uva "
        "é a resposta correta à competição chilena e argentina no vinho de mesa.",
        "growth"
    ), unsafe_allow_html=True)
