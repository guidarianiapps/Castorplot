import pandas as pd
import plotly.graph_objects as go
from BaselineRemoval import BaselineRemoval
import streamlit as st
import os
import numpy as np


def plot_dados(uploaded_files, fig, lista_removal_baseline):
    for index_lista in range(len(lista_removal_baseline)):
        arquivo, extensao = os.path.splitext(uploaded_files[index_lista].name)
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
        baseObj = BaselineRemoval(df["y"])
        df["y"] = baseObj.ZhangFit()
        df = df.loc[logic & logic1]
        lista_removal_baseline.append(df)
    return lista_removal_baseline


st.title("Raman")
st.write("### Coloque os arquivos renomeados com o nome da legenda de cada arquivo!!")
uploaded_files = st.file_uploader(
    "Coloque os dados txt aqui", accept_multiple_files=True
)
arquivo_exemplo = open(r"dados\GO_exemplo.txt")
st.download_button("Exemplo de arquivo",arquivo_exemplo,file_name="arquivo_exemplo.txt")
arquivo_exemplo.close()

if uploaded_files == []: ## Esperar algum arquivo
    st.stop()


fig = go.Figure()
nome = st.empty()
lista_dados = []
for numero in range(len(uploaded_files)):
    df = pd.read_csv(uploaded_files[numero], names=["x", "y"], sep="\t")
    lista_dados.append(df)
x_minimo_original = min([i["x"].values.min() for i in lista_dados])
x_maximo_original = max([i["x"].values.max() for i in lista_dados])
value_escala = st.slider(
    'Selecione o intervalo de x',
    x_minimo_original, x_maximo_original, (float(x_minimo_original), float(x_maximo_original)))

lista_removal_baseline = baseline_remov_min_max(lista_dados, value_escala[0], value_escala[1])

fig = plot_dados(uploaded_files, fig, lista_removal_baseline)
st.plotly_chart(fig, use_container_width=True)