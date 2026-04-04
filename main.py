import streamlit as st

st.set_page_config(
    page_title="Vitivinicultura Brasileira · Embrapa",
    layout="wide",
    page_icon="🍇",
    initial_sidebar_state="expanded",
)

pages = st.navigation([
    st.Page("pages/0_Visao_Geral.py",    title="🍇 Visão Geral"),
    st.Page("pages/1_Producao.py",       title="🍷 Produção & Comercialização"),
    st.Page("pages/2_Processamento.py",  title="🌿 Processamento de Uvas"),
    st.Page("pages/3_Exportacoes.py",    title="✈️ Exportações"),
    st.Page("pages/4_Importacoes.py",    title="🛬 Importações"),
    st.Page("pages/5_Conclusoes.py",     title="💡 Conclusões"),
], position="sidebar")
pages.run()
