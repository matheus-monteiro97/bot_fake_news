import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# ------------------------
# Configuração da página
# ------------------------

st.set_page_config(
    page_title="Bot Protetor de Golpes",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Dashboard - Bot Protetor de Golpes")

# ------------------------
# Banco de dados
# ------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE = BASE_DIR / "data" / "analysis_history.db"


@st.cache_data
def load_data():

    conn = sqlite3.connect(str(DATABASE))

    df = pd.read_sql_query(
        """
        SELECT *
        FROM analyses
        ORDER BY data DESC
        """,
        conn
    )

    conn.close()

    return df


df = load_data()

# ------------------------
# Caso ainda não exista dado
# ------------------------

if len(df) == 0:

    st.warning("Nenhuma análise encontrada.")

    st.stop()

# ------------------------
# Conversão da data
# ------------------------

df["data"] = pd.to_datetime(df["data"])

# ------------------------
# Sidebar
# ------------------------

st.sidebar.header("Filtros")

categorias = st.sidebar.multiselect(

    "Categoria",

    options=df["categoria"].unique(),

    default=df["categoria"].unique()

)

tipos = st.sidebar.multiselect(

    "Tipo",

    options=df["tipo"].unique(),

    default=df["tipo"].unique()

)

df_filtrado = df[
    (df["categoria"].isin(categorias))
    &
    (df["tipo"].isin(tipos))
]

# ------------------------
# Métricas
# ------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total de análises",
        len(df_filtrado)
    )

with col2:

    st.metric(
        "Score médio",
        round(df_filtrado["score"].mean(), 1)
    )

with col3:

    suspeitos = len(
        df_filtrado[
            df_filtrado["score"] >= 35
        ]
    )

    st.metric(
        "Conteúdos suspeitos",
        suspeitos
    )

with col4:

    alto_risco = len(
        df_filtrado[
            df_filtrado["score"] >= 70
        ]
    )

    st.metric(
        "Alto risco",
        alto_risco
    )

# ------------------------
# Gráficos
# ------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Distribuição por categoria")

    categoria_df = (

        df_filtrado

        .groupby("categoria")

        .size()

        .reset_index(name="Quantidade")

    )

    fig = px.bar(

        categoria_df,

        x="categoria",

        y="Quantidade"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    st.subheader("🥧 Categorias")

    fig = px.pie(

        categoria_df,

        values="Quantidade",

        names="categoria"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------
# Evolução temporal
# ------------------------

st.subheader("📈 Evolução das análises")

por_dia = (

    df_filtrado

    .groupby(

        df_filtrado["data"].dt.date

    )

    .size()

    .reset_index(name="Quantidade")

)

fig = px.line(

    por_dia,

    x="data",

    y="Quantidade",

    markers=True

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------
# Distribuição dos scores
# ------------------------

st.subheader("📉 Distribuição dos scores")

fig = px.histogram(

    df_filtrado,

    x="score",

    nbins=20

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------
# Top 10 mais perigosos
# ------------------------

st.subheader("🔥 Top 10 conteúdos mais suspeitos")

top10 = (

    df_filtrado

    .sort_values(

        by="score",

        ascending=False

    )

    .head(10)

)

st.dataframe(

    top10[
        [
            "data",
            "tipo",
            "categoria",
            "score",
            "texto"
        ]
    ],

    use_container_width=True

)

# ------------------------
# Histórico completo
# ------------------------

st.subheader("📋 Histórico completo")

pesquisa = st.text_input(
    "Pesquisar texto"
)

if pesquisa:

    tabela = df_filtrado[
        df_filtrado["texto"]
        .str.contains(
            pesquisa,
            case=False,
            na=False
        )
    ]

else:

    tabela = df_filtrado

st.dataframe(

    tabela[
        [
            "data",
            "tipo",
            "categoria",
            "score",
            "texto"
        ]
    ],

    use_container_width=True

)