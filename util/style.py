import copy
from util.constants import C, HOVER

# ── PLOTLY BASE ───────────────────────────────────────────────
_BASE = dict(
    paper_bgcolor=C["surface"],
    plot_bgcolor=C["surface"],
    font=dict(family="Georgia, serif", color=C["muted"], size=12),
    title=dict(text="", font=dict(color=C["cream"], size=14)),
    legend=dict(bgcolor=C["bg"], bordercolor=C["border"],
                borderwidth=1, font=dict(color=C["muted"], size=11)),
    xaxis=dict(gridcolor=C["border"], linecolor=C["border"],
               tickfont=dict(color=C["muted"]), title_font=dict(color=C["muted"]),
               zeroline=False),
    yaxis=dict(gridcolor=C["border"], linecolor=C["border"],
               tickfont=dict(color=C["muted"]), title_font=dict(color=C["muted"]),
               zeroline=False),
    margin=dict(l=16, r=16, t=44, b=16),
    hoverlabel=HOVER,
)

def get_layout(**kw):
    lay = copy.deepcopy(_BASE)
    lay.update(kw)
    lay["hoverlabel"] = copy.deepcopy(HOVER)
    return lay

def hex_to_rgba(hex_color: str, alpha: float = 0.15) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# ── CSS ───────────────────────────────────────────────────────
_CSS_LINES = [
    "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');",
    f"html,body,[class*='css']{{font-family:'Inter',sans-serif !important;}}",
    f"html,body{{background-color:{C['bg']} !important;}}",
    f"[data-testid='stAppViewContainer']{{background-color:{C['bg']} !important;}}",
    f"[data-testid='stMain']{{background-color:{C['bg']} !important;}}",
    f".main .block-container{{background-color:{C['bg']} !important;}}",
    ".block-container{padding-top:1.2rem !important;padding-bottom:2rem !important;}",
    f"[data-testid='stHeader']{{background:{C['bg']} !important;}}",
    "[data-testid='stHeaderActionElements']{display:none !important;}",
    f"[data-testid='stSidebar']{{background-color:{C['surface']} !important;border-right:1px solid {C['border']} !important;}}",
    f"[data-testid='stSidebar']>div{{background-color:{C['surface']} !important;}}",
    f"[data-testid='stSidebar'] *{{color:{C['muted']} !important;}}",
    # Tabs — underline style
    f"[data-baseweb='tab-list']{{background-color:{C['bg']} !important;border-bottom:1px solid {C['border']} !important;gap:4px !important;padding:0 !important;}}",
    f"[data-baseweb='tab']{{background-color:transparent !important;color:{C['muted']} !important;border-bottom:2px solid transparent !important;padding:0.5rem 1rem !important;font-family:'Inter',sans-serif !important;}}",
    f"[aria-selected='true'][data-baseweb='tab']{{color:{C['gold']} !important;border-bottom-color:{C['gold']} !important;}}",
    f"[data-baseweb='tab-panel']{{background-color:{C['bg']} !important;padding-top:1.2rem !important;}}",
    f"[data-baseweb='select'] *{{color:{C['cream']} !important;background:{C['surface']} !important;}}",
    f".stSlider *{{color:{C['cream']} !important;}}",
    f".stRadio *{{color:{C['cream']} !important;}}",
    f".stMarkdown p{{color:{C['muted']} !important;}}",
    f"hr{{border-color:{C['border']} !important;}}",
    # KPI card
    f".kpi-card{{background:{C['surface']};border:1px solid {C['border']};border-radius:8px;padding:1rem 1.2rem;margin-bottom:0.5rem;}}",
    f".kpi-card:hover{{border-color:{C['gold']};}}",
    ".kpi-number{font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;line-height:1;margin-bottom:0.2rem;}",
    f".kpi-label{{font-size:0.65rem;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:{C['dim']};}}",
    ".kpi-delta{font-size:0.75rem;font-weight:500;margin-top:0.25rem;}",
    # Insight card
    f".insight{{border-radius:8px;padding:0.85rem 1.1rem;margin:0.6rem 0;border-left:3px solid;}}",
    f".insight-wine{{background:{hex_to_rgba(C['gold'],0.08)};border-color:{C['gold']};}}",
    f".insight-alert{{background:{hex_to_rgba(C['red'],0.08)};border-color:{C['red']};}}",
    f".insight-growth{{background:{hex_to_rgba(C['green'],0.08)};border-color:{C['green']};}}",
    f".insight-info{{background:{hex_to_rgba(C['rose'],0.08)};border-color:{C['rose']};}}",
    ".insight p{color:#D4B8C0;font-size:0.85rem;line-height:1.65;margin:0;}",
    f".insight strong{{color:{C['cream']};}}",
    # Section header
    f".sec-label{{font-size:0.62rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:{C['gold']};margin-bottom:0.25rem;}}",
    f".sec-title{{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;color:{C['cream']};line-height:1.15;margin-bottom:0.75rem;}}",
    # Event badge
    f".evt-badge{{display:inline-block;font-size:0.6rem;font-weight:700;letter-spacing:0.08em;padding:0.12rem 0.5rem;border-radius:3px;}}",
    # Data row
    f".data-row{{display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid {C['border']};font-size:0.8rem;}}",
    f".data-row .dk{{color:{C['muted']};}}",
    f".data-row .dv{{color:{C['cream']};font-weight:500;}}",
]

CSS = "<style>\n" + "\n".join(_CSS_LINES) + "\n</style>"

def inject_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)


# ── COMPONENTS ────────────────────────────────────────────────

def kpi(number: str, label: str, delta: str = None, color: str = None, icon: str = "🍷") -> str:
    color = color or C["gold"]
    d = f'<div class="kpi-delta" style="color:{color};">{delta}</div>' if delta else ""
    return (
        f'<div class="kpi-card">'
        f'<div style="font-size:1.1rem;margin-bottom:0.15rem;">{icon}</div>'
        f'<div class="kpi-number" style="color:{color};">{number}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'{d}</div>'
    )

def insight(text: str, kind: str = "wine") -> str:
    icons = {"wine": "🍷", "alert": "⚠️", "growth": "📈", "info": "💡"}
    return f'<div class="insight insight-{kind}"><p>{icons.get(kind,"💡")} {text}</p></div>'

def section_header(label: str, title: str) -> str:
    return (
        f'<div class="sec-label">{label}</div>'
        f'<div class="sec-title">{title}</div>'
    )

def event_badge(text: str, color: str) -> str:
    return (
        f'<span class="evt-badge" '
        f'style="background:{color}22;color:{color};border:1px solid {color}44;">'
        f'{text}</span>'
    )

def data_row(key: str, value: str, value_color: str = None) -> str:
    vc = f'color:{value_color};' if value_color else ""
    return (
        f'<div class="data-row">'
        f'<span class="dk">{key}</span>'
        f'<span class="dv" style="{vc}">{value}</span>'
        f'</div>'
    )
