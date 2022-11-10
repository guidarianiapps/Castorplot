import pandas as pd
import plotly.graph_objects as go
from BaselineRemoval import BaselineRemoval
import streamlit as st


def plot_dados(uploaded_files, lista_removal_baseline):
    fig = go.Figure()
    for index_lista in range(len(lista_removal_baseline)):
        arquivo = uploaded_files[index_lista].name[:-4]
        fig = fig.add_trace(
            go.Scatter(
                x=lista_removal_baseline[index_lista]["x"],
                y=lista_removal_baseline[index_lista]["y"],
                name=arquivo,
            )
        )

    return fig


def baseline_remov_min_max(lista_dados, x_minimo, x_maximo):
    lista_removal_baseline = []
    for df in lista_dados:
        logic = df["x"] > x_minimo
        logic1 = df["x"] < x_maximo
        df = df.loc[logic & logic1]
        baseObj = BaselineRemoval(df["y"])
        df["y"] = baseObj.ZhangFit()
        lista_removal_baseline.append(df)
    return lista_removal_baseline


st.title("Raman")
st.write("### Coloque os arquivos renomeados com o nome da legenda de cada arquivo!!")
uploaded_files = st.file_uploader(
    "Coloque os dados txt aqui", accept_multiple_files=True
)
st.write(
    "[Arquivo de exemplo](https://github.com/guilhermeilum/app_equipamentos/blob/testes/dados/GO_exemplo.txt)"
)
if uploaded_files == []:  ## Esperar algum arquivo
    st.stop()

nome = st.empty()
lista_dados = []
for numero in range(len(uploaded_files)):
    df = pd.read_csv(uploaded_files[numero], names=["x", "y"], sep="\t")
    lista_dados.append(df)

colunas = st.columns(len(uploaded_files))
for index_col in range(len(uploaded_files)):
    with colunas[index_col]:
        arquivo = uploaded_files[index_col].name[:-4]
        st.write("#### ", arquivo)
        st.write(lista_dados[index_col].head(5))
        
fig_normal = plot_dados(uploaded_files,lista_dados)
st.plotly_chart(fig_normal, use_container_width=True)

x_minimo_original = min([i["x"].values.min() for i in lista_dados])
x_maximo_original = max([i["x"].values.max() for i in lista_dados])
coluna_começo = st.columns(2)
with coluna_começo[0]:
    value_escala = st.slider(
        "Selecione o intervalo de x",
        x_minimo_original,
        x_maximo_original,
        (float(x_minimo_original), float(x_maximo_original)),
    )
with coluna_começo[1]:
    distancia_linhas = st.number_input(
        "Qual a distancia em y entre as linhas.", min_value=0
    )
col1, col2, col3 = st.columns(3)
with col1:
    normalizar = st.checkbox("Normalizar Graficos")
with col2:
    x_min_norm = st.number_input(
        "Qual é o x mínimo do pico da normalização.", max_value=x_maximo_original
    )
with col3:
    x_max_norm = st.number_input(
        "Qual é o x maximo do pico da normalização.", max_value=x_maximo_original
    )
lista_removal_baseline = baseline_remov_min_max(
    lista_dados, value_escala[0], value_escala[1]
)

if normalizar:
    lista_nova_dados = []
    for df in lista_removal_baseline:
        logic = df["x"] > x_min_norm
        logic1 = df["x"] < x_max_norm
        valor_maximo = df.loc[logic & logic1]["y"].max()
        df["y"] = df["y"] / valor_maximo
        lista_nova_dados.append(df)
    if distancia_linhas > 0:
        distancia = 0
        for i in lista_nova_dados:
            i["y"] = i["y"] + distancia
            distancia += distancia_linhas
    Grafico_baselineremoval = plot_dados(
        uploaded_files, lista_nova_dados
    )

else:
    if distancia_linhas > 0:
        distancia = 0
        for i in lista_removal_baseline:
            i["y"] = i["y"] + distancia
            distancia += distancia_linhas
    Grafico_baselineremoval = plot_dados(
        uploaded_files, lista_removal_baseline
    )

st.plotly_chart(Grafico_baselineremoval, use_container_width=True)
