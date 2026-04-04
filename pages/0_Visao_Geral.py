import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from util.style    import inject_css, kpi, insight, section_header, event_badge, data_row, get_layout, hex_to_rgba, C
from util.data     import load_producao, load_comercializacao, load_uvas_americanas, load_uvas_viniferas, yearly_total
from util.layout   import sidebar
from util.constants import EVENTS, PROD_CATS

inject_css(); sidebar()

prod  = load_producao()
com   = load_comercializacao()
amer  = load_uvas_americanas()
vinif = load_uvas_viniferas()

# ── PAGE TITLE ────────────────────────────────────────────────
st.markdown(
    f'<h1 style="font-family:Playfair Display,serif;font-size:2.1rem;'
    f'font-weight:700;color:{C["cream"]};margin:0 0 0.2rem;">🍇 Vitivinicultura Brasileira</h1>'
    f'<div style="font-size:0.85rem;color:{C["muted"]};margin-bottom:1.2rem;">'
    f'50 anos de dados · Embrapa Uva e Vinho · Serra Gaúcha, RS · 1970–2019</div>',
    unsafe_allow_html=True
)

# ── KPIs ──────────────────────────────────────────────────────
vm_total = prod[prod["categoria"] == "VINHO DE MESA"].groupby("ano")["valor"].sum()
suco_total = prod[prod["categoria"] == "SUCO"].groupby("ano")["valor"].sum()
esp_total  = com[com["categoria"] == "ESPUMANTES"].groupby("ano")["valor"].sum()
proc_total = amer.groupby("ano")["valor"].sum()

queda_2016 = (vm_total[2016] / vm_total[2015] - 1) * 100
esp_growth  = (esp_total[2019] / esp_total[2000] - 1) * 100

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(kpi(f"{vm_total[2019]/1e6:.0f}M L", "Vinho de Mesa 2019",
        f"Pico: {vm_total.idxmax()} ({vm_total.max()/1e6:.0f}M L)", C["rose"], "🍷"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi(f"{suco_total[2019]/1e6:.0f}M L", "Suco de Uva 2019",
        f"+{(suco_total[2019]/suco_total[1990]-1)*100:.0f}% desde 1990", C["green"], "🥤"), unsafe_allow_html=True)
with c3:
    st.markdown(kpi(f"{esp_total[2019]/1e6:.1f}M L", "Espumantes Comercializados 2019",
        f"+{esp_growth:.0f}% desde 2000", C["gold"], "🥂"), unsafe_allow_html=True)
with c4:
    st.markdown(kpi(f"{queda_2016:.0f}%", "Queda em 2016 (geada)",
        "Pior ano desde 1973 · evento climático", C["red"], "🌨️"), unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ── SÉRIE HISTÓRICA PRINCIPAL ─────────────────────────────────
st.markdown(section_header("01 · SÉRIE HISTÓRICA", "Produção de Vinho de Mesa — 50 anos (1970–2019)"), unsafe_allow_html=True)

fig = go.Figure()

# Background fill by decade
decade_colors = ["#4A0E2B", "#521A34", "#4A0E2B", "#521A34", "#4A0E2B"]
for i, (start, end) in enumerate([(1970,1980),(1980,1990),(1990,2000),(2000,2010),(2010,2019)]):
    fig.add_vrect(x0=start, x1=end, fillcolor=decade_colors[i],
                  opacity=0.3, layer="below", line_width=0)

# Main area chart
anos = vm_total.index.tolist()
vals = vm_total.values.tolist()
fig.add_trace(go.Scatter(
    x=anos, y=[v/1e6 for v in vals],
    mode="lines", fill="tozeroy",
    line=dict(color=C["rose"], width=2),
    fillcolor=hex_to_rgba(C["rose"], 0.18),
    name="Vinho de Mesa (ML)",
    hovertemplate="<b>%{x}</b><br>%{y:.1f} milhões L<extra></extra>",
))

# Add suco overlay
fig.add_trace(go.Scatter(
    x=suco_total.index.tolist(), y=[v/1e6 for v in suco_total.values],
    mode="lines", line=dict(color=C["green"], width=1.5, dash="dot"),
    name="Suco de Uva (ML)",
    hovertemplate="<b>%{x}</b><br>%{y:.1f} milhões L<extra></extra>",
))

# Event markers
for ano, label, color, desc in EVENTS:
    if ano in vm_total.index:
        y_val = vm_total[ano] / 1e6
        fig.add_trace(go.Scatter(
            x=[ano], y=[y_val],
            mode="markers",
            marker=dict(size=11, color=color, symbol="diamond",
                        line=dict(color=C["bg"], width=1.5)),
            name=label,
            hovertemplate=f"<b>{ano}</b><br>{label}<br>{desc}<extra></extra>",
            showlegend=False,
        ))
        fig.add_annotation(
            x=ano, y=y_val + (15 if y_val < 200 else -25),
            text=f"{ano}", showarrow=False,
            font=dict(color=color, size=9),
        )

# 2016 annotation
fig.add_annotation(
    x=2016, y=vm_total[2016]/1e6 - 20,
    text="🌨️ Geada 2016<br>−59%",
    showarrow=True, arrowhead=2, arrowcolor=C["red"],
    font=dict(color=C["red"], size=10), bgcolor=C["surface"],
    bordercolor=C["red"], borderwidth=1,
)

fig.update_layout(**get_layout(
    height=420, yaxis_title="Litros (milhões)",
    legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
))
st.plotly_chart(fig, use_container_width=True)

st.markdown(insight(
    "<strong>2016 foi o pior ano desde 1973:</strong> a geada severa de julho de 2016 na Serra Gaúcha "
    "destruiu boa parte das videiras e causou queda de 59% na produção de vinho de mesa e 52% no suco de uva. "
    "A recuperação foi imediata — 2017 registrou o maior volume da série.",
    "alert"
), unsafe_allow_html=True)

st.divider()

# ── PROCESSAMENTO DE UVAS ─────────────────────────────────────
st.markdown(section_header("02 · PROCESSAMENTO", "Uvas Americanas vs Viníferas — kilos processados"), unsafe_allow_html=True)

amer_yr  = amer.groupby("ano")["valor"].sum()
vinif_yr = vinif.groupby("ano")["valor"].sum()

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=amer_yr.index, y=[v/1e6 for v in amer_yr.values],
    name="Americanas/Híbridas", marker_color=hex_to_rgba(C["purple"], 0.85),
    hovertemplate="<b>%{x}</b><br>%{y:.0f} M kg<extra></extra>",
))
fig2.add_trace(go.Bar(
    x=vinif_yr.index, y=[v/1e6 for v in vinif_yr.values],
    name="Viníferas (finas)", marker_color=hex_to_rgba(C["gold"], 0.85),
    hovertemplate="<b>%{x}</b><br>%{y:.0f} M kg<extra></extra>",
))
fig2.add_vrect(x0=2015.5, x1=2016.5, fillcolor=C["red"], opacity=0.15,
               annotation_text="Geada", annotation_font_color=C["red"])
fig2.update_layout(**get_layout(
    height=340, barmode="stack", yaxis_title="Kilos (milhões)",
    legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
))
st.plotly_chart(fig2, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    pct_amer  = amer_yr[2018] / (amer_yr[2018] + vinif_yr[2018]) * 100
    pct_vinif = 100 - pct_amer
    st.markdown(insight(
        f"<strong>Americanas dominam o processamento:</strong> em 2018, {pct_amer:.0f}% do total processado "
        f"foram uvas americanas e híbridas. As viníferas representam apenas {pct_vinif:.0f}% — "
        "mas produzem vinhos de maior valor agregado (vinhos finos).",
        "wine"
    ), unsafe_allow_html=True)
with c2:
    peak_amer = amer_yr.idxmax()
    st.markdown(insight(
        f"<strong>Pico de produção em {peak_amer}:</strong> {amer_yr[peak_amer]/1e6:.0f} milhões de kg "
        "de americanas processadas. A queda de 2016 foi proporcional nas duas categorias, "
        "confirmando que a geada afetou toda a Serra Gaúcha indistintamente.",
        "info"
    ), unsafe_allow_html=True)

st.divider()

# ── EVOLUÇÃO POR PRODUTO ──────────────────────────────────────
st.markdown(section_header("03 · MIX DE PRODUTOS", "Comercialização por categoria — 1970 a 2019"), unsafe_allow_html=True)

cats_plot = {
    "VINHO DE MESA":          C["rose"],
    "VINHO  FINO DE MESA":    C["purple"],
    "ESPUMANTES":             C["gold"],
    "SUCO DE UVAS":           C["green"],
}

fig3 = go.Figure()
for cat, color in cats_plot.items():
    sub = com[com["categoria"] == cat].groupby("ano")["valor"].sum()
    if len(sub) == 0:
        continue
    fig3.add_trace(go.Scatter(
        x=sub.index, y=[v/1e6 for v in sub.values],
        mode="lines", name=cat.title(),
        line=dict(color=color, width=2),
        fill="tonexty" if cat == "VINHO DE MESA" else "none",
        fillcolor=hex_to_rgba(color, 0.08),
        hovertemplate=f"<b>{cat}</b><br>%{{x}}: %{{y:.1f}}M L<extra></extra>",
    ))

fig3.update_layout(**get_layout(
    height=360, yaxis_title="Litros / Kilos (milhões)",
    legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
))
st.plotly_chart(fig3, use_container_width=True)

st.markdown(insight(
    "<strong>Três transformações em 50 anos:</strong> (1) o vinho de mesa perdeu espaço relativo "
    "para produtos diferenciados; (2) os espumantes cresceram de forma consistente — "
    "de 4,3M L em 2000 para 22,8M L em 2019 (+430%); "
    "(3) o suco de uva se consolidou como o produto de maior crescimento da categoria.",
    "growth"
), unsafe_allow_html=True)

st.divider()

# ── EVENTOS CLIMÁTICOS ────────────────────────────────────────
st.markdown(section_header("04 · EVENTOS HISTÓRICOS", "Impacto de eventos climáticos e econômicos na produção"), unsafe_allow_html=True)

for i in range(0, len(EVENTS), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j >= len(EVENTS): break
        ano, label, color, desc = EVENTS[i + j]
        val = vm_total.get(ano, None)
        val_str = f"{val/1e6:.0f}M L" if val else "—"
        col.markdown(f"""
        <div style="background:{C['surface']};border:1px solid {C['border']};
                    border-radius:8px;padding:0.85rem;border-top:2px solid {color};">
            <div style="font-size:0.68rem;color:{color};font-weight:700;
                        margin-bottom:0.2rem;">{ano}</div>
            <div style="font-size:0.84rem;font-weight:600;color:{C['cream']};
                        margin-bottom:0.25rem;">{label}</div>
            <div style="font-size:0.74rem;color:{C['muted']};line-height:1.45;">{desc}</div>
            <div style="font-size:0.72rem;color:{color};margin-top:0.35rem;
                        font-weight:600;">Vinho mesa: {val_str}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
