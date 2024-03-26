# Castorplot

<img src="imagem\CASTORPLOT.png" width="200">

# Introdução

A ideia principal e motivação desse site foi para ajudar principalmente os novos estudantes que terão os mesmos problemas que tivemos, para plotar gráficos retirados dos diversos equipamentos da Ilum.

- Facilitar a criação de gráficos a partir de dados dos equipamentos da Ilum.
- Acelerar o processo de análise e visualização de dados.
- Oferecer uma interface amigável e intuitiva para usuários de todos os níveis.
- Ser um recurso gratuito e de código aberto disponível para todos.

# Índice

- [Avisos](#avisos)
- [Menu de páginas](#menu-de-páginas)
- [Importação](#importação)
  - [Arquivos suportados](#arquivos-suportados)
  - [Parâmetros](#parâmetros)
  - [Tabela](#tabela)
  - [Gráfico exemplo](#gráfico-exemplo)
  - [Arquivo com várias colunas](#arquivo-com-várias-colunas)
  - [Avisos](#avisos-1)
- [Tratamento e layout](#tratamento-e-layout)
  - [Tratamento](#tratamento)
    - [Intervalo de interesse](#intervalo-de-interesse)
    - [Normalização](#normalização)
    - [Baseline](#baseline)
    - [Separar linhas](#separar-linhas)
  - [Layout](#layout)
    - [Título e eixos](#título-e-eixos)
    - [Local legenda](#local-legenda)
    - [Cores e fonte](#cores-e-fonte)
    - [Legenda cortada](#legenda-cortada)
- [Personalização pelo gráfico](#personalização-pelo-gráfico)
- [O gráfico](#o-gráfico)
  - [Salvar imagem](#salvar-imagem)
  - [Zoom](#zoom)
  - [Movimentar](#movimentar)
  - [Auto escala](#auto-escala)
  - [Resetar eixos](#resetar-eixos)
  - [Mostra linhas](#mostra-linhas)



# Avisos

1. O site continua sendo atualizado, portanto, se encontrar algum problema, me avise por e-mail, pessoalmente ou pelo git, que será corrigido o mais rápido possível.
2. Não sou especialista no assunto, portanto, **não me responsabilizo** por nenhuma informação incorreta ou uso indevido do site.
3. Erros ortográficos podem acontecer. Tenho disgrafia e disortografia. Erros desse tipo não significam que o site está errado.
4. ***Não sou especialista em frontend***. Portanto, não espere algo bonito, apenas funcional. O foco do site é a utilidade e a praticidade.

# Menu de páginas

O menu se encontra na barra lateral a esquerda, se não estiver aparecendo é apenas clicar no símbolo > na parte superior esquerda.

# Importação

## Arquivos suportados

- txt
- CSV

## Parâmetros

Linha do cabeçalho, define a linha que será utilizada como cabeçalho, automaticamente se a primeira linha tiver somente números os nomes serão trocados automaticamente. Futuramente poderá ser trocado o nome de cada linha diretamente no site.

Delimitador de coluna: É o que mostra para o código onde é uma coluna e quando é outra, por padrão utiliza \t, pois é como se interpreta o "tab", outros parâmetros como "," e ";" é somente escrever, qualquer dúvida concute a [documentação](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#:~:text=ou%20StringIO.-,sep,-str%2C%20padr%C3%A3o%20%27%2C%27).

Separador decimal: é o parâmetro que será utilizado como separador decimal, é normalmente utilizado como "," ou ".".

## Tabela

A(s) tabela(s) são apenas para mostrar os seus dados, e assim sendo possível identificar rapidamente erros.

## Gráfico exemplo

O gráfico que aparece na tela de importação é apenas o exemplo dos seus dados, por isso não é possível fazer nenhuma alteração no layout.

## Arquivo com várias colunas

Quando o arquivo tem várias colunas a opção selecionar colunas de interesse irá ser habilitada, nela é possível colocar que todas as linhas terão o nome do arquivo, selecionar qual coluna será o x do gráfico, e quais colunas estarão no gráfico, isso é definido após desmarcar a caixa “Todas”. 

Neste modo não é recomendado a utilização mais de um arquivo, podendo ocasionar erro, ainda não foi devidamente arrumado.

## Avisos

Sempre confira que seus dados não possuem letras e/ou palavras, o site não irá ignorar isso e ocorrerá um erro.

# Tratamento e layout

Para mudar de tratamento para layout é apenas clicar na barra de escolha:

![Tratamento e layout](imagem\Tratamento_layout.png)

## Tratamento

### Intervalo de interesse

O intervalo de interesse é onde será visualizado seu espectro, é recomendado delimitar a área de interesse. A limitação é apenas um corte do x mínimo escolhido até o máximo. Não tendo nenhuma outra alteração.

### Normalização

A normalização utiliza a fórmula de min max:

$$
x_{norm} = \frac{x-x_{min}}{x_{max}-x_{min}}
$$

Para encontrar o mínimo e o máximo valor é procurado no intervalo x descrito, para todos os dados analisados.

### Baseline

É tirado a linha de base de todas as colunas y dos dados utilizando a biblioteca BaselineReamoval, com a função ZhangFit com parâmetros originais. Mais informações disponíveis em [site da biblioteca](https://pypi.org/project/BaselineRemoval/).

Sempre na remoção da linha de base ocorrem pequenos erros, para melhorar isso o usuário pode escolher se será removida antes ou após limitar o intervalo. Isso implica qual informação o código iria utilizar para entender a tendência dos dados, para assim ver analisar a baseline.

### Separar linhas

A separação de linha apenas soma o valor no y, isso permite dar um shift nos dados e melhorar a visualização, normalmente utilizado com a normalização dos dados.

![Exemplo de imagem normalizada e com o valor de 0,5 no argumento, separar linhas e sem os números no eixo y. Imagem criada no site.](imagem\plot.png)

Exemplo de imagem normalizada e com o valor de 0,5 no argumento, separar linhas e sem os números no eixo y. Imagem criada no site.

## Layout

### Título e eixos

Quando for mudar o título do gráfico, as legendas dos eixos, para as unidades é recomendado usar o alt Gr, mas se precisar é possível escrever HTML, por exemplo, <sup>-1</sup> para $^{-1}$ e <sub>-1</sub> para $_{-1}$, [mais](https://www.w3schools.com/tags/ref_byfunc.asp)

- Ticks são os traços ao longo do eixo, eles podem ser desativados ou ativados.
- Remover números do eixo y é uma técnica interessante quando o valor y não possuem uma unidade com valor importante. Uma unidade arbitrária.
- Linha nos eixos, é possível remover.
- Inverter eixo x, apenas inverte o eixo colocando decrescente da esquerda para a direita.

### Local legenda

Não achei um jeito fácil para mudar de local a imagem, mas pense que a legenda tem coordenadas e o ponto de x mínimo e y mínimo do gráfico é o ponto 0,0 da legenda… Desculpa a confusão, ainda pensarei em algo.

Se quiser é possível arrumar diretamente no gráfico, na secção “Personalização pelo gráfico”.

### Cores e fonte

A Borda do gráfico pode ser transparente ou com uma cor definida, por padrão é branca.

O fundo também segue a mesma lógica.

O grid, grade, por padrão, vem desativado, mas pode ser ativado e assim escolher sua cor.

Para o texto por padrão a cor é preta e a fonte é Arial, mas isso pode ser alterado.

Por último é possível mudar a cor das linhas do gráfico, primeiro é necessário escolher a linha e depois mudar a cor, é normal que algumas vezes quando for alterar não altere de primeira, assim sendo necessário selecionar a cor novamente. A solução deste erro ainda não foi achada. Isso por se tratar de uma das funções mais recentes.

### Legenda cortada

Às vezes quando as linhas possuem legendas grandes o final da legenda é cortado, por enquanto é recomendado colocar alguns espaços no final do nome da coluna antes de mandar o arquivo. Isso será corrigido rapidamente. Isso é um erro antigo que acredito não ocorrer mais, mas se ocorrer você pode alterar o nome tanto antes de importar quanto na “Personalização pelo gráfico”.

# Personalização pelo gráfico

É possível personalizar o gráfico diretamente nele. Isso inclui mudar legendas, o local delas e até mesmo os nomes dos eixos. Porém, é melhor fazer todas as suas personalizações no final, porque se retornar a essa tela tudo será perdido (por enquanto).

Por se tratar de uma atualização muito nova podem ocorrer erros, se encontrar algum mande no GitHub e se possível com uma captura de tela.

# O gráfico

O gráfico é construído usando a biblioteca [plotly](https://plotly.com/), para assim ser interativo. As ferramentas podem ser encontrada quando o mouse está no gráfico, elas aparecem no canto superior direito.

![Menu do gráfico](imagem\grafico_menu.png)


## Salvar imagem

O primeiro item, uma câmera, é o botão de salvar a imagem, a imagem é salva em png, e salva exatamente como está na tela, portanto se estiver com o zoom ativado irá salvar com o zoom.

## Zoom

O zoom é a ferramenta ativada por padrão, é necessário apenas clicar e segurar com o mouse no gráfico, o retângulo criado será a área a ser visualizada quando soltar o mouse. Clique duplo, desativa o zoom. Outra forma é o + ou o -, mas esses apenas dão zoom centralizado.

## Movimentar

O símbolo com duas setas como uma cruz é o Pan, utilizado para movimentar no gráfico.

## Auto escala

Para centralizar novamente todo o gráfico é possível clicar no autoscale que se encontra do lado da casinha.

## Resetar eixos

Serve basicamente para o mesmo objetivo que o autoscale, ainda não entendi a diferença.

## Mostra linhas

É possível esconder alguma linha clicando no nome dela nas legendas, isso ira deixar ela com um tom mais apagado e a linha do gráfico irá desaparecer. Outra forma é clicar duas vezes rápido em uma linha, que ela irá ser mostrada sozinha, para voltar o normal é apenas clicar duas vezes novamente.

Lembre-se que como a imagem exportada é idêntica a mostrada no site, a legenda da linha escondida apenas ficara apagada.