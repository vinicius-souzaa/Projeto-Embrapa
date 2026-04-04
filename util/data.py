import pandas as pd
import numpy as np
import streamlit as st
import os

# Resolve data directory relative to this file — works on Streamlit Cloud
_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _p(filename: str) -> str:
    """Return absolute path to a data file."""
    return os.path.join(_DATA_DIR, filename)


# ── PARSERS ───────────────────────────────────────────────────

def _parse_production(path: str, year_end: int) -> pd.DataFrame:
    """col[0]=id, col[1]=code, col[2]=name, col[3+]=yearly values (1 per year)"""
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            cols = line.strip().split(";")
            if len(cols) < 5:
                continue
            try:
                int(cols[0])
            except ValueError:
                continue
            name = cols[2].strip()
            n_years = len(cols) - 3
            year_start = year_end - n_years + 1
            for i, val in enumerate(cols[3:]):
                try:
                    v = float(val) if val.strip() else 0.0
                    rows.append({"categoria": name, "ano": year_start + i, "valor": v})
                except ValueError:
                    pass
    return pd.DataFrame(rows)


def _parse_impexp(path: str, year_start: int = 1970, year_end: int = 2019) -> pd.DataFrame:
    """col[0]=id, col[1]=pais, col[2+]=yr_kg, yr_usd, yr+1_kg, yr+1_usd ..."""
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            cols = line.strip().split(";")
            if len(cols) < 4:
                continue
            try:
                int(cols[0])
            except ValueError:
                continue
            pais = cols[1].strip()
            data = cols[2:]
            for i in range(0, len(data) - 1, 2):
                ano = year_start + (i // 2)
                if ano > year_end:
                    break
                try:
                    kg  = float(data[i])     if data[i].strip()     else 0.0
                    usd = float(data[i + 1]) if data[i + 1].strip() else 0.0
                    rows.append({"pais": pais, "ano": ano, "kg": kg, "usd": usd})
                except ValueError:
                    pass
    return pd.DataFrame(rows)


# ── CACHED LOADERS ────────────────────────────────────────────

@st.cache_data
def load_producao() -> pd.DataFrame:
    return _parse_production(_p("Produção_de_vinhos__sucos_e_derivados_1970-2019.csv"), 2019)

@st.cache_data
def load_comercializacao() -> pd.DataFrame:
    return _parse_production(_p("Comercialização_de_vinhos_e_derivados_1970-2019.csv"), 2019)

@st.cache_data
def load_uvas_americanas() -> pd.DataFrame:
    return _parse_production(_p("Uvas_americanas_e_híbridas_processadas_1970-2018.csv"), 2018)

@st.cache_data
def load_uvas_viniferas() -> pd.DataFrame:
    return _parse_production(_p("Uvas_viníferas_processadas_1970-2018.csv"), 2018)

@st.cache_data
def load_uvas_mesa() -> pd.DataFrame:
    return _parse_production(_p("Uvas_de_mesa_processadas_1970-2018.csv"), 2018)

@st.cache_data
def load_uvas_sem_class() -> pd.DataFrame:
    return _parse_production(_p("Uvas_sem_classificação_processadas_1970-2018.csv"), 2018)

@st.cache_data
def load_exp_vinhos() -> pd.DataFrame:
    return _parse_impexp(_p("Exportação_de_vinhos_de_mesa_1970-2019.csv"))

@st.cache_data
def load_exp_espumantes() -> pd.DataFrame:
    return _parse_impexp(_p("Exportação_de_espumantes_1970-2019.csv"))

@st.cache_data
def load_exp_suco() -> pd.DataFrame:
    return _parse_impexp(_p("Exportação_de_suco_de_uva_1970-2019.csv"))

@st.cache_data
def load_exp_uvas() -> pd.DataFrame:
    return _parse_impexp(_p("Exportação_de_uvas_frescas_1970-2019.csv"))

@st.cache_data
def load_imp_vinhos() -> pd.DataFrame:
    return _parse_impexp(_p("Importação_de_vinhos_de_mesa_1970-2019.csv"))

@st.cache_data
def load_imp_espumantes() -> pd.DataFrame:
    return _parse_impexp(_p("Importação_de_espumantes_1970-2019.csv"))

@st.cache_data
def load_imp_suco() -> pd.DataFrame:
    return _parse_impexp(_p("Importação_de_suco_de_uva_1970-2019.csv"))

@st.cache_data
def load_imp_uvas() -> pd.DataFrame:
    return _parse_impexp(_p("Importação_de_uvas_frescas_1970-2019.csv"))

@st.cache_data
def load_imp_passas() -> pd.DataFrame:
    return _parse_impexp(_p("Importação_de_uvas_passas_1970-2019.csv"))


# ── HELPERS ───────────────────────────────────────────────────

def yearly_total(df: pd.DataFrame, col: str = "valor") -> pd.Series:
    return df.groupby("ano")[col].sum()

def top_cat(df: pd.DataFrame, n: int = 10) -> pd.Series:
    return df.groupby("categoria")["valor"].sum().sort_values(ascending=False).head(n)

def top_pais(df: pd.DataFrame, col: str = "kg", n: int = 10) -> pd.Series:
    return df.groupby("pais")[col].sum().sort_values(ascending=False).head(n)
