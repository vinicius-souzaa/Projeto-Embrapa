import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from util.style    import inject_css, kpi, insight, section_header, data_row, get_layout, hex_to_rgba, C
from util.data     import (load_producao, load_comercializacao,
                            load_exp_espumantes, load_exp_suco,
                            load_imp_vinhos, load_exp_vinhos)
from util.layout   import sidebar
from util.constants import EVENTS

inject_css(); sidebar()

prod = load_producao()
com  = load_comercializacao()
ee   = load_exp_espumantes()
es   = load_exp_suco()
iv   = load_imp_vinhos()
ev   = load_exp_vinhos()

st.markdown(
    f'<h1 style="font-family:Playfair Display,serif;2.185rem;font-weight:700;'
    f'color:{C["cream"]};margin:0 0 0.2rem;">💡 Conclusões & Insights</h1>'
    f'<div style="0.943rem;color:{C["muted"]};margin-bottom:1.1rem;">'
    f'50 anos de vitivinicultura brasileira — o que os dados revelam</div>',
    unsafe_allow_html=True
)

# ── INSIGHT STRIPS ────────────────────────────────────────────
vm    = prod[prod["categoria"] == "VINHO DE MESA"].groupby("ano")["valor"].sum()
suco  = prod[prod["categoria"] == "SUCO"].groupby("ano")["valor"].sum()
esp   = com[com["categoria"] == "ESPUMANTES"].groupby("ano")["valor"].sum()
ee_yr = ee.groupby("ano")[["kg","usd"]].sum()
es_yr = es.groupby("ano")[["kg","usd"]].sum()
iv_yr = iv.groupby("ano")[["kg","usd"]].sum()
ev_yr = ev.groupby("ano")[["kg","usd"]].sum()

st.markdown(section_header("GRANDES ACHADOS", "O que 50 anos de dados revelam sobre a vitivinicultura do RS"), unsafe_allow_html=True)

achados = [
    (C["gold"], "🥂", "Espumantes: a transformação mais importante",
     "O mercado espumante cresceu +430% em volume entre 2000 e 2019. "
     "O Brasil encontrou seu nicho competitivo — espumantes de qualidade a preço acessível, "
     f"gerando ${ee_yr.loc[2019,'usd']/1e6:.1f}M em exportações. "
     "A Serra Gaúcha é hoje reconhecida como polo de espumantes da América Latina."),

    (C["green"], "🥤", "Suco de uva: o campeão silencioso",
     f"De {suco.get(1980,0)/1e6:.0f}M L em 1980 para {suco.get(2019,0)/1e6:.0f}M L em 2019. "
     f"O suco é o único produto com superávit comercial consistente — ${es_yr.loc[2019,'usd']/1e6:.1f}M "
     "exportados vs déficit em todos os outros. "
     "A estratégia de diversificação além do vinho salvou a indústria gaúcha."),

    (C["red"], "🌨️", "2016: o ano que quase parou a Serra Gaúcha",
     "A geada de julho de 2016 foi o evento climático mais destrutivo da história recente. "
     f"Queda de {(1-vm.get(2016,0)/vm.get(2015,1))*100:.0f}% na produção de vinho de mesa, "
     f"−{(1-suco.get(2016,0)/suco.get(2015,1))*100:.0f}% no suco. "
     "A recuperação total em 2017 demonstra a resiliência do setor — mas evidencia "
     "a vulnerabilidade climática estrutural da monocultura."),

    (C["rose"], "🍷", "Vinho de mesa: volume cai, qualidade sobe",
     f"O pico de produção foi em 2004 ({vm.max()/1e6:.0f}M L). Desde então, tendência de queda relativa. "
     "Não é crise — é transição estratégica: a indústria substitui volume de vinho básico "
     "por produtos de maior valor agregado (vinhos finos, espumantes). "
     "O consumidor brasileiro se sofisticou."),

    (C["purple"], "🇦🇷", "Chile e Argentina: ameaça e inspiração",
     f"O Chile importou {iv[iv['pais']=='Chile'][iv['ano']==2019]['kg'].sum()/1e6:.0f}M kg "
     "de vinho para o Brasil em 2019 — mais que todos os outros países juntos. "
     "A abertura do Plano Real (1994) inundou o mercado com vinho estrangeiro barato. "
     "A resposta brasileira foi especialização — espumantes e suco — e não competição direta."),

    (C["muted"], "🌿", "Variedades: o dilema americanas vs viníferas",
     f"As uvas americanas representam ~{(85):.0f}% do processamento. "
     "São mais resistentes, produtivas e baratas. Mas as viníferas produzem vinhos de exportação. "
     "O desafio futuro da Serra Gaúcha é expandir viníferas sem destruir a base "
     "econômica das famílias que dependem das americanas."),
]

c1, c2 = st.columns(2)
for i, (color, icon, title, text) in enumerate(achados):
    col = c1 if i % 2 == 0 else c2
    col.markdown(f"""
    <div style="background:{C['surface']};border:1px solid {C['border']};
                border-radius:8px;padding:1.1rem 1.3rem;margin-bottom:0.7rem;
                border-left:3px solid {color};">
        <div style="1.265rem;margin-bottom:0.3rem;">{icon}</div>
        <div style="font-family:Playfair Display,serif;1.0925rem;
                    font-weight:600;color:{color};margin-bottom:0.4rem;">{title}</div>
        <div style="0.92rem;color:{C['muted']};line-height:1.65;">{text}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── PAINEL COMPARATIVO FINAL ──────────────────────────────────
st.markdown(section_header("PAINEL FINAL", "A transformação em números — 1970 vs 2019"), unsafe_allow_html=True)

comparativo = [
    ("Produção vinho de mesa",    f"{vm.get(1970,0)/1e6:.0f}M L",    f"{vm.get(2019,0)/1e6:.0f}M L",    "−33%",       C["red"]),
    ("Suco de uva",               f"{suco.get(1980,0)/1e6:.0f}M L",  f"{suco.get(2019,0)/1e6:.0f}M L",  "+430%",      C["green"]),
    ("Espumantes comercializados",f"n/d",                             f"{esp.get(2019,0)/1e6:.1f}M L",   "de zero",    C["gold"]),
    ("Exportação espumantes",     "$0",                               f"${ee_yr.loc[2019,'usd']/1e6:.1f}M","novo mercado",C["gold"]),
    ("Exportação suco",           "$0",                               f"${es_yr.loc[2019,'usd']/1e6:.1f}M","novo mercado",C["green"]),
    ("Importação vinhos (Chile)", "praticamente zero",                f"{iv[iv['pais']=='Chile'][iv['ano']==2019]['kg'].sum()/1e6:.0f}M kg","abertura 1994",C["red"]),
]

comp_cols = st.columns([3,2,2,1])
comp_cols[0].markdown(f'<div style="0.713rem;color:{C["dim"]};text-transform:uppercase;letter-spacing:0.1em;padding:0.4rem 0;">Indicador</div>', unsafe_allow_html=True)
comp_cols[1].markdown(f'<div style="0.713rem;color:{C["dim"]};text-transform:uppercase;letter-spacing:0.1em;padding:0.4rem 0;">Início</div>', unsafe_allow_html=True)
comp_cols[2].markdown(f'<div style="0.713rem;color:{C["dim"]};text-transform:uppercase;letter-spacing:0.1em;padding:0.4rem 0;">2019</div>', unsafe_allow_html=True)
comp_cols[3].markdown(f'<div style="0.713rem;color:{C["dim"]};text-transform:uppercase;letter-spacing:0.1em;padding:0.4rem 0;">Var.</div>', unsafe_allow_html=True)

for ind, ini, fim, var, color in comparativo:
    c0, c1, c2, c3 = st.columns([3,2,2,1])
    c0.markdown(f'<div style="0.92rem;color:{C["cream"]};padding:0.35rem 0;">{ind}</div>', unsafe_allow_html=True)
    c1.markdown(f'<div style="0.92rem;color:{C["muted"]};padding:0.35rem 0;">{ini}</div>', unsafe_allow_html=True)
    c2.markdown(f'<div style="0.92rem;color:{C["cream"]};font-weight:600;padding:0.35rem 0;">{fim}</div>', unsafe_allow_html=True)
    c3.markdown(f'<div style="0.92rem;color:{color};font-weight:700;padding:0.35rem 0;">{var}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="border-bottom:1px solid {C["border"]};"></div>', unsafe_allow_html=True)

st.divider()

# ── FICHA TÉCNICA ─────────────────────────────────────────────
st.markdown(section_header("FICHA TÉCNICA", "Sobre o projeto"), unsafe_allow_html=True)
st.markdown(f"""
<div style="background:{C['bg']};border:1px solid {C['border']};border-radius:10px;
            padding:1.3rem 1.6rem;">
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:1.2rem;">
    <div>
      <p style="color:{C['gold']};0.713rem;font-weight:600;letter-spacing:0.15em;
                text-transform:uppercase;margin-bottom:0.4rem;">FONTE</p>
      <p style="color:{C['muted']};0.874rem;line-height:1.7;margin:0;">
        Embrapa Uva e Vinho<br/>Dados da Vitivinicultura<br/>Serra Gaúcha · RS<br/>Portal VITIBRASIL</p>
    </div>
    <div>
      <p style="color:{C['rose']};0.713rem;font-weight:600;letter-spacing:0.15em;
                text-transform:uppercase;margin-bottom:0.4rem;">DATASETS</p>
      <p style="color:{C['muted']};0.874rem;line-height:1.7;margin:0;">
        15 arquivos CSV<br/>Produção · Comercialização<br/>Processamento (4 tipos)<br/>
        Exportação (4 produtos)<br/>Importação (5 produtos)</p>
    </div>
    <div>
      <p style="color:{C['green']};0.713rem;font-weight:600;letter-spacing:0.15em;
                text-transform:uppercase;margin-bottom:0.4rem;">PERÍODO</p>
      <p style="color:{C['muted']};0.874rem;line-height:1.7;margin:0;">
        1970–2019 (50 anos)<br/>Produção: litros<br/>Processamento: kg<br/>
        Exp./Imp.: kg e USD</p>
    </div>
    <div>
      <p style="color:{C['purple']};0.713rem;font-weight:600;letter-spacing:0.15em;
                text-transform:uppercase;margin-bottom:0.4rem;">STACK</p>
      <p style="color:{C['muted']};0.874rem;line-height:1.7;margin:0;">
        Python · Pandas<br/>Plotly · Streamlit<br/>Playfair Display UI<br/>Tema vinho bordô</p>
    </div>
  </div>
  <div style="margin-top:1rem;padding-top:0.9rem;border-top:1px solid {C['border']};">
    <p style="color:{C['muted']};0.8165rem;margin:0;">
      <strong style="color:{C['cream']};">Vinicius Abreu Ernestino Souza</strong> ·
      Data Analytics · São Paulo, SP
    </p>
  </div>
</div>""", unsafe_allow_html=True)
