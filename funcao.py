from BaselineRemoval import BaselineRemoval
import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from sympy import sympify, lambdify, symbols
from matplotlib import pyplot as plt
import matplotlib

@st.cache_data
def importar(uploaded_file, ignor_cabecalho, delimitador, separador, linha_final=0):
    """
    Lê arquivos CSV segundo a semântica:
      - ignor_cabecalho: linha do cabeçalho (1-based). 0 = sem cabeçalho.
      - linha_final: positivo = número de linhas a partir do início dos dados;
                     negativo = posição contada a partir do final (-1 = última linha);
                     0 = até o fim.
    Retorna dicionário {nome_arquivo: DataFrame}.
    """
    import io

    ignor_cabecalho = int(ignor_cabecalho)
    header = None if ignor_cabecalho == 0 else ignor_cabecalho - 1

    if uploaded_file is None:
        st.stop()

    arquivos_pandas = {}
    lista_nomes = []

    for arquivo in uploaded_file:
        nome = arquivo.name.split(".")[0]
        lista_nomes.append(nome)

        # --- Determina número total de linhas apenas se linha_final < 0 ---
        total_lines = None
        if linha_final is not None and int(linha_final) < 0:
            # lê todo o conteúdo para contar linhas; depois reseta ponteiro
            try:
                pos = arquivo.tell()
            except Exception:
                pos = None
            arquivo.seek(0)
            content = arquivo.read()
            # content pode ser bytes ou str
            if isinstance(content, bytes):
                try:
                    text = content.decode("utf-8")
                except Exception:
                    text = content.decode("latin-1", errors="ignore")
            else:
                text = content
            total_lines = len(text.splitlines())
            # reset do ponteiro
            try:
                if pos is not None:
                    arquivo.seek(pos)
                else:
                    arquivo.seek(0)
            except Exception:
                pass

        # --- Interpretação simples de linha_final ---
        lf = None if (linha_final is None or int(linha_final) == 0) else int(linha_final)

        # se lf é None -> ler até o fim (nrows=None)
        nrows = None
        if lf is not None:
            if lf > 0:
                # positivo -> ler lf linhas a partir da primeira linha de dados
                nrows = lf
            else:
                # lf < 0 -> precisamos do total_lines
                if total_lines is None:
                    # contar se não contamos ainda
                    try:
                        pos = arquivo.tell()
                    except Exception:
                        pos = None
                    arquivo.seek(0)
                    cont = arquivo.read()
                    if isinstance(cont, bytes):
                        try:
                            cont_text = cont.decode("utf-8")
                        except Exception:
                            cont_text = cont.decode("latin-1", errors="ignore")
                    else:
                        cont_text = cont
                    total_lines = len(cont_text.splitlines())
                    try:
                        if pos is not None:
                            arquivo.seek(pos)
                        else:
                            arquivo.seek(0)
                    except Exception:
                        pass

                # -1 => última linha -> absolute_last_line = total_lines
                absolute_last_line = total_lines + lf + 1
                # primeira linha de dados (1-based)
                first_data_line = 1 if header is None else ignor_cabecalho + 1
                nrows = absolute_last_line - first_data_line + 1

            if nrows is None or nrows <= 0:
                raise ValueError(
                    f"linha_final={linha_final} resulta em intervalo vazio. "
                    f"Calcule uma linha_final válida (nrows={nrows})."
                )

        # --- Reset do ponteiro e leitura ---
        try:
            arquivo.seek(0)
        except Exception:
            pass

        df = pd.read_csv(
            arquivo,
            header=header,
            sep=delimitador,
            decimal=separador,
            nrows=nrows
        )

        # nomes únicos
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
