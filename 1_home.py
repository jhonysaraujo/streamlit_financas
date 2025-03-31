import streamlit as st
import pandas as pd
import datetime

# Configuração da página para layout amplo
st.set_page_config(page_title="Gestão de Gastos", layout="wide")

# Título do app
st.title("Gestão de Gastos Pessoais")

# Carregar os dados do Excel
@st.cache_data
def load_data():
    return pd.read_excel("datasets/gastos.xlsx")

df = load_data()

# Dicionário com meses no formato desejado
meses_formatados = {
    1: "1. Janeiro", 2: "2. Fevereiro", 3: "3. Março",
    4: "4. Abril", 5: "5. Maio", 6: "6. Junho",
    7: "7. Julho", 8: "8. Agosto", 9: "9. Setembro",
    10: "10. Outubro", 11: "11. Novembro", 12: "12. Dezembro"
}

# Mês atual no formato "3. Março", por exemplo
mes_atual_formatado = meses_formatados[datetime.datetime.now().month]

# Criar barra lateral para os filtros
st.sidebar.header("Filtros")

# Filtro de Tipo com checkboxes
tipos_disponiveis = df["Tipo"].unique()
tipo_selecionado = [tipo for tipo in tipos_disponiveis if st.sidebar.checkbox(f"Incluir {tipo}", value=True)]

# Filtro de Mês e Categoria na sidebar
meses_disponiveis = ["Todos"] + list(df["Mês"].unique())
indice_mes_padrao = meses_disponiveis.index(mes_atual_formatado) if mes_atual_formatado in meses_disponiveis else 0
mes_selecionado = st.sidebar.selectbox("Selecione o mês:", meses_disponiveis, index=indice_mes_padrao)

categorias_disponiveis = ["Todos"] + list(df["Categoria"].unique())
categoria_selecionada = st.sidebar.selectbox("Selecione a categoria:", categorias_disponiveis)

# Aplicar os filtros ao dataframe
df_filtrado = df[df["Tipo"].isin(tipo_selecionado)]

if mes_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Mês"] == mes_selecionado]

if categoria_selecionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria_selecionada]

# Calcular o gasto total
gasto_total = df_filtrado["Valor Total (R$)"].sum() if not df_filtrado.empty else 0

# Exibir o total gasto
st.metric(label="Total Gasto (R$)", value=f"R$ {gasto_total:,.2f}")

# Exibir a tabela de gastos filtrados
if df_filtrado.empty:
    st.warning("Nenhum gasto encontrado para essa seleção. Tente outro filtro.")
else:
    st.dataframe(df_filtrado, use_container_width=True)
