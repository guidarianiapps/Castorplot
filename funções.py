from bokeh.models import ColumnDataSource
from bokeh.palettes import Turbo256
from bokeh.plotting import figure
import numpy as np
import streamlit as st

def criar_grafico(dado_pandas):
    """
    Cria a figrua do grafico em bokeh utilizando os dados pandas.
    arg:
        dado_pandas: dados em tabela pandas
    return:
        figura: imagem gerada com bokeh.
    """
    
    colunas = list(dado_pandas.columns)
    n_colunas=len(dado_pandas.columns)-1
    index_cor = np.linspace(0,len(Turbo256),n_colunas)
    
    st.write([ i for i in list(index_cor)])
    
    mypalette= [Turbo256[i] for i in index_cor]
    
    ys = [dado_pandas[name].values for name in colunas[1:]]
    xs=[dado_pandas[colunas[0]].values]*n_colunas
    legenda_lista = colunas[1:]
    
    p = figure(width=500, height=300) 
    for (colr, leg, x, y ) in zip(mypalette, legenda_lista, xs, ys):
        p.line(x, y, color= colr, legend_label= leg)
    

    

    return p
