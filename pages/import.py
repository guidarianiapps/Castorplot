import streamlit as st
import funcao
from matplotlib import pyplot as plt
import matplotlib

cmap = plt.get_cmap("cool")


funcao.config_page()

st.sidebar.image(r"imagem/CASTORPLOT.png")
st.sidebar.header("Menu de páginas:")
if st.sidebar.button("**Página inicial** :house:"):
    st.switch_page("castorplot.py")

### Passar dados para as outras paginas
if "usar_nome_arquivo" not in st.session_state:
    st.session_state["usar_nome_arquivo"] = 0
if "coluna_x" not in st.session_state:
    st.session_state["coluna_x"] = 0
if "colunas_y" not in st.session_state:
    st.session_state["colunas_y"] = 0

st.title("Importação")
colunas_import = st.columns([2, 3])
with colunas_import[0]:
    uploaded_file = st.file_uploader(
        "Envie os arquivos que deseja utilizar.",
        accept_multiple_files=True,
        type=[".csv", ".txt"],
        key="import",
    )

    if uploaded_file == []:
        st.warning("Envie um arquivo antes de continuar")
        st.stop()
    ignor_cabecalho = st.number_input(
        "Linha do cabeçalho?",
        value=0,
        min_value=0,
        help="Linha do cabeçalho, define a linha que será utilizada como cabeçalho, automaticamente se a primeira linha tiver somente números os nomes serão trocados automaticamente. Futuramente poderá ser trocado o nome de cada linha diretamente no site.",
    )

    delimitador = st.text_input(
        "Qual é o delimitador de coluna?",
        value="\\t",
        help="""Delimitador de coluna: É o delimitador  de coluna, por padrão utiliza \\t, pois é como se interpreta o "tab", outros parâmetros como "," e ";" é somente escrever, qualquer dúvida concute a [documentação](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#:~:text=ou%20StringIO.-,sep,-str%2C%20padr%C3%A3o%20%27%2C%27).""",
    )

    separador = st.text_input(
        "Qual é o separador decimal?",
        value=".",
        help="""                 
                 3) Separador decimal: é o parâmetro que será utilizado como separador decimal, é normalmente utilizado como "," ou ".".
                 """,
    )

# erros por falta de informação
if separador == "" or delimitador == "":
    if delimitador == "":
        st.warning("Escreva um delimitador de coluna.")
    if separador == "":
        st.warning("Escreva um separador decimal.")
    st.stop()

dicionario_pandas = funcao.importar(
    uploaded_file, ignor_cabecalho, delimitador, separador
)  # criação do dicionario pandas


chaves = dicionario_pandas.keys()  # nome de todos os arquivos que foram importados
# Mudar nome das colunas
colocar_botao = False
for key in chaves:
    if not (
        all(dicionario_pandas[key].dtypes != "object")
    ):

        st.warning(
            "Os dados não estão com o delimitador correto, o cabeçalho é em outra linha, o separador decimal está errado ou possue algum dado não numérico."
        )
        with colunas_import[1]:
            st.write(dicionario_pandas[key])
        st.stop()

    colunas = dicionario_pandas[key].columns
    mudar_nome = False
    for palavra in colunas:
        try:
            mudar_nome = palavra.replace(separador, ".").isdigit()
        except:
            mudar_nome = isinstance(palavra, int)
        if mudar_nome:  # muda se não tiver nome
            dicionario_pandas[key].columns = [f"x_{key}"] + [
                f"y_{key}_{i}" for i in range(len(colunas) - 1)
            ]
            break
colunas_primeiro_dataset = list(dicionario_pandas[list(chaves)[0]].columns)
if len(colunas_primeiro_dataset) > 2:

    with colunas_import[0]:
        with st.expander("Selecionar colunas de interesse."):
            coluna_interesse = st.columns(2)
            colunas_interesse = colunas_primeiro_dataset
            with coluna_interesse[0]:
                usar_nome_arquivo = st.checkbox("Usar nome do arquivo.")
                coluna_x = st.selectbox("Selecione a coluna X.", colunas_interesse)
                colunas_sem_X = colunas_interesse.copy()
                colunas_sem_X.remove(coluna_x)  # type: ignore
            with coluna_interesse[1]:
                botao_todas_colunas = st.checkbox("Todas", value=True)
                colunas_y = st.multiselect(
                    "Selecione as colunas de interesse.",
                    colunas_sem_X,
                    disabled=botao_todas_colunas,
                )
    if botao_todas_colunas:
        colunas_y = colunas_sem_X
else:
    coluna_x = colunas_primeiro_dataset[0]
    colunas_y = [colunas_primeiro_dataset[1]]
    usar_nome_arquivo = False


with colunas_import[1]:
    colunas_tabelas = st.columns(
        len(dicionario_pandas)
    )  # cria as colunas para as tabelas

    for index, key in zip(
        range(len(dicionario_pandas)), chaves
    ):  # mostra as tabelas importadas
        with colunas_tabelas[index]:
            st.write(dicionario_pandas[key].head(5))

    plot_teste = funcao.criar_grafico_plotly(
        dicionario_pandas, coluna_x, colunas_y, usar_nome_arquivo
    )
    plot_teste.grafico()
    st.plotly_chart(plot_teste.fig, use_container_width=True)

if st.sidebar.button("**Tratamento e layout** :wrench:"):
    st.switch_page("pages/tratamento.py")

norm = plt.Normalize(0, len(plot_teste.names))
if "color" not in st.session_state:
    st.session_state["color"] = {}

for num, name in enumerate(plot_teste.names):
    st.session_state["color"][name] = matplotlib.colors.to_hex(cmap(norm(num)))

### Passar dados para as outras paginas

st.session_state["dicionario_pandas"] = dicionario_pandas

st.session_state["usar_nome_arquivo"] = usar_nome_arquivo

st.session_state["coluna_x"] = coluna_x

st.session_state["colunas_y"] = colunas_y

st.session_state["names"] = plot_teste.names


with st.expander("Doação"):
    doacao_colunas = st.columns(2)
    with doacao_colunas[0]:
        st.write("O QR-code é:")
        st.image("imagem//pix.png", width=300)
    with doacao_colunas[1]:
        st.write("A chave é o email guidarianiapps@gmail.com")
