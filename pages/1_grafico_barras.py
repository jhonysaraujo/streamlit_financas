import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página (sem layout wide)
st.set_page_config(page_title="Gráfico de Barras")

# Título da página
st.title("📊 Comparação dos Gastos por Categoria")

# Carregar os dados do Excel
@st.cache_data
def load_data():
    return pd.read_excel("datasets/gastos.xlsx")

df = load_data()

# Criar checkboxes para selecionar múltiplos meses
st.sidebar.header("Filtros")
meses_disponiveis = list(df["Mês"].unique())
meses_selecionados = st.sidebar.multiselect("Selecione um ou mais meses:", meses_disponiveis, default=meses_disponiveis)

# Aplicar o filtro de meses para o gráfico de barras
df_barras = df[df["Mês"].isin(meses_selecionados)] if meses_selecionados else df

# Calcular os gastos por categoria
gastos_por_categoria = df_barras.groupby("Categoria")["Valor Total (R$)"].sum().sort_values(ascending=False)

# 🔹 GRÁFICO: BARRAS HORIZONTAIS COM VALORES E PERCENTUAIS
st.subheader(f"📌 Gastos por Categoria ({', '.join(meses_selecionados)})")

# Calcular total gasto e percentuais
total_gasto = gastos_por_categoria.sum()
percentuais = (gastos_por_categoria / total_gasto) * 100  

# Criar o gráfico
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(gastos_por_categoria.index, gastos_por_categoria.values, color="mediumseagreen")

# Adicionar rótulos de valores e percentuais ao lado de cada barra
for bar, valor, perc in zip(bars, gastos_por_categoria.values, percentuais):
    ax.text(
        bar.get_width() + total_gasto * 0.01,  # Ajuste para espaçamento correto
        bar.get_y() + bar.get_height() / 2,  # Centraliza na barra
        f"R$ {valor:,.2f}  ({perc:.1f}%)",  # Exibe R$ e percentual
        va="center", fontsize=10, color="black"
    )

# Ajustar títulos e rótulos
ax.set_xlabel("Valor Total (R$)")
ax.set_ylabel("Categoria")
ax.set_title("Gastos por Categoria")

# Exibir o gráfico no Streamlit
st.pyplot(fig)
