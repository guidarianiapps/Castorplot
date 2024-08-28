import streamlit as st
import funcao
import copy

funcao.config_page()

st.sidebar.image(r"imagem/CASTORPLOT.png")
st.sidebar.header("Menu de páginas:")
if st.sidebar.button("**Página inicial** :house:"):
    st.switch_page("castorplot.py")
if st.sidebar.button("**Importação** :open_file_folder:"):
    st.switch_page(r"pages/import.py")


if "figura" not in st.session_state:
    st.session_state["figura"] = 0

try:
    dicionario_pandas = copy.deepcopy(st.session_state["dicionario_pandas"])
except:
    st.switch_page("castorplot.py")

st.title("Tratamento e layout")
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
                    funcao.normaliza(
                        dicionario_pandas,
                        x_min_escolido,
                        x_max_escolido,
                    )
        with st.expander("Separar linhas"):
            st.write(
                "A separação de linha apenas soma o valor no y, isso serve para dar um shift nos dados e melhorar a visualização, normalmente utilizado junto com a normalização dos dados."
            )
            separar = st.number_input("Valor de separação", min_value=0.00, step=0.01)
            if separar != 0:
                funcao.separar(
                    dicionario_pandas, separar, st.session_state["colunas_y"]
                )

plot_final = funcao.criar_grafico_plotly(
    dicionario_pandas,
    st.session_state["coluna_x"],
    st.session_state["colunas_y"],
    st.session_state["usar_nome_arquivo"],
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
                leg_x = st.text_input("Legenda eixo x")

            with coluna_leg_eixos[1]:
                leg_y = st.text_input("Legenda eixo y")

            coluna_opções_eixos = st.columns(2)
            with coluna_opções_eixos[0]:
                ticks_x = st.checkbox("Ticks x", value=True)
                ticks_y = st.checkbox("Ticks y", value=True)
                linha_eixos = st.checkbox("Linha nos eixos", value=True)
                n_fonte_eixos = st.number_input(
                    "Qual o tamanho da fonte dos eixos?",
                    value=14,
                    help="Escolha o tamanho da fonte dos eixos, isso irá mudar o tamanho do eixo x e y.",
                )
                n_font_titulo = st.number_input(
                    "Qual o tamanho da fonte do titulo?",
                    value=12,
                    help="Escolha o tamanho da fonte do titulo, isso irá mudar o tamanho do titulo.",
                    disabled=(titulo=="")
                )
            with coluna_opções_eixos[1]:
                tirar_y = st.checkbox("Remover números do eixo y")
                inverter_eixo_x = st.checkbox("Inverter eixo x")
                n_fonte_numeros = st.number_input(
                    "Qual o tamanho da fonte dos numeros nos eixos?",
                    value=12,
                    help="Escolha o tamanho da fonte dos eixos, isso irá mudar o tamanho do numeros nos eixo x e y.",
                )

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
                if st.checkbox("Sem grid", value=True):
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
                    "Escolha a cor para a grade", value="#000000", disabled=not grade
                )
            with coluna_final[0]:
                txcolor = st.color_picker(
                    "Escolha a cor para o texto e linhas", value="#000000"
                )
            with coluna_final[1]:
                fonte = st.text_input("Qual fonte?", value="Arial")

            st.subheader("Mudar cor das linhas")
            coluna_cor_linha = st.columns(2)
            with coluna_cor_linha[0]:
                linha_cor = st.selectbox("Linha", st.session_state["names"].keys())
            with coluna_cor_linha[1]:
                color = st.color_picker(
                    "Selecione a cor da linha.",
                    help="A cor não está sincronizada.",
                    value=st.session_state["color"][linha_cor],
                )
                st.session_state["color"][linha_cor] = color
                for name, cor in st.session_state["color"].items():
                    plot_final.fig.update_traces(
                        line=dict(color=cor), selector=({"name": name})
                    )

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


if ticks_x:
    plot_final.fig.update_layout(
        xaxis=dict(ticks="inside", tickfont=dict(color=txcolor), tickcolor=txcolor),
    )

if ticks_y:
    plot_final.fig.update_layout(
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

plot_final.fig.update_layout(
    title={"font": {"size": n_font_titulo}},  # Tamanho da fonte do título
    xaxis={
        "title": {"font": {"size": n_fonte_eixos}},
        "tickfont": {"size": n_fonte_numeros},
    },  # Tamanho da fonte do título do eixo X e dos números do eixo X
    yaxis={
        "title": {"font": {"size": n_fonte_eixos}},
        "tickfont": {"size": n_fonte_numeros},
    },  # Tamanho da fonte do título do eixo Y e dos números do eixo Y
)


if inverter_eixo_x:
    plot_final.fig.update_xaxes(autorange="reversed")


plot_final.fig.update_xaxes(zeroline=False, showgrid=grade, gridcolor=grcolor)
plot_final.fig.update_yaxes(zeroline=False, showgrid=grade, gridcolor=grcolor)

if linha_eixos:
    plot_final.fig.update_xaxes(showline=True, linewidth=2, linecolor=txcolor)
    plot_final.fig.update_yaxes(showline=True, linewidth=2, linecolor=txcolor)


with st.expander("Personalização pelo gráfico"):
    st.write(
        """Agora você pode personalizar o seu gráfico diretamente! Isso inclui mudar legendas, o local delas e até mesmo os nomes dos eixos. Porém, é melhor fazer todas as suas personalizações no final, porque se retornar a essa tela tudo será perdido (por enquanto). Se encontrar algum problema, por favor, avise!"""
    )
    if st.button("Personalização :chart_with_upwards_trend:"):
        st.switch_page(r"pages/personalizacao.py")

config = {
    "toImageButtonOptions": {
        "format": "png",  # one of png, svg, jpeg, webp
        "filename": "Plot_castorplot",
        "scale": 6,  # Multiply title/legend/axis/canvas sizes by this factor
    }
}

st.session_state["figura"] = plot_final

st.plotly_chart(plot_final.fig, use_container_width=True, config=config)

with st.expander("Doação"):
    doacao_colunas = st.columns(2)
    with doacao_colunas[0]:
        st.write("O QR-code é:")
        st.image("imagem//pix.png", width=300)
    with doacao_colunas[1]:
        st.write("A chave é o email guidarianiapps@gmail.com")
