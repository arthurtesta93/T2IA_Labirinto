
# maze.py
# Representação do labirinto e funções auxiliares de E/S.

from typing import List, Tuple

class Maze:
    def __init__(self, grid: List[List[str]], start: Tuple[int, int], exit_pos: Tuple[int, int]):
        self.grid = grid
        self.n = len(grid)
        self.start = start
        self.exit = exit_pos

    @classmethod
    def from_file(cls, path: str) -> "Maze":
        """Lê um labirinto a partir de um arquivo texto.

        Formato esperado:
        - primeira linha: inteiro n (tamanho da matriz n x n)
        - próximas n linhas: caracteres separados por espaço OU colados
          ('E', 'S', '0', '1').
        """
        with open(path, 'r', encoding='utf-8') as f:
            first = f.readline()
            if not first:
                raise ValueError("Arquivo vazio")
            first = first.strip()
            if not first:
                # permite linha em branco antes do número
                first = f.readline().strip()
            n = int(first)
            grid: List[List[str]] = []
            start = None
            exit_pos = None

            for i in range(n):
                line = f.readline()
                if line is None or line == "":
                    raise ValueError(f"Fim do arquivo antes de ler a linha {i+1} do labirinto")
                line = line.strip()
                if not line:
                    # permite linhas vazias extras
                    i -= 1
                    continue
                tokens = line.split()
                if len(tokens) == 1 and len(tokens[0]) == n:
                    row = list(tokens[0])
                else:
                    row = tokens
                if len(row) != n:
                    raise ValueError(f"Linha {i+1} deveria ter {n} colunas, mas tem {len(row)}: {row}")
                for j, c in enumerate(row):
                    if c == 'E':
                        start = (i, j)
                    elif c == 'S':
                        exit_pos = (i, j)
                grid.append(row)

        if start is None:
            start = (0, 0)
        if exit_pos is None:
            raise ValueError("Saída 'S' não encontrada no labirinto")
        return cls(grid, start, exit_pos)

    def is_inside(self, r: int, c: int) -> bool:
        return 0 <= r < self.n and 0 <= c < self.n

    def is_free(self, r: int, c: int) -> bool:
        """Retorna True se a célula é transitável (0, E ou S)."""
        return self.is_inside(r, c) and self.grid[r][c] != '1'

    def clone_grid(self):
        return [row[:] for row in self.grid]
