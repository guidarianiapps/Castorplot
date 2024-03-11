import streamlit as st

# Dados da pagina
st.set_page_config(
    page_title="CastorPlot",
    page_icon=r"imagem/CASTORPLOT.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


####################################Contatos################
st.sidebar.image(r"imagem/CASTORPLOT.png")

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


# Importa bibliotecas
import streamlit as st

# Define a paleta de cores
primary_color = "#0077b6"
secondary_color = "#95a5a6"

# Título
st.title("Castorplot")

colunas = st.columns(2)

with colunas[0]:
    # Header: Ideia principal
    st.header("Ideia principal")

    # Formata frase principal
    main_text = """
    A ideia principal e motivação desse site foi para ajudar principalmente os novos estudantes que terão os mesmos problemas que tivemos, para plotar gráficos retirados dos diversos equipamentos da Ilum.
    """
    st.markdown(main_text)

    # Lista de benefícios
    benefits = [
        "Facilitar a criação de gráficos a partir de dados dos equipamentos da Ilum.",
        "Acelerar o processo de análise e visualização de dados.",
        "Oferecer uma interface amigável e intuitiva para usuários de todos os níveis.",
        "Ser um recurso gratuito e de código aberto disponível para todos.",
    ]
    for benefit in benefits:
        st.markdown(f"- {benefit}")

    if st.button(":blue[**Importação**] :open_file_folder:"):
        st.switch_page(r"pages\import.py")
with colunas[1]:
    # Header: Avisos
    st.header("Avisos")

    # Aviso 1
    st.warning(
        """
    1) O site continua sendo atualizado, portanto, se encontrar algum problema, me avise por e-mail, pessoalmente ou pelo git, que será corrigido o mais rápido possível.
    """
    )

    # Aviso 2
    st.error(
        """
    2) Não sou especialista no assunto, portanto, **não me responsabilizo** por nenhuma informação incorreta ou uso indevido do site.
    """
    )

    # Aviso 3
    st.info(
        """
    3) Erros ortográficos podem acontecer. Tenho disgrafia e disortografia. Erros desse tipo não significam que o site está errado.
    """
    )

    # Aviso 4
    st.info(
        """
    4) ***Não sou especialista em frontend***. Portanto, não espere algo bonito, apenas funcional. O foco do site é a utilidade e a praticidade.
    """
    )

st.write(
    """Este site gratuito oferece funções que muitos outros cobram para realizá-las.
Também é mantido por uma única pessoa, o que torna o trabalho difícil e demanda muito tempo.
Sua contribuição é muito bem-vinda e ajudará a mantê-lo."""
)
st.write("Por enquanto, só é aceito pix.")
doacao_colunas = st.columns(2)
with doacao_colunas[0]:
    st.write("Se preferir o QR-code é:")
    st.image("imagem//pix.png")
with doacao_colunas[1]:
    st.write("A chave é o email guidarianiapps@gmail.com.")
