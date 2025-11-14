# PUCRS – Inteligência Artificial

# T2 – Algoritmos de Busca: labirinto

## Profa. Silvia Moraes

1. **Objetivo**
    Fixar e exercitar conceitos relativos a agentes e a algoritmos de busca. O trabalho consiste
    na simulação de um jogo, no qual o agente deve encontrar a saída de um labirinto.
**2. Ambiente: Labirinto**
    O ambiente consiste em uma matriz n n (Figura1 ). A entrada E será sempre na posição (0,0),
    porém a saída S do labirinto pode ser em qualquer lugar. A entrada é sempre conhecida pelo
    agente, é a sua célula inicial. Já a saída, ele tem que descobrir. Serão fornecidos arquivos
    contendo os labirintos.
3. Movimentação do agente
    O agente pode se mover no ambiente, uma célula de cada vez em qualquer direção:
    ←↑→↓↖↗↘↙. Agentes não caminham sobre paredes e nem as transpassam. As paredes
    estão representadas pelo caracter 1 (um). No arquivo, células vazias (livres) estão
    identificadas por 0 (zero).
**4. Solução**
    O agente deve encontrar a saída por meio de um algoritmo de busca com informação por
    refinamentos sucessivos. Você pode usar Algoritmos Genéticos ou Simulated Annealing para
    encontrar a saída. Faz parte do seu trabalho definir a forma de representação do problema e
    a função heurística de avaliação que permitirão a execução desses algoritmos. O caminho
    definido pelo algoritmo de busca que leva o agente da entrada até a saída pode não ser o
    mais curto. Portanto, ao encontrar a saída, execute um A* para encontrar a melhor rota
    entre a entrada e a saída do labirinto.


O caminho definido pelo algoritmo de busca que leva o agente da entrada até a saída pode não ser o
mais curto. Portanto, após o Algoritmo Genético encontrar a saída, execute um A* para encontrar a
melhor rota entre a entrada e a saída do labirinto. Importante: a saída S deve ser descoberta pelo
algoritmo genético, ela não deve ser usada como conhecimento pré-existente.

**5. Simulação**
A simulação deve exibir informações referentes às iterações do algoritmo genético. De ser capaz de
ler um arquivo texto no formato exibido na Figura 2. O processamento do algoritmo deve ser exibido
na tela. Defina um modo rápido exibindo o melhor cromossomo a cada x gerações e um modo mais
lento com informações mais detalhadas. A Figura 3 tem um exemplo de saída esperada. Se o
algoritmo encontrar a saída, exiba o caminho definido pelo algoritmo genético que leva da entrada à
saida. O caminho encontrado pelo algoritmo genético pode não ser o mais curto. Por isso, uma vez
encontrada a saída, sua simulação deve exibir também o caminho encontrado pelo A* agora com a
saída conhecida. Tanto a saída gerada pelo algoritmo genético quanto pelo A* deve ser apresentada
na tela e salva em um arquivo texto. A Figura 4 apresenta um exemplo de arquivo de saída.


**6. Forma de Avaliação**
1) O trabalho pode ser realizado em grupo (a ser definido).
2) A entrega dos fontes, do executável, dos arquivos de saída e do relatório no moodle
    conforme o cronograma da disciplina. Nesse dia, serão fornecidos novos arquivos (labirintos)
    para testar o código.
3) A nota será distribuída da seguinte forma:
    Pontuação - Critério
    1,0 - Leitura do arquivo de entrada
    2,5 - Implementação do ciclo do Algoritmo Genético
    1,0 - Implementação do A*
    2,5 - Simulação (visualização e arquivos de saída)
    3,0 - Relatório em formato ppt
    A falta de domínio da solução demonstrado durante a apresentação pode gerar desconto
    significativo ou mesmo a perda a nota do trabalho (todos do grupo devem estar presentes)
● Leitura do arquivo de entrada correta seguindo o formato dado como entrada.
● Implementação do ciclo do Algoritmo Genético, incluindo codificação, operadores de
    seleção, cruzamento e mutação. Estabelecer os critérios de parada e definir uma função de
    aptidão adequada. O algoritmo genético não pode usar a posição S (saída), deve procurá-la.
    A definição dos parâmetros (tamanho da população, escolha dos operadores, taxas de


mutação e cruzamento) do algoritmo é uma parte importante do trabalho, assim como a
definição da função de aptidão. A função de aptidão é fundamental para o sucesso desse
algoritmo.
● Implementação do Algoritmo A* : o algoritmo genético encontra o S e passa para o A*: o
labirinto, a célula de entrada E e a de saída S descoberta. Implementar a versão em grafo que
é uma extensão do Dijkstra.
● Simulação deve permitir o acompanhamento visual da execução dos algoritmos e seus
resultados. Entregue um executável e informações de como executá-lo. Permita que seu
programa receba o nome do arquivo (labirinto) como entrada (args). Os arquivos de saída
para os casos de labirinto dados devem ser entregues juntamente com o código e o
executável.
● Relatório no formato ppt: explicando codificação, tamanho da população inicial, funções
heurísticas, operadores escolhidos, taxa de mutação e cruzamento, problemas e
considerações sobre o desenvolvimento do trabalho.
● Os trabalhos não serão aceitos sem apresentação.


