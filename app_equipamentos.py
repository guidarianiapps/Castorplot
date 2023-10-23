import streamlit as st
import funcao


# Dados da pagina
st.set_page_config(page_title="CastorPlot")


####################################Contatos################
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
    "Um site para qualquer pessoa poder utilizar para efetuar um pré-tratamento rápido e plotá-los."
)
with st.expander("Sobre"):
    st.title("Ideia principal")
    st.write(
        "A ideia principal e motivação desse site foi para ajudar principalmente os novos estudantes que terão os mesmos problemas que tivemos, para plotar gráficos retirados dos diversos equipamentos da Ilum. Por exemplo, FTIR, UvVis, florescência, leitor de placas."
    )
    st.title("Avisos")
    st.write(
        """
  1) O site continua sendo atualizado, portanto, não estranhe se algo der errado, me mande um e-mail ou fale pessoalmente o problema, que será corrigido mais rápido possível.
  2) Qualquer erro, me desculpe, não sou especialista no assunto, apenas tento ajudar, portanto, não me responsabilizo por nenhuma informação incorreta ou uso indevido. 
  3) Erro ortográfico, por favor avise ou desconsidere, tenho disgrafia e disortografia, erros desse tipo não significa que está errado o site...
  4) ***Não sou de frontend*** então não espere algo bonito, apenas funcional.
"""
    )
    st.title("Curiosidades")
    st.write(
        "Estava sem ideia para nome e a Professora Juliana me ajudou, o nome vem da segunda estrela mais brilhante da constelação de gêmeos, que é meu signo... "
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
    with st.expander("Parâmetros"):
        st.write("""Os parâmetros são:""")
        st.write(
            """                 
                 1) Linha do cabeçalho, define a linha que será utilizada como cabeçalho, automaticamente se a primeira linha tiver somente números os nomes serão trocados automaticamente. Futuramente poderá ser trocado o nome de cada linha diretamente no site.
                 2) Delimitador de coluna: É o delimitador  de coluna, por padrão utiliza \\t, pois é como se interpreta o "tab", outros parâmetros como "," e ";" é somente escrever, qualquer dúvida concute a [documentação](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#:~:text=ou%20StringIO.-,sep,-str%2C%20padr%C3%A3o%20%27%2C%27).
                 3) Separador decimal: é o parâmetro que será utilizado como separador decimal, é normalmente utilizado como "," ou ".".
                 """
        )
with colunas_import[1]:
    ignor_cabecalho = st.number_input("Linha do cabeçalho?", value=0, min_value=0)

    delimitador = st.text_input("Qual é o delimitador de coluna?", value="\\t")

    separador = st.text_input("Qual é o separador decimal?", value=".")

    # tipo_tabela = st.selectbox(
    #     "Como é o tipo de tabela que irá trabalhar?",
    #     ("Primeira coluna x e uma ou mais y", "Leitor de placas"),
    # )  # Qual tipo de tabela o usuario irá trabalhar.
####### quando tiver pronto.


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
    with st.expander("Selecionar colunas de interesse."):
        coluna_interesse = st.columns(2)
        colunas_interesse = colunas_primeiro_dataset
        with coluna_interesse[0]:
            botao_todas_colunas = st.checkbox("Todas", value=True)
            coluna_x = st.selectbox("Selecione a coluna X.", colunas_interesse)
            colunas_sem_X = colunas_interesse.copy()
            colunas_sem_X.remove(coluna_x)  # type: ignore
        with coluna_interesse[1]:
            usar_nome_arquivo = st.checkbox("Usar nome do arquivo.")
            colunas_y = st.multiselect(
                "Selecione as colunas de interesse.",
                colunas_sem_X,
                disabled=botao_todas_colunas,
            )
    if botao_todas_colunas:
        colunas_y = colunas_sem_X
else:
    coluna_x = None
    colunas_y = None
    usar_nome_arquivo = False


colunas_tabelas = st.columns(len(dicionario_pandas))  # cria as colunas para as tabelas

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
st.title("Tratamento")

tratamento, layout = st.tabs(["Tratamento", "Layout"])

with tratamento:
    esquerda_tratamento, direita_tratamento = st.columns(2)
    with esquerda_tratamento:
        with st.expander("Intervalo de interesse"):
            x_max_interv, x_min_interv = funcao.definir_max_min(dicionario_pandas)
            st.write(
                "O intervalo de interesse é onde será visualizado seu espectro, é recomendado delimitar a área de interesse."
            )
            coluna_esqueda_intervalo, coluna_direita_intervalo = st.columns(2)
            with coluna_esqueda_intervalo:
                intervalo_minimo = st.number_input(
                    "Minímo", x_min_interv, x_max_interv, value=x_min_interv
                )
            with coluna_direita_intervalo:
                intervalo_maximo = st.number_input(
                    "Maxímo", x_min_interv, x_max_interv, value=x_max_interv
                )
        with st.expander("Baseline"):
            st.write(
                """É tirado a linha de base de todas as colunas y dos dados utilizando a biblioteca BaselineReamoval, com a função ZhangFit com parâmetros originais. Mais informações disponíveis em [site da biblioteca](https://pypi.org/project/BaselineRemoval/)."""
            )

            st.write(
                """Sempre na remoção da linha de base ocorre pequenos erros, para melhorar isso o usuário pode escolher se será removida antes ou após limitar o intervalo."""
            )
            coluna_esqueda_baseline, coluna_direita_baseline = st.columns(2)
            with coluna_esqueda_baseline:
                tirar_baseline = st.checkbox("Tirar baseline")
            with coluna_direita_baseline:
                tirar_baseline_antes = st.checkbox(
                    "Tirar antes de limitar", disabled=not tirar_baseline
                )

    if tirar_baseline_antes and tirar_baseline:
        funcao.baseline_remov(dicionario_pandas)
        funcao.limitar(dicionario_pandas, intervalo_minimo, intervalo_maximo)
    elif not tirar_baseline_antes and tirar_baseline:
        funcao.limitar(dicionario_pandas, intervalo_minimo, intervalo_maximo)
        funcao.baseline_remov(dicionario_pandas)
    else:
        funcao.limitar(dicionario_pandas, intervalo_minimo, intervalo_maximo)

    with direita_tratamento:
        with st.expander("Normalização"):
            st.write(
                "A normalização por min max, utilizando somente as informações do intervalo determinado."
            )
            normalizacao_colunas_dentro = st.columns(2)
            x_max, x_min = funcao.definir_max_min(dicionario_pandas)
            with normalizacao_colunas_dentro[1]:
                x_min_escolido = st.number_input("Mínimo", x_min, x_max, value=x_min)
                x_max_escolido = st.number_input("Máximo", x_min, x_max, value=x_max)

            with normalizacao_colunas_dentro[0]:
                normalizar = st.checkbox(
                    "Normalizar",
                    disabled=x_max_escolido <= x_min_escolido,  # type: ignore
                    key="normalizar",
                )
                if x_max_escolido <= x_min_escolido:  # type: ignore
                    st.warning("O valor maxímo precisa ser maior que o minímo.")
                if normalizar:
                    funcao.normaliza(dicionario_pandas, x_min_escolido, x_max_escolido)
        with st.expander("Separar linhas"):
            st.write(
                "A separação de linha apenas soma o valor no y, isso serve para dar um shift nos dados e melhorar a visualização, normalmente utilizado junto com a normalização dos dados."
            )
            separar = st.number_input("Valor de separação", min_value=0.00, step=0.01)
            if separar != 0:
                funcao.separar(dicionario_pandas, separar)

plot_final = funcao.criar_grafico_plotly(
    dicionario_pandas, coluna_x, colunas_y, usar_nome_arquivo
)  # criar classe grafico
plot_final.grafico()


with layout:
    coluna_esquerda_layout, coluna_direita_layout = st.columns(2)
    with coluna_esquerda_layout:
        with st.expander("Título e eixos"):
            st.write(
                "Título e legenda dos eixos do gráfico, para unidade utilize o alt Gr do teclado. "
            )
            st.write(
                "Se precisar é possível escrever HTML por exemplo, <sup>-1</sup> para $^{-1}$ e <sub>-1</sub> para $_{-1}$, [mais exemplos](https://www.w3schools.com/tags/ref_byfunc.asp) "
            )
            titulo = st.text_input("Título do gráfico")
            coluna_leg_eixos = st.columns(2)
            with coluna_leg_eixos[0]:
                leg_x = st.text_input(
                    "Legenda eixo x", value="Raman Shift (cm<sup>-1</sup>)"
                )

            with coluna_leg_eixos[1]:
                leg_y = st.text_input("Legenda eixo y", value="Intensity (au)")

            coluna_opções_eixos = st.columns(2)
            with coluna_opções_eixos[0]:
                ticks = st.checkbox("Ticks", value=True)
                linha_eixos = st.checkbox("Linha nos eixos", value=True)
            with coluna_opções_eixos[1]:
                tirar_y = st.checkbox("Remover números do eixo y")
                inverter_eixo_x = st.checkbox("Inverter eixo x")

        with st.expander("Cores e fonte"):
            coluna_borda = st.columns(2)
            coluna_fundo = st.columns(2)
            coluna_grid = st.columns(2)
            coluna_final = st.columns(2)

            with coluna_borda[0]:
                borda_transp = st.checkbox("Borda transparente")

            with coluna_fundo[0]:
                fundo_transp = st.checkbox("Fundo transparente")

            with coluna_grid[0]:
                if st.checkbox("Sem grid"):
                    grade = False
                else:
                    grade = True

            with coluna_borda[1]:
                borda_bgcolor = st.color_picker(
                    "Escolha a cor da borda", value="#FFFFFF", disabled=borda_transp
                )
            with coluna_fundo[1]:
                bgcolor = st.color_picker(
                    "Escolha a cor do fundo do gráfico",
                    value="#FFFFFF",
                    disabled=fundo_transp,
                )
            with coluna_grid[1]:
                grcolor = st.color_picker(
                    "Escolha a cor para a grade", value="#FFFFFF", disabled=not grade
                )
            with coluna_final[0]:
                txcolor = st.color_picker(
                    "Escolha a cor para o texto e linhas", value="#000000"
                )
            with coluna_final[1]:
                fonte = st.text_input("Qual fonte?", value="Arial")

    with coluna_direita_layout:
        with st.expander("Local legenda"):
            st.write(
                "Não achei um jeito fácil para mudar de local a imagem, mas pense que a legenda tem coordenadas e o ponto de x mínimo e y mínimo do gráfico é o ponto 0,0 da legenda... Desculpa a confusão, vou pensar em algo."
            )
            local_leg_col = st.columns(2)
            with local_leg_col[0]:
                leg_loc_x = st.number_input(
                    "Cordenada x da leganda de 0 a 1",
                    min_value=0.0,
                    max_value=1.0,
                    value=1.0,
                )
            with local_leg_col[1]:
                leg_loc_y = st.number_input(
                    "Cordenada y da leganda de 0 a 1",
                    min_value=0.0,
                    max_value=1.0,
                    value=1.0,
                )
        with st.expander("Legenda cortada"):
            st.write(
                """As vezes quando as linhas possuem legendas grandes o final da legenda é cortado, por enquanto é recomendado colocar alguns espaços no final do nome da coluna antes de mandar o arquivo. Isso será corrigido rapidamente."""
            )  # Mudar

## Em construção
# with st.expander("Mudar legendas"):
#     dicionario_nomes_cor = {nome: ["", "",""] for nome in plot_final.names} #primeiro é o nome de agora, depois a cor, e o nome antigo.
#     for linha in range(1, len(plot_final.names), 2):
#         colunas = st.columns(2)
#         with colunas[0]:
#             colunas_esquerda_legendas = st.columns(2)
#             with colunas_esquerda_legendas[0]:
#                 dicionario_nomes_cor[plot_final.names[linha - 1]][
#                     0
#                 ] = st.text_input(
#                     "teste",
#                     value=plot_final.names[linha - 1],
#                     key=plot_final.names[linha - 1],
#                     label_visibility="collapsed",
#                 )

#             with colunas_esquerda_legendas[1]:
#                 dicionario_nomes_cor[plot_final.names[linha - 1]][
#                     1
#                 ] = st.color_picker(
#                     "teste",
#                     key=f"color_{plot_final.names[linha-1]}",
#                     label_visibility="collapsed",
#                 )

#         with colunas[1]:
#             colunas_direitas_legendas = st.columns(2)
#             with colunas_direitas_legendas[0]:
#                 dicionario_nomes_cor[plot_final.names[linha]][0] = st.text_input(
#                     "teste",
#                     value=plot_final.names[linha],
#                     key=plot_final.names[linha],
#                     label_visibility="collapsed",
#                 )
#             with colunas_direitas_legendas[1]:
#                 dicionario_nomes_cor[plot_final.names[linha]][1] = st.color_picker(
#                     "teste",
#                     key=f"color_{plot_final.names[linha]}",
#                     label_visibility="collapsed",
#                 )

#     if len(plot_final.names) % 2 != 0:
#         colunas_finais_legenda = st.columns(3)
#         with colunas_finais_legenda[0]:
#             dicionario_nomes_cor[plot_final.names[-1]][0] = st.text_input(
#                 "teste",
#                 value=plot_final.names[-1],
#                 key=plot_final.names[-1],
#                 label_visibility="collapsed",
#             )
#         with colunas_finais_legenda[1]:
#             dicionario_nomes_cor[plot_final.names[-1]][1] = st.color_picker(
#                 "",
#                 key=f"color_{plot_final.names[-1]}",
#                 label_visibility="collapsed",
#             )
#         with colunas_finais_legenda[2]:
#             st.button("Aplicar alterações")
#     else:
#         st.button("Aplicar alterações")
# st.write(dicionario_nomes_cor)
## A resolver...

if ticks:
    plot_final.fig.update_layout(
        xaxis=dict(ticks="inside", tickfont=dict(color=txcolor), tickcolor=txcolor),
        yaxis=dict(ticks="inside", tickfont=dict(color=txcolor), tickcolor=txcolor),
    )
else:
    plot_final.fig.update_xaxes(tickfont=dict(color=txcolor))
    plot_final.fig.update_yaxes(tickfont=dict(color=txcolor))


if borda_transp:
    borda_bgcolor = "rgba(0,0,0,0)"

if fundo_transp:
    bgcolor = "rgba(0,0,0,0)"

plot_final.fig.update_layout(
    {
        "paper_bgcolor": borda_bgcolor,
        "plot_bgcolor": bgcolor,
    },
    font=dict(family=fonte),
)

if tirar_y:
    plot_final.fig.update_yaxes(showticklabels=False)
plot_final.fig.update_layout(
    title={
        "text": titulo,
        "x": 0.5,  # Centraliza o título horizontalmente
        "xanchor": "center",  # Ancora o título ao centro
        "font": {"color": txcolor},  # Define a cor do título
    },
    title_font=dict(color=txcolor),
    xaxis_title=leg_x,
    xaxis_title_font=dict(color=txcolor),
    yaxis_title=leg_y,
    yaxis_title_font=dict(color=txcolor),
    font=dict(size=10),
    legend=dict(
        x=leg_loc_x,
        y=leg_loc_y,
    ),
    legend_font=dict(color=txcolor),
)

if inverter_eixo_x:
    plot_final.fig.update_xaxes(autorange="reversed")


plot_final.fig.update_xaxes(zeroline=False, showgrid=grade, gridcolor=grcolor)

plot_final.fig.update_yaxes(zeroline=False, showgrid=grade, gridcolor=grcolor)


if linha_eixos:
    plot_final.fig.update_xaxes(showline=True, linewidth=2, linecolor=txcolor)
    plot_final.fig.update_yaxes(showline=True, linewidth=2, linecolor=txcolor)

config = {
    "toImageButtonOptions": {
        "format": "png",  # one of png, svg, jpeg, webp
        "filename": "Plot_castorplot",
        "scale": 2,  # Multiply title/legend/axis/canvas sizes by this factor
    }
}

st.plotly_chart(plot_final.fig, use_container_width=True, config=config)
