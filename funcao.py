from BaselineRemoval import BaselineRemoval
import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from sympy import sympify, lambdify, symbols
from matplotlib import pyplot as plt
import matplotlib

@st.cache_data
@st.cache_data
def importar(uploaded_file, ignor_cabecalho, delimitador, separador, linha_final=None):
    """
    Cria os dataframes pandas recebidos da variavel uploaded_file.

    Args:
        uploaded_file: Lista de dados importados para realizar a conversão para dataframes.
        ignor_cabecalho: Linha do cabeçalho (1-based). Use 0 para indicar "sem cabeçalho".
        delimitador: Delimitador das colunas.
        separador: Separador decimal dos dados.
        linha_final: Última linha a ser lida (1-based). Se None, lê até o fim.

    Returns:
        arquivos_pandas: Dicionário com os dataframes importados.
    """
    # header: None (sem header) ou 0-based index da linha do header
    header = None if int(ignor_cabecalho) == 0 else int(ignor_cabecalho) - 1

    lista_nomes = []
    if uploaded_file is None:
        st.stop()

    arquivos_pandas = {}
    for arquivo in uploaded_file:
        nome = arquivo.name.split(".")[0]
        lista_nomes.append(nome)

        # Calcula nrows com base na semântica escolhida:
        # - Se header é None (sem header): queremos ler até a linha `linha_final` (1-based),
        #   então nrows = linha_final (porque leitura começa na linha 1).
        # - Se header está em uma linha >0: pandas usa essa linha como header e os dados
        #   começam na próxima linha; então nrows = linha_final - ignor_cabecalho.
        nrows = None
        if linha_final is not None:
            linha_final = int(linha_final)
            if header is None:
                nrows = linha_final
                if nrows <= 0:
                    raise ValueError("linha_final deve ser >= 1")
            else:
                nrows = linha_final - int(ignor_cabecalho)
                if nrows <= 0:
                    raise ValueError("linha_final deve ser maior que a linha do cabeçalho (ignor_cabecalho)")

        # Leitura: NÃO usar skiprows para não causar deslocamento duplo
        df = pd.read_csv(
            arquivo,
            header=header,
            sep=delimitador,
            decimal=separador,
            nrows=nrows
        )

        # Garante nomes únicos
        if nome not in arquivos_pandas:
            arquivos_pandas[nome] = df
        else:
            arquivos_pandas[f"{nome}({lista_nomes.count(nome)-1})"] = df

    return arquivos_pandas



class criar_grafico_plotly:
    def __init__(self, dados_pandas, coluna_x, colunas_y, nome_arquivo):
        self.fig = go.Figure()
        self.dados = dados_pandas
        self.names = {}
        self.coluna_x = coluna_x
        self.colunas_de_interrese = colunas_y
        self.nome_arquivo = nome_arquivo

    def grafico(self):
        """
        Cria a figrua do grafico em plotly utilizando os dados pandas.
        Args:
            dado_pandas: dados em tabela pandas
        Return:
            figura: imagem gerada com plotly.
        """
        assert isinstance(self.dados, dict)

        cmap, num, norm = self.mapa_cor()

        for key, valor in self.dados.items():

            colunas = valor.columns
            if len(colunas) == 2:
                num += 1
                self.fig = self.fig.add_trace(
                    go.Scatter(
                        x=valor[colunas[0]],
                        y=valor[colunas[1]],
                        name=key,
                        mode="lines",
                        line=dict(color=matplotlib.colors.to_hex(cmap(norm(num)))),
                    )
                )
                if key in self.names.keys():
                    self.names[f"{key}_(1)"] = len(self.names)
                else:
                    self.names[key] = len(self.names)
            else:
                for col in self.colunas_de_interrese:
                    num += 1
                    if self.nome_arquivo:
                        nome = key
                    else:
                        nome = col
                    self.fig = self.fig.add_trace(
                        go.Scatter(
                            x=valor[self.coluna_x],
                            y=valor[col],
                            name=nome,
                            mode="lines",
                            line=dict(color=matplotlib.colors.to_hex(cmap(norm(num)))),
                        )
                    )

                    if nome in self.names.keys():
                        self.names[f"{nome}_(1)"] = len(self.names)
                    else:
                        self.names[nome] = len(self.names)

    def mapa_cor(self):
        cmap = plt.get_cmap("cool")
        num = 0
        norm = plt.Normalize(
            vmin=0,
            vmax=sum(
                [
                    (
                        len(valor.columns)
                        if len(valor.columns) == 2
                        else len(valor.columns) - 1
                    )
                    for valor in self.dados.values()
                ]
            ),
        )
        
        return cmap,num,norm


def reescreve_latex(string, mudar):
    if mudar:
        função = sympify(string)
        return função


def utilizar_equação(dicionario, colunas, função):
    x = symbols("x")
    funcao_lambda = lambdify(x, função, modules="numpy")
    for chaves in dicionario.keys():
        for coluna in colunas:
            dado_mudar = dicionario[chaves][coluna].values
            dicionario[chaves][coluna] = funcao_lambda(dado_mudar)


def baseline_remov(dicionario):
    for chaves in dicionario.keys():
        for coluna in dicionario[chaves].columns[1::]:
            baseObj = BaselineRemoval(dicionario[chaves][coluna])
            dicionario[chaves][coluna] = baseObj.ZhangFit()


def normaliza(dicionario, x_min, x_max):
    for chaves in dicionario.keys():
        x = dicionario[chaves].columns[0]
        parametro_min = dicionario[chaves][x] >= x_min
        parametro_max = dicionario[chaves][x] <= x_max
        intervalo = dicionario[chaves][parametro_min & parametro_max]
        for coluna in dicionario[chaves].columns[1::]:
            valor_maximo = intervalo[coluna].max()
            valor_minimo = intervalo[coluna].min()
            dicionario[chaves][coluna] = (dicionario[chaves][coluna] - valor_minimo) / (
                valor_maximo - valor_minimo
            )


def definir_max_min(dicionario):
    lista = []
    for df in dicionario.values():
        coluna = df.columns[0]
        lista.append(df[coluna].min())
        lista.append(df[coluna].max())
    maximo = max(lista)
    minimo = min(lista)
    return maximo, minimo


def separar(dicionario, valor,ys):
    espacamento = 0
    for chaves in dicionario.keys():
        if ys==0:
            for coluna in dicionario[chaves].columns[1::]:
                dicionario[chaves][coluna] = dicionario[chaves][coluna] + espacamento
                espacamento += valor
        else:
            for coluna in ys:
                dicionario[chaves][coluna] = dicionario[chaves][coluna] + espacamento
                espacamento += valor


def limitar(dicionario, valor_min, valor_max):
    for chaves in dicionario.keys():
        x = dicionario[chaves].columns[0]
        parametro_min = dicionario[chaves][x] >= valor_min
        parametro_max = dicionario[chaves][x] <= valor_max
        dicionario[chaves] = dicionario[chaves][parametro_min & parametro_max]


def config_page():
    # Dados da pagina
    st.set_page_config(
        page_title="CastorPlot",
        page_icon=r"imagem/CASTORPLOT.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inicial():
    ####################################Contatos################
    st.sidebar.image(r"imagem/CASTORPLOT.png")

    st.sidebar.title("Contato")

    st.sidebar.write("Envie erros, duvidas ou sugestões no github do site.")
    st.sidebar.write("[GitHub e manual do site](https://github.com/guidarianiapps/Castorplot)")
    st.sidebar.write("[GitHub pessoal](https://github.com/guidariani)")
    st.sidebar.write("[GitHub acadêmico](https://github.com/guilhermeilum)")

    st.sidebar.write("[Mais contatos](https://linktr.ee/guidariani)")

    st.sidebar.write("Autor: Guilherme Gurian Dariani")

    st.sidebar.write(
        """Em nenhum caso o autor será responsável por quaisquer erros, resultados ou informações incorretas."""
    )
