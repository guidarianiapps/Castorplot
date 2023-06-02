from BaselineRemoval import BaselineRemoval
import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objs as go


@st.cache_data
def importar(uploaded_file, ignor_cabecalho, delimitador, separador):
    """
    Cria os dataframes pandas recebidos da variavel uploaded_file.
    Args:
        uploaded_file: Lista de dados importados para realizar a conversão para dataframes.

        ignor_cabecalho: Quantas linhas do cabeçlho devem ser ignoradas

        delimitador: Delimitador das colunas.

        separador: Separador decimal dos dados.

    Returns:
        arquivos_pandas: Lista dos dataframes importados,
    """
    numero_cabeçalho = (
        None if int(ignor_cabecalho) == 0 else int(ignor_cabecalho) - 1
    )  # Arrumar cabeçalho
    lista_nomes = []
    if uploaded_file is not None:
        arquivos_pandas = {}
        for arquivo in uploaded_file:
            nome = arquivo.name.split(".")[0]
            lista_nomes.append(nome)
            if nome not in arquivos_pandas.keys():
                arquivos_pandas[nome] = pd.read_csv(
                    arquivo, header=numero_cabeçalho, sep=delimitador, decimal=separador
                )
            else:
                arquivos_pandas[nome + f"({lista_nomes.count(nome)-1})"] = pd.read_csv(
                    arquivo, header=numero_cabeçalho, sep=delimitador, decimal=separador
                )
            # cria lista com todos os aquivos em pandas.
    else:  # para o programa se uploaded_file is None, não precisaria, pois já existe no programa esse if, porêm estava tendo aviso
        st.stop()
    return arquivos_pandas


class criar_grafico_plotly:
    def __init__(self, dados_pandas):
        self.fig = go.Figure()
        self.dados = dados_pandas
        self.names = []

    def grafico(self):
        """
        Cria a figrua do grafico em plotly utilizando os dados pandas.
        Args:
            dado_pandas: dados em tabela pandas
        Return:
            figura: imagem gerada com plotly.
        """
        assert isinstance(self.dados, dict)
        for key, valor in self.dados.items():
            colunas = valor.columns
            if len(colunas) == 2:
                self.fig = self.fig.add_trace(
                    go.Scatter(
                        x=valor[colunas[0]], y=valor[colunas[1]], name=key, mode="lines"
                    )
                )
                self.names.append(key)
            else:
                for col in colunas[1::]:
                    self.fig = self.fig.add_trace(
                        go.Scatter(
                            x=valor[colunas[0]], y=valor[col], name=col, mode="lines"
                        )
                    )
                    self.names.append(col)



def baseline_remov(dicionario):
    for chaves in dicionario.keys():
        for coluna in dicionario[chaves].columns[1::]:
            baseObj = BaselineRemoval(dicionario[chaves][coluna])
            dicionario[chaves][coluna] = baseObj.ZhangFit()



def normaliza(dicionario, x_min, x_max):
    for chaves in dicionario.keys():
        x = dicionario[chaves].columns[0]
        parametro_min = dicionario[chaves][x] > x_min
        parametro_max = dicionario[chaves][x] < x_max
        intervalo = dicionario[chaves][parametro_min & parametro_max]
        for coluna in dicionario[chaves].columns[1::]:
            valor_maximo = intervalo[coluna].max()
            dicionario[chaves][coluna] = dicionario[chaves][coluna] / valor_maximo



def definir_max_min(dicionario):
    lista = []
    for df in dicionario.values():
        coluna = df.columns[0]
        lista.append(df[coluna].min())
        lista.append(df[coluna].max())
    maximo = max(lista)
    minimo = min(lista)
    return maximo, minimo



def separar(dicionario, valor):
    espacamento = 0
    for chaves in dicionario.keys():
        for coluna in dicionario[chaves].columns[1::]:
            dicionario[chaves][coluna] = dicionario[chaves][coluna] + espacamento
            espacamento += valor



def limitar(dicionario, valor_min, valor_max):
    for chaves in dicionario.keys():
        x = dicionario[chaves].columns[0]
        parametro_min = dicionario[chaves][x] >= valor_min
        parametro_max = dicionario[chaves][x] <= valor_max
        dicionario[chaves] = dicionario[chaves][parametro_min & parametro_max]