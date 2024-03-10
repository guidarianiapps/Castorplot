import streamlit as st

import funcao

funcao.inicial()

config = {
    "toImageButtonOptions": {
        "format": "png",  # one of png, svg, jpeg, webp
        "filename": "Plot_castorplot",
        "scale": 3,  # Multiply title/legend/axis/canvas sizes by this factor
    },
    "edits":{
        "annotationPosition":True,
        "annotationTail":True,
        "annotationText":True,
        "axisTitleText":True,
        "legendPosition":True,
        "legendText":True,
        "shapePosition":True,
        "titleText":True,
    }
}

st.plotly_chart(st.session_state["figura"].fig, use_container_width=True,config=config)
colunas = st.columns(2)

if st.button("Tratamento e layout :wrench:"):
    st.switch_page("pages/tratamento.py")

with st.expander("Doação"):
    doacao_colunas = st.columns(2)
    with doacao_colunas[0]:
        st.write("O QR-code é:")
        st.image("imagem//pix.png", width=300)
    with doacao_colunas[1]:
        st.write("A chave é o email guidarianiapps@gmail.com")