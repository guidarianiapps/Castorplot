import pandas as pd
import plotly.graph_objects as go
from BaselineRemoval import BaselineRemoval
import streamlit as st


def plot_dados(uploaded_files, lista):
    fig = go.Figure()
    for index_lista in range(len(lista)):
        arquivo = uploaded_files[index_lista].name[:-4]
        fig = fig.add_trace(
            go.Scatter(
                x=lista[index_lista]["x"],
                y=lista[index_lista]["y"],
                name=arquivo,
            )
        )

    return fig


def baseline_remov(lista_dados):
    lista_removal_baseline = []
    for df in lista_dados:
        baseObj = BaselineRemoval(df["y"])
        df["y"] = baseObj.ZhangFit()
        lista_removal_baseline.append(df)
    return lista_removal_baseline


def cortar_dados(lista_dados, x_minimo, x_maximo):
    lista_nova = []
    for df in lista_dados:
        logic = df["x"] > x_minimo
        logic1 = df["x"] < x_maximo
        df = df.loc[logic & logic1]
        lista_nova.append(df)
    lista_dados = lista_nova
    return lista_dados


def juntar_df(uploaded_files, lista):
    for index_lista in range(len(lista)):
        arquivo = uploaded_files[index_lista].name[:-4]
        x = "x_" + arquivo
        y = "y_" + arquivo
        lista[index_lista].rename(columns={"x": x, "y": y}, inplace=True)
    df = pd.concat(lista, axis=1, join="inner")
    return df


@st.cache
def convert_csv(df):
    return df.to_csv().encode("utf-8")
#Contatos
st.sidebar.title("Contato")

st.sidebar.write("[Contacte-me](mailto:guidarianiapps@gmail.com)")
st.sidebar.write("[GitHub pessoal](https://github.com/guidariani)")
st.sidebar.write("[GitHub acadêmico](https://github.com/guilhermeilum)")
st.sidebar.write("[GitHub deste site](https://github.com/guidarianiapps)")
st.sidebar.write("[Lattes](http://lattes.cnpq.br/4388577854566943)")

st.sidebar.write("Autor: Guilherme Gurian Dariani")



st.title("Raman, FTIR e UV-Vis")
st.write("### Coloque os arquivos renomeados com o nome da legenda de cada arquivo!!")
coluna_dados = st.columns(2)
with coluna_dados[0]:
    uploaded_files = st.file_uploader(
        "Coloque os dados txt aqui", accept_multiple_files=True
    )
with coluna_dados[1]:
    cabecalho = st.number_input(
        "Coloque a quantidade de linhas do cabeçalho que deseja ignorar.", value=0
    )
    delimitador = st.text_input("Escreva o delimitador.", value="\t")
    st.write(
        "O delimitador deve ser escrito como delimitador da biblioteca pandas, por padrão separa por espaço."
    )
    separador_decimal = st.text_input("Escreva o separador decimal", value=".")
    if delimitador == "":
        delimitador = "\t"
if uploaded_files == []:  ## Esperar algum arquivo
    st.stop()
else:
    lista_dados = []
    for numero in range(len(uploaded_files)):
        df = pd.read_csv(
            uploaded_files[numero],
            names=["x", "y"],
            sep=delimitador,
            skiprows=cabecalho,
            decimal=separador_decimal,
        )
        lista_dados.append(df)

colunas = st.columns(len(uploaded_files))
for index_col in range(len(uploaded_files)):
    with colunas[index_col]:
        arquivo = uploaded_files[index_col].name[:-4]
        st.write("#### ", arquivo)
        st.write(lista_dados[index_col].head(5))
st.write("## Plot dos dados puros.")

fig_normal = plot_dados(uploaded_files, lista_dados)
st.plotly_chart(fig_normal, use_container_width=True)
st.write("## Plot dos dados trabalhados")
st.write(
    "Agora é tirado a linha de base dos dados, utilizando a biblioteca BaselineReamoval, utilizando a função ZhangFit com parâmetros originais, para mais informações [site da biblioteca](https://pypi.org/project/BaselineRemoval/)."
)

x_minimo_original = min([i["x"].values.min() for i in lista_dados])
x_maximo_original = max([i["x"].values.max() for i in lista_dados])
coluna_começo = st.columns(2)
value_escala = st.slider(
    "Selecione o intervalo de x",
    x_minimo_original,
    x_maximo_original,
    (float(x_minimo_original), float(x_maximo_original)),
)
lista_dados = cortar_dados(lista_dados, value_escala[0], value_escala[1])


coluna_opcao = st.columns(2)
with coluna_opcao[0]:
    if st.checkbox("Tirar baseline."):
        lista_dados = baseline_remov(lista_dados)
with coluna_opcao[1]:
    inverter = st.checkbox("Inverter eixo x.")


col1, col2, col3, col4 = st.columns(4)
with col1:
    normalizar = st.checkbox("Normalizar Gráficos")
with col2:
    x_min_norm = st.number_input(
        "Qual é o x mínimo do pico da normalização.", max_value=int(x_maximo_original)
    )
with col3:
    x_max_norm = st.number_input(
        "Qual é o x maximo do pico da normalização.", max_value=int(x_maximo_original)
    )
with col4:
    distancia_linhas = st.number_input(
        "Qual a distancia em y entre as linhas.", min_value=float(0)
    )
juntar_dados = st.button("Juntar dados para salvar.")
coluna_salvar = st.columns(2)
if normalizar:
    lista_nova_dados = []
    for df in lista_dados:
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
    grafico_trabalhado = plot_dados(uploaded_files, lista_nova_dados)
else:
    grafico_trabalhado = plot_dados(uploaded_files, lista_dados)

if juntar_dados:
    df_total = juntar_df(uploaded_files, lista_dados)
    with coluna_salvar[0]:
        st.write(df_total)
    with coluna_salvar[1]:
        st.download_button(
            label="Download data as CSV",
            data=convert_csv(df_total),
            file_name="large_df.csv",
            mime="text/csv",
        )


st.write(
    "Título, se necessário, e legenda dos eixos do gráfico, para unidade é possível escrever HTML, por exemplo, <sup>-1</sup> para $^{-1}$ e <sub>-1</sub> para $_{-1}$, [mais exemplos](https://www.w3schools.com/tags/ref_byfunc.asp) "
)
coluna_leg = st.columns(3)
with coluna_leg[0]:
    titulo = st.text_input("Título do gráfico")
with coluna_leg[1]:
    leg_x = st.text_input("Legenda x", value="Raman Shift (cm<sup>-1</sup>)")
with coluna_leg[2]:
    leg_y = st.text_input("Legenda y", value="Intensity (au)")

local_leg_col = st.columns(2)
with local_leg_col[0]:
    leg_loc_x = st.number_input(
        "Cordenada x da leganda de 0 a 1", min_value=0.0, max_value=1.0
    )
with local_leg_col[1]:
    leg_loc_y = st.number_input(
        "Cordenada y da leganda de 0 a 1", min_value=0.0, max_value=1.0
    )

st.write("Infelizmente algumas vezes é cortada,  a legenda, no último carácter, e não foi encontrado um jeito de correção simples, quando ocorrer o erro renomeie, o arquivo que está com o nome cortado, colocando 2 ou 3 espaços no final do nome do arquivo, obviamente antes da extensão do arquivo, provavelmente solucionará o problema.")
grafico_trabalhado.update_layout(
    title=titulo,
    title_x=0.5,
    xaxis_title=leg_x,
    yaxis_title=leg_y,
    legend=dict(
        x=leg_loc_x,
        y=leg_loc_y,
        traceorder="normal",
        font=dict(
            size=12,
        ),
    ),
)


if inverter:
    grafico_trabalhado.update_xaxes(autorange="reversed")


st.plotly_chart(grafico_trabalhado, use_container_width=True)