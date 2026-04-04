import streamlit as st
from util.constants import C

LBL = "#C0909A"   # legible pinkish-grey on dark wine bg

def sidebar():
    with st.sidebar:
        st.markdown(
            f'<div style="padding:1rem 0 0.5rem;">'
            f'<div style="font-family:Playfair Display,serif;font-size:1.1rem;'
            f'font-weight:700;color:{C["gold"]};">🍇 Vitivinicultura</div>'
            f'<div style="font-size:0.68rem;color:{LBL};letter-spacing:0.14em;'
            f'text-transform:uppercase;margin-top:3px;">Embrapa · RS · 1970–2019</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="background:{C["bg"]};border:1px solid {C["border"]};'
            f'border-radius:8px;padding:0.8rem;margin:0.5rem 0 1rem;">'
            f'<div style="font-size:0.65rem;color:{LBL};text-transform:uppercase;'
            f'letter-spacing:0.1em;margin-bottom:0.6rem;">Fontes de dados</div>'
            f'<div style="font-size:0.72rem;color:{LBL};line-height:1.7;">'
            f'📂 Embrapa Uva e Vinho<br/>'
            f'📍 Serra Gaúcha · RS<br/>'
            f'📅 1970–2019 (50 anos)<br/>'
            f'📊 15 datasets<br/>'
            f'⚠️ Geada catastrófica 2016'
            f'</div></div>',
            unsafe_allow_html=True
        )

        st.divider()
        st.caption("Vinicius Abreu Ernestino Souza")
        st.caption("Data Analytics · São Paulo, SP")
