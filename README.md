# 🍇 Vitivinicultura Brasileira — Análise de Dados Embrapa

> Dashboard interativo com 50 anos de dados da vitivinicultura gaúcha: produção, processamento de uvas, exportações e importações. Desenvolvido com dados públicos da Embrapa Uva e Vinho, cobrindo o período de 1970 a 2019.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://projeto-embrapa.streamlit.app)
&nbsp;
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-green)
![Plotly](https://img.shields.io/badge/Plotly-5.15+-purple)

---

## 📌 Sobre o projeto

A Serra Gaúcha é o coração da vitivinicultura brasileira. Em 50 anos, a indústria passou por transformações profundas: a abertura comercial de 1994 inundou o mercado com vinho chileno e argentino, a geada de 2016 destruiu quase 60% da safra em um único evento, e os espumantes brasileiros passaram de zero a fenômeno nacional. Este projeto analisa cada uma dessas transformações com dados reais do portal VITIBRASIL da Embrapa.

**Design:** bordô escuro `#2A0A1A` + dourado `#C8972A` + tipografia `Playfair Display` — tema vinho, completamente distinto dos outros projetos do portfólio.

---

## 📊 Dados

### Fonte

**Embrapa Uva e Vinho — VITIBRASIL**
Portal de dados da vitivinicultura brasileira, com sede em Bento Gonçalves, RS.
Disponível em: [vitibrasil.cnpuv.embrapa.br](http://vitibrasil.cnpuv.embrapa.br)

### Estrutura dos arquivos

Os dados da Embrapa têm dois formatos distintos:

**Produção, Processamento e Comercialização:**
```
col[0] = id
col[1] = código da categoria
col[2] = nome da categoria
col[3..N] = valor por ano (1 coluna por ano)
```

**Importação e Exportação:**
```
col[0] = id
col[1] = país
col[2..N] = pares intercalados: (ano_kg, ano_usd, ano+1_kg, ano+1_usd, ...)
```

> A estrutura de pares intercalados nos arquivos de comércio exterior foi o maior desafio de parsing — cada ano ocupa duas colunas, não uma. Foi necessário implementar um parser customizado com `step=2` sobre os dados.

### Datasets

| Arquivo (nome no repositório) | Tipo | Linhas | Período | Unidade |
|-------------------------------|------|--------|---------|---------|
| `producao_vinhos_1970-2019.csv` | Produção | 2.250 | 1970–2019 | Litros |
| `comercializacao_vinhos_1970-2019.csv` | Comercialização | 3.050 | 1970–2019 | Litros |
| `uvas_americanas_1970-2018.csv` | Processamento | 2.744 | 1970–2018 | Kg |
| `uvas_viniferas_1970-2018.csv` | Processamento | 6.517 | 1970–2018 | Kg |
| `uvas_mesa_1970-2018.csv` | Processamento | 490 | 1970–2018 | Kg |
| `uvas_sem_class_1970-2018.csv` | Processamento | 49 | 1970–2018 | Kg |
| `exportacao_vinhos_1970-2019.csv` | Exportação | 5.350 | 1970–2019 | Kg + USD |
| `exportacao_espumantes_1970-2019.csv` | Exportação | 4.300 | 1970–2019 | Kg + USD |
| `exportacao_suco_1970-2019.csv` | Exportação | 5.250 | 1970–2019 | Kg + USD |
| `exportacao_uvas_frescas_1970-2019.csv` | Exportação | 5.250 | 1970–2019 | Kg + USD |
| `importacao_vinhos_1970-2019.csv` | Importação | 2.850 | 1970–2019 | Kg + USD |
| `importacao_espumantes_1970-2019.csv` | Importação | 2.050 | 1970–2019 | Kg + USD |
| `importacao_suco_1970-2019.csv` | Importação | 1.450 | 1970–2019 | Kg + USD |
| `importacao_uvas_frescas_1970-2019.csv` | Importação | 900 | 1970–2019 | Kg + USD |
| `importacao_uvas_passas_1970-2019.csv` | Importação | 1.650 | 1970–2019 | Kg + USD |

> **Atenção sobre nomes de arquivo:** os arquivos originais da Embrapa usam caracteres especiais (`ç`, `ã`, `é`) nos nomes. O git/Streamlit Cloud corrompe esses nomes em sistemas Linux como `__Importa├º├úo__`. Todos os arquivos foram renomeados para ASCII puro antes do commit.

---

## 🗂️ Estrutura do projeto

```
projeto-embrapa/
├── main.py                           # Entrada — st.navigation() com 6 páginas
├── requirements.txt
├── [15 CSVs com nomes ASCII]         # Dados na raiz do projeto
├── .streamlit/
│   └── config.toml                   # Tema bordô escuro
│
├── pages/
│   ├── 0_Visao_Geral.py              # KPIs + série histórica + eventos + décadas
│   ├── 1_Producao.py                 # Produção por produto + comercialização + por década
│   ├── 2_Processamento.py            # Americanas vs Viníferas + variedades
│   ├── 3_Exportacoes.py              # Vinhos, espumantes, suco e uvas frescas
│   ├── 4_Importacoes.py              # Concorrência externa + balança comercial
│   └── 5_Conclusoes.py               # 6 grandes achados + painel comparativo
│
└── util/
    ├── constants.py                  # Paleta de cores, 9 eventos históricos, PAIS_COLORS
    ├── data.py                       # Parsers + loaders com @st.cache_data
    ├── style.py                      # CSS Playfair Display + componentes HTML
    └── layout.py                     # Sidebar com info do projeto
```

---

## 🔍 Páginas e análises

### 🍇 Visão Geral
KPIs de destaque (vinho de mesa, suco, espumantes, queda de 2016). Série histórica de 50 anos com área sombreada por produto, 9 eventos climáticos e econômicos anotados diretamente no gráfico. Processamento americanas vs viníferas em barras empilhadas com destaque da geada de 2016. Mix de produtos por categoria 1970–2019. Cards de cada evento histórico com ano, descrição e impacto.

### 🍷 Produção & Comercialização
Três abas: tendências de todos os produtos (vinho mesa tinto/branco/rosado, suco integral/concentrado, espumantes) com destaque para a geada 2016; comercialização interna com destaque para o crescimento dos espumantes de 2000 a 2019; análise por década com cards comparativos de médias e extremos, gráfico de barras agrupado Anos 90/2000/2010.

### 🌿 Processamento de Uvas
Três abas: top 12 variedades de americanas e híbridas com ranking horizontal e evolução das 5 principais; top 12 viníferas finas (Cabernet Sauvignon, Merlot, Moscato, etc.) com análise de crescimento; comparativo proporcional e volumétrico americanas vs viníferas ao longo de 49 anos.

### ✈️ Exportações
Quatro abas com eixo duplo kg/USD: vinhos de mesa com top destinos e análise da volatilidade; espumantes com crescimento de +657% em receita desde 2000 e preço médio por kg; suco de uva como campeão de receita com $4M exportados; uvas frescas com evolução do preço unitário.

### 🛬 Importações
Quatro abas: vinhos importados com o impacto da abertura comercial de 1994, Chile como dominador; espumantes importados com Itália/França no premium e Argentina no volume; análise da dependência argentina por todas as categorias; balança comercial mostrando déficit em vinhos/espumantes e superávit em suco.

### 💡 Conclusões
Seis grandes achados com análise narrativa. Painel comparativo de 6 indicadores-chave 1970 vs 2019. Ficha técnica completa.

---

## 📅 9 Eventos Históricos Mapeados

| Ano | Evento | Impacto |
|-----|--------|---------|
| 1973 | Seca severa RS | Pior safra dos anos 70 |
| 1980 | Geada + clima adverso | −38% na produção |
| 1983 | Seca · El Niño | −49% produção vinho mesa |
| 1994 | Plano Real | Abertura comercial — importações disparam |
| 2002 | Serra Gaúcha · geada | Queda pontual de produção |
| 2005 | Boom espumantes | Crescimento acelerado começa |
| 2010 | Recorde suco de uva | Suco ultrapassa 50M litros/ano |
| 2016 | **Geada catastrófica RS** | **−59% produção — pior ano desde 1973** |
| 2019 | Recorde espumantes | Maior exportação de espumantes |

---

## 📈 Principais números

| Indicador | Valor |
|-----------|-------|
| Vinho de mesa 1970 | 217M litros |
| Vinho de mesa 2019 | 145M litros |
| Pico de produção | 314M litros (2004) |
| Queda em 2016 (geada) | −59% em relação a 2015 |
| Suco de uva — crescimento 1990→2019 | +646% (10M → 78M litros) |
| Espumantes — crescimento 2000→2019 | +426% (4,3M → 22,8M litros) |
| Uvas americanas (% do processamento 2018) | 90% |
| Exportação total 2019 | $104,8M |
| Importação total 2019 | $450M |
| Déficit comercial em vinhos 2019 | −$338M |
| Superávit em suco de uva 2019 | +$4M |
| Chile — % das importações de vinho (2019) | 46% do volume total |

---

## 🧠 Decisões técnicas

**Parser customizado para dois formatos distintos**
Os arquivos de produção/processamento têm uma coluna por ano. Os de importação/exportação têm dois valores por ano (kg + USD) intercalados na mesma linha. Foi necessário implementar dois parsers separados: `_parse_production()` para o primeiro formato e `_parse_impexp()` com `step=2` para o segundo.

**Nomes de arquivo ASCII puro**
Os arquivos originais da Embrapa usam caracteres especiais (`Importação`, `Produção`, `Viníferas`). O git em sistemas Linux decodifica esses nomes com encoding diferente, resultando em nomes corrompidos como `__Importa├º├úo__` no Streamlit Cloud. Todos os 15 arquivos foram renomeados para ASCII puro antes do primeiro commit.

**Caminhos absolutos via `__file__`**
O `data.py` resolve os caminhos dos CSVs usando `os.path.dirname(os.path.abspath(__file__))` — não caminhos relativos. No Streamlit Cloud, o processo pode rodar de um diretório diferente do repositório, quebrando referências relativas.

**Categorias hierárquicas nos dados**
Os datasets de produção e comercialização têm dois níveis: categorias em MAIÚSCULAS são totais (ex.: `VINHO DE MESA`), categorias em mixed case são subcategorias (ex.: `Tinto`, `Branco`). A separação entre os dois níveis é feita por filtragem `.str.isupper()` para evitar dupla contagem nas análises agregadas.

**Design diferenciado no portfólio**
Este é o 5º projeto do portfólio. Para garantir identidade visual única: fundo bordô `#2A0A1A`, tipografia `Playfair Display` (serif) nos títulos, dourado `#C8972A` como cor de destaque, paleta de rosa/vinho/verde uva — completamente diferente dos outros quatro projetos (navy, cinza frio, dark amber, navy esmeralda).

---

## 💡 Principais achados analíticos

**Espumantes: a transformação mais importante dos últimos 20 anos**
De 4,3M litros em 2000 para 22,8M litros em 2019 (+426%). A receita de exportação cresceu +657% no mesmo período. A Serra Gaúcha encontrou seu nicho competitivo — espumantes de qualidade a preço acessível — e passou a competir com Prosecco e Cava na América Latina.

**Suco de uva: o campeão silencioso**
Único produto com superávit comercial consistente. Crescimento de +646% em 30 anos. O Brasil se consolidou como um dos maiores produtores mundiais, com os EUA como principal destino de exportação.

**2016: o evento climático mais destrutivo da série**
A geada de julho de 2016 na Serra Gaúcha causou queda de 59% na produção de vinho de mesa e 52% no suco de uva. Atingiu americanas (−58%) e viníferas (−54%) com intensidade similar. A recuperação total em 2017 demonstra resiliência — mas evidencia a vulnerabilidade climática estrutural da monocultura.

**O dilema do vinho de mesa: volume cai, qualidade sobe**
O pico foi em 2004 (314M litros). A queda subsequente não é crise — é transição estratégica. A indústria substituiu volume de vinho básico por espumantes e vinhos finos de maior valor agregado. O consumidor brasileiro se sofisticou.

**O impacto do Plano Real de 1994**
A abertura comercial inundou o mercado com vinhos chilenos e argentinos baratos. O Chile hoje representa 46% do volume de vinho importado — 52,7M kg em 2019. A resposta brasileira foi especialização, não competição direta no segmento de entrada.

**Americanas vs Viníferas: o dilema estrutural**
90% do processamento são uvas americanas e híbridas. São mais resistentes, produtivas e a base econômica das famílias da Serra Gaúcha. As viníferas representam 10% do volume mas geram os vinhos de exportação. Expandir viníferas sem destruir a base das americanas é o principal desafio estratégico da indústria.

---

## ⚙️ Como rodar localmente

```bash
git clone https://github.com/vinicius-souzaa/projeto-embrapa.git
cd projeto-embrapa
pip install -r requirements.txt
streamlit run main.py
```

### Dependências

| Pacote | Versão mínima |
|--------|---------------|
| streamlit | 1.36.0 |
| pandas | 2.0.0 |
| numpy | 1.24.0 |
| plotly | 5.15.0 |

---

## 👤 Autor

**Vinicius Abreu Ernestino Souza**
Data Analytics · São Paulo, SP

---

## 📄 Fonte dos dados

- [Embrapa Uva e Vinho — VITIBRASIL](http://vitibrasil.cnpuv.embrapa.br)
- Bento Gonçalves, RS — Brasil
- Dados públicos de acesso livre
