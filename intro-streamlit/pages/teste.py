import streamlit as st

st.title("Carregando um arquivo")
data = st.file_uploader("Escolha uma imagem", type=["csv"])

# Cria duas colunas para a página
col_a, col_b = st.columns(2)

if data is None:
    st.warning("Nenhum arquivo carregado")
else:
    # carrega o dataframe
    import pandas as pd
    df = pd.read_csv(data)
    df = df[df.columns[1:]]
    colunas = st.multiselect("Escolha uma coluna", df.columns)
    if colunas:
        df[colunas]
        
    
