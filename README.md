# Desafio ENACOM de otimização e Python


Este projeto é uma aplicação de otimização de investimentos que usa programação linear e algoritmo genético para encontrar o melhor conjunto de investimentos baseado no capital disponível, limite de custo e mínimo por categoria. Esta aplicação é implementada em Python e usa a biblioteca tkinter para a interface gráfica do usuário.
Requisitos

    Python 3.x
    Bibliotecas Python: pandas, tkinter, pulp, numpy, matplotlib, deap


## Instruções de Instalação

Clone este repositório ou faça o download do código-fonte.
Certifique-se de que o Python esteja instalado no seu sistema.
Instale as bibliotecas necessárias. Se você estiver usando pip, você pode fazer isso executando

    pip install pandas tkinter pulp numpy matplotlib deap.

## Como usar

Execute o arquivo python 

    optimization_gui.py

A aplicação será iniciada e você verá a interface gráfica do usuário.

![Alt text](/images/image-5.png)

Selecione os dados que você deseja usar na otimização. Por padrão, você pode escolher entre "data.csv" e "fake_data.csv"

Chamamos de "problema padrão", a seguinte instância (Esta é a instância salva em data.csv.):

![Alt text](/images/enacom.png)

Digite o capital disponível, limite de custo e mínimo por categoria.
Escolha o tipo de solver que deseja usar: Programação Linear (Determinístico, Ótimo) ou Algoritmo Genético (Estocástico).
Clique no botão "Resolver" para iniciar a otimização. A solução será salva em um arquivo CSV.
Você pode visualizar a solução clicando no botão "Visualizar Solução".
Se você deseja gerar e usar dados falsos, insira o número de pontos de dados falsos e clique em "Gerar Dados Falsos".
A aplicação também suporta múltiplas soluções. Para habilitar isso, marque a opção 'Múltiplas soluções' e digite o número de soluções desejadas.

Também é possível executar o a solução de Programação Linear ou o algoritmo genético separadamente, basta executar os arquivos *otimizacao_investimentos_prog_linear.py* ou *programacao_investimentos_algo_genetico.py*, respectivamente.

## Funcionalidades

**Carregar Dados:** Permite que o usuário carregue os dados a serem usados na otimização.

**Gerar Dados Falsos:** Gera um conjunto de dados falsos com base no número de pontos de dados falsos fornecidos pelo usuário.

**Resolver:** Inicia a otimização com base nos parâmetros fornecidos pelo usuário.

**Visualizar Solução:** Mostra a solução da otimização em uma tabela.

**Múltiplas Soluções:** Fornece a opção de obter múltiplas soluções para o problema de otimização.

## Resultados (problema padrão)

- Investimento 1  - Custo: 470.000, Retorno: 410000, Risco: Baixo
- Investimento 2  - Custo: 400.000, Retorno: 330000, Risco: Baixo
- Investimento 4  - Custo: 270.000, Retorno: 250000, Risco: Médio
- Investimento 5  - Custo: 340.000, Retorno: 320000, Risco: Médio
- Investimento 6  - Custo: 230.000, Retorno: 320000, Risco: Médio
- Investimento 7  - Custo: 50.000, Retorno: 90000, Risco: Médio
- Investimento 9  - Custo: 320.000, Retorno: 120000, Risco: Alto
- Investimento 13  - Custo: 300.000, Retorno: 380000, Risco: Médio

Investimentos por categoria de risco:
Baixo: [1, 2]
Médio: [4, 5, 6, 7, 13]
Alto: [9]

- Total ROI = 2.220.000
- Total Gasto = 2.380.000
- Disponível  - Gasto = 20.000
- Status: Solução Ótima

Variando capital disponível:

![Alt text](/images/image.png)

## Outras Análises

### Maximizar ROI e maximizar efficiência

![Alt text](/images/image-1.png)

### Maximizar ROI e minimizar risco

![Alt text](/images/image-2.png)

### Maximizar ROI e minimizar gastos

![Alt text](/images/image-3.png)

Pontos vermelhos (menos dinheiro gasto para o mesmo ROI):

![Alt text](/images/image-4.png)

## Testes Unitários

- Verifica se o problema de otimização foi definido corretamente.
- Confere se a resolução do problema de otimização retorna um estado ótimo.
- Testa se o retorno dos resultados está correto e assegura que as variáveis estejam dentro dos limites pré-definidos.
- Verifica se a classe retorna um erro quando o arquivo de entrada não é válido.
- Confere se a classe retorna um erro quando o arquivo de entrada não existe.
- Testa se a classe retorna um erro quando o arquivo de dados está vazio.
- Verifica se a classe retorna um erro quando o capital disponível é inválido.
- Confere se a classe retorna um erro quando o capital disponível é zero.
- Verifica se a classe retorna um erro quando o mínimo por categoria é inviável.
- Confere se a classe retorna um erro quando os limites de custo são inviáveis.

