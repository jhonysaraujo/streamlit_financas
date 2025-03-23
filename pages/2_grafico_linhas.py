import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Gráfico de Linhas")

# Título da página
st.title("📈 Evolução dos Gastos")

# Carregar os dados do Excel
@st.cache_data
def load_data():
    return pd.read_excel("datasets/gastos.xlsx")

df = load_data()

# Criar sidebar com melhor organização
st.sidebar.header("📌 Filtros")

# Escolha do tipo de comparação em um menu dropdown (selectbox)
opcao_comparacao = st.sidebar.selectbox(
    "Selecione a forma de comparação:",
    ["Comparar meses", "Comparar categorias"]
)

# 🔹 Se a opção for "Comparar meses"
if opcao_comparacao == "Comparar meses":
    st.sidebar.subheader("Selecione os meses:")
    meses_disponiveis = list(df["Mês"].unique())
    meses_selecionados = st.sidebar.multiselect("Escolha os meses", meses_disponiveis, default=meses_disponiveis)

    # Filtrar os dados
    df_filtrado = df[df["Mês"].isin(meses_selecionados)]

    # Criar gráfico
    st.subheader("📌 Comparação dos Gastos entre Meses")

    # Calcular total de gastos por mês
    gastos_totais_mes = df_filtrado.groupby("Mês")["Valor Total (R$)"].sum()

    # Criar gráfico
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(gastos_totais_mes.index, gastos_totais_mes.values, marker="o", linestyle="-", color="blue", linewidth=2)

    # Adicionar rótulos nos pontos
    for i, (mes, valor) in enumerate(zip(gastos_totais_mes.index, gastos_totais_mes.values)):
        ax.text(mes, valor, f"R$ {valor:,.2f}", ha="center", va="bottom", fontsize=9, color="black")

    ax.set_xlabel("Mês")
    ax.set_ylabel("Valor Total (R$)")
    ax.set_title("Evolução dos Gastos Totais")
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)

# 🔹 Se a opção for "Comparar categorias"
elif opcao_comparacao == "Comparar categorias":
    st.sidebar.subheader("Selecione as categorias:")
    categorias_disponiveis = list(df["Categoria"].unique())

    # Botões de selecionar todas ou limpar
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Selecionar Todas"):
        categorias_selecionadas = categorias_disponiveis
    elif col2.button("Limpar Seleção"):
        categorias_selecionadas = []
    else:
        categorias_selecionadas = st.sidebar.multiselect("Escolha as categorias", categorias_disponiveis, default=categorias_disponiveis)

    # Filtrar os dados
    df_filtrado = df[df["Categoria"].isin(categorias_selecionadas)]

    # Criar gráfico
    st.subheader("📌 Evolução das Categorias ao Longo dos Meses")

    # Calcular gastos por categoria ao longo dos meses
    gastos_categoria_mes = df_filtrado.groupby(["Mês", "Categoria"])["Valor Total (R$)"].sum().unstack()

    # Criar gráfico
    fig, ax = plt.subplots(figsize=(10, 5))

    # Criar linha para cada categoria
    if gastos_categoria_mes is not None:  # Evita erro se estiver vazio
        for categoria in gastos_categoria_mes.columns:
            ax.plot(
                gastos_categoria_mes.index, gastos_categoria_mes[categoria],
                marker="o", linestyle="--", label=categoria, alpha=0.7
            )

    ax.set_xlabel("Mês")
    ax.set_ylabel("Valor Total (R$)")
    ax.set_title("Evolução dos Gastos por Categoria")
    ax.legend(title="Categorias", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)
