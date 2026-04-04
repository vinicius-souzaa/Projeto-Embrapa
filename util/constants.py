# ── VITIVINICULTURA BRASILEIRA · Constantes ───────────────────

# Paleta de cores — tema vinho
C = {
    "bg":       "#2A0A1A",   # bordô muito escuro — fundo principal
    "surface":  "#3D1226",   # vinho escuro — cards
    "surface2": "#521A34",   # vinho médio — hover
    "border":   "#6B2A46",   # bordeaux — bordas
    "border2":  "#8B3A5E",   # rosa escuro — bordas ativas
    "gold":     "#C8972A",   # dourado — destaque principal
    "rose":     "#D4748C",   # rosé — secundário
    "cream":    "#F5E6D3",   # creme — texto principal
    "green":    "#5C7A3E",   # verde uva — crescimento
    "red":      "#C0392B",   # vermelho — alerta / queda
    "purple":   "#7B3F6E",   # roxo uva — accent3
    "muted":    "#B08090",   # rosado acinzentado — texto secundário
    "dim":      "#6B4050",   # bordô dim — texto terciário
}

# Hover Plotly
HOVER = dict(
    bgcolor="#3D1226",
    bordercolor="#6B2A46",
    font=dict(color="#F5E6D3", size=12),
    namelength=-1,
)

# Eventos climáticos e históricos relevantes
EVENTS = [
    (1973, "Seca severa RS",          C["red"],    "Pior safra dos anos 70"),
    (1980, "Geada + clima adverso",   C["red"],    "Queda de 38% na produção"),
    (1983, "Seca · El Niño",          C["red"],    "−49% produção vinho mesa"),
    (1994, "Plano Real",              C["gold"],   "Abertura comercial · importações disparam"),
    (2002, "Serra Gaúcha · geada",    C["red"],    "Queda pontual de produção"),
    (2005, "Boom espumantes",         C["green"],  "Crescimento acelerado começa"),
    (2010, "Récord suco de uva",      C["green"],  "Suco ultrapassa 50M litros/ano"),
    (2016, "Geada catastrófica RS",   C["red"],    "−59% produção · pior ano desde 1973"),
    (2019, "Récord espumantes",       C["green"],  "Maior exportação de espumantes"),
]

# Categorias principais de produção
PROD_CATS = {
    "VINHO DE MESA":                 C["rose"],
    "VINHO FINO DE MESA (VINÍFERA)": C["purple"],
    "SUCO":                          C["green"],
    "DERIVADOS":                     C["gold"],
    "ESPUMANTES":                    C["cream"],
}

# Top países importadores de vinho BR (2019)
TOP_IMP_PAISES = ["Chile", "Portugal", "Argentina", "Itália", "Espanha", "França"]
PAIS_COLORS = {
    "Chile":     "#E74C3C",
    "Portugal":  "#2ECC71",
    "Argentina": "#3498DB",
    "Itália":    "#E67E22",
    "Espanha":   "#9B59B6",
    "França":    "#1ABC9C",
    "Outros":    C["dim"],
}

# Décadas
DECADES = {
    1970: "Anos 70",
    1980: "Anos 80",
    1990: "Anos 90",
    2000: "Anos 2000",
    2010: "Anos 2010",
}
