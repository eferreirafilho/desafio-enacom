# Desafio-enacom
Desafio enacom de otimização e Python


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

Selecione os dados que você deseja usar na otimização. Por padrão, você pode escolher entre "data.csv" e "fake_data.csv".
Digite o capital disponível, limite de custo e mínimo por categoria.
Escolha o tipo de solver que deseja usar: Programação Linear (Determinístico, Ótimo) ou Algoritmo Genético (Estocástico).
Clique no botão "Resolver" para iniciar a otimização. A solução será salva em um arquivo CSV.
Você pode visualizar a solução clicando no botão "Visualizar Solução".
Se você deseja gerar e usar dados falsos, insira o número de pontos de dados falsos e clique em "Gerar Dados Falsos".
A aplicação também suporta múltiplas soluções. Para habilitar isso, marque a opção 'Múltiplas soluções' e digite o número de soluções desejadas.

Também é possível executar o a solução de Programação Linear ou o Algoroithm genético separadament, basta executar os arquivos *otimizacao_investimentos_prog_linear.py* ou *programacao_investimentos_algo_genetico.py*, respectivamente.



## Funcionalidades

Carregar Dados: Permite que o usuário carregue os dados a serem usados na otimização.
Gerar Dados Falsos: Gera um conjunto de dados falsos com base no número de pontos de dados falsos fornecidos pelo usuário.
Resolver: Inicia a otimização com base nos parâmetros fornecidos pelo usuário.
Visualizar Solução: Mostra a solução da otimização em uma tabela.
Múltiplas Soluções: Fornece a opção de obter múltiplas soluções para o problema de otimização.

## Resultados (problema padrão)

Investimento 1  - Custo: 470.000, Retorno: 410000, Risco: Baixo
Investimento 2  - Custo: 400.000, Retorno: 330000, Risco: Baixo
Investimento 4  - Custo: 270.000, Retorno: 250000, Risco: Médio
Investimento 5  - Custo: 340.000, Retorno: 320000, Risco: Médio
Investimento 6  - Custo: 230.000, Retorno: 320000, Risco: Médio
Investimento 7  - Custo: 50.000, Retorno: 90000, Risco: Médio
Investimento 9  - Custo: 320.000, Retorno: 120000, Risco: Alto
Investimento 13  - Custo: 300.000, Retorno: 380000, Risco: Médio

Investimentos por categoria de risco:
Baixo: [1, 2]
Médio: [4, 5, 6, 7, 13]
Alto: [9]

Total ROI = 2.220.000
Total Gasto = 2.380.000
Disponível  - Gasto = 20.000
Status: Solução Ótima

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

- Preparação e Finalização: Criação e remoção de um arquivo .csv de teste para manter o ambiente limpo.

- Definição do Problema: Verificação da correta definição do problema.

- Resolução: Confirmação do funcionamento correto do solucionador, verificando se retorna o status ótimo.

- Obtenção de Resultados: Verificação da correta cálculo dos valores esperados.

- Arquivo de Entrada Inválido: Teste do comportamento da classe com arquivos inválidos.

- Arquivo Não Encontrado: Avaliação do tratamento da classe com arquivos inexistentes.

- Arquivo de Dados Vazio: Análise do tratamento da classe com arquivos de dados vazios.

- Capital Disponível Inválido: Verificação da classe ao lidar com capital disponível negativo.

- Problema Inviável: Avaliação de como a classe lida com problemas matematicamente inviáveis.
