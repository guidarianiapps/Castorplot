import pandas as pd
import streamlit as st
import funções


# Dados da pagina
st.set_page_config(page_title="CastorPlot", layout="wide")

# Contatos
st.sidebar.title("Contato")

st.sidebar.write("Envie erros, duvidas ou sugestões no email.")
st.sidebar.write("[E-mail](mailto:guidarianiapps@gmail.com)")
st.sidebar.write("[GitHub pessoal](https://github.com/guidariani)")
st.sidebar.write("[GitHub acadêmico](https://github.com/guilhermeilum)")
st.sidebar.write("[GitHub deste site](https://github.com/guidarianiapps)")

st.sidebar.write("[Mais contatos](https://linktr.ee/guidariani)")


st.sidebar.write("Autor: Guilherme Gurian Dariani")

st.sidebar.write(
    """Em nenhum caso o autor será responsável por quaisquer erros, resultados ou informações incorretas."""
)


st.header(
    "Um site para qualquer pessoa poder utilizar para efetuar um pré-tratamento rápido dos dados dos equipamentos e plotá-los."
)
colunas_import = st.columns(2)
with colunas_import[0]:
    uploaded_file = st.file_uploader(
        "Envie os arquivos que deseja utilizar.",
        accept_multiple_files=True,
        type=[".csv", ".txt"],
    )

    if uploaded_file == []:
        st.warning("Envie um arquivo antes de continuar")
        st.stop()
with colunas_import[1]:
    ignor_cabecalho = st.number_input(
        "Quantas linhas do cabeçalho deseja ignorar?", value=0, min_value=0
    )

    delimitador = st.text_input("Qual é o delimitador de coluna?", value=",")

    separador = st.text_input("Qual é o separador decimal?", value=".")

    tipo_tabela = st.selectbox(
        "Como é o tipo de tabela que irá trabalhar?",
        ("Primeira coluna x e uma ou mais y", "Leitor de placas"),
    )  # Qual tipo de tabela o usuario irá trabalhar.

if separador == "" or delimitador == "":
    if delimitador == "":
        st.warning("Escreva um delimitador de coluna.")
    if separador == "":
        st.warning("Escreva um separador decimal.")
    st.stop()

numero_cabeçalho = (
    None if int(ignor_cabecalho) == 0 else int(ignor_cabecalho) - 1
)  # Arrumar cabeçalho

if uploaded_file is not None:
    arquivos_pandas = [
        pd.read_csv(
            arquivo, header=numero_cabeçalho, sep=delimitador, decimal=separador
        )
        for arquivo in uploaded_file
    ]  # cria lista com todos os aquivos em pandas.
else:  # para o programa se uploaded_file is None, não precisaria, pois já existe no programa esse if, porêm estava tendo aviso
    st.stop()

# Mudar nome das colunas
for index in range(len(arquivos_pandas)):
    colunas = arquivos_pandas[index].columns
    if list(colunas) == list(range(len(colunas))):
        arquivos_pandas[index].columns = [f"x_{index}"] + [
            f"y_{index}_{i}" for i in range(len(colunas) - 1)
        ]

colunas_tabelas = st.columns(len(arquivos_pandas))  # cria as colunas para as tabelas

for index in range(len(arquivos_pandas)):  # mostra as tabelas importadas
    with colunas_tabelas[index]:
        st.write(arquivos_pandas[index])

figura = funções.criar_grafico(arquivos_pandas[0])
st.bokeh_chart(figura, use_container_width=True)