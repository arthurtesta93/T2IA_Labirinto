
Trabalho T2 - Labirinto com Algoritmo Genético + A*

Estrutura dos arquivos
----------------------
- main.py      : ponto de entrada do programa.
- maze.py      : leitura do arquivo de entrada e representação do labirinto.
- genetic.py   : implementação do ciclo do Algoritmo Genético.
- astar.py     : implementação do algoritmo A* em grafo (labirinto como grafo implícito).

Como compilar / executar
------------------------
É necessário ter Python 3 instalado.

Execute no terminal:

    python main.py <arquivo_labirinto> [modo]

onde:
  - <arquivo_labirinto> é um arquivo texto no formato especificado no enunciado
    (primeira linha n, seguido de n linhas com E, S, 0 e 1).
  - [modo] pode ser:
      * rapido (padrão): imprime apenas o melhor cromossomo de cada 10 gerações.
      * lento          : imprime todos os cromossomos de cada geração (como no exemplo).

O programa:
-----------
1) Lê o arquivo de entrada e constrói o labirinto.
2) Executa o Algoritmo Genético para tentar encontrar a saída S.
   - Cada cromossomo é uma sequência de movimentos (1..8) nas 8 direções possíveis.
   - A função de aptidão considera a distância até a saída, colisões com paredes
     e o comprimento do caminho. Um grande bônus é dado quando o caminho chega em S.
   - O programa mostra na tela as gerações, cromossomos, caminhos e valores de aptidão,
     em formato semelhante ao da Figura 3 do enunciado.
   - O melhor caminho do GA é salvo em um arquivo de saída com sufixo
     "_saida_genetico.txt". O labirinto é impresso com o caminho marcado por 'S',
     seguido da linha "Caminho: ..." como na Figura 4.
3) Após o GA, o programa executa o algoritmo A* a partir de E até S,
   encontrando o caminho ótimo entre essas duas células.
   - O caminho do A* também é mostrado na tela e salvo em arquivo texto com sufixo
     "_saida_aestrela.txt", no mesmo formato da saída do GA.

Observação:
-----------
Os parâmetros do algoritmo genético (tamanho da população, comprimento do cromossomo,
número máximo de gerações, taxas de cruzamento e mutação) podem ser ajustados dentro
do arquivo genetic.py, caso seja necessário melhorar o desempenho em labirintos maiores.
