# main.py
# Trabalho T2 - Labirinto com Algoritmo Genético + A*.

import sys
from typing import List, Tuple

from maze import Maze
from genetic import GeneticSolver
from astar import astar


def format_path_with_spaces(path: List[Tuple[int, int]]) -> str:
    """Formata caminho como: (0,0) (0,1) (1,1) ..."""
    return " ".join(f"({r},{c})" for (r, c) in path)


def maze_with_path(maze: Maze, path: List[Tuple[int, int]]):
    """Devolve uma cópia do labirinto marcando o caminho com '*'.

    Mantém o 'E' na origem e o 'S' da saída.
    """
    grid = maze.clone_grid()
    if not path:
        return grid

    # ignora a posição inicial (já marcada com E)
    for (r, c) in path[1:]:
        # não mexe na célula da saída original
        if (r, c) == maze.exit:
            continue
        # só altera células livres
        if grid[r][c] == "0":
            grid[r][c] = "*"

    return grid


def write_output_file(filename: str, maze: Maze, path: List[Tuple[int, int]]):
    """Grava arquivo de saída no formato pedido no enunciado."""
    grid = maze_with_path(maze, path)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{maze.n}\n")
        for row in grid:
            f.write(" ".join(row) + "\n")
        f.write("\n")
        f.write("Caminho: " + format_path_with_spaces(path) + "\n")


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        print("Uso: python main.py <arquivo_labirinto> [modo]")
        print("  modo = rapido (padrão) -> mostra apenas o melhor cromossomo a cada 10 gerações")
        print("  modo = lento           -> mostra todos os cromossomos de cada geração")
        return 1

    lab_file = argv[1]
    mode = argv[2].lower() if len(argv) >= 3 else "rapido"
    detailed = (mode == "lento")

    maze = Maze.from_file(lab_file)
    solver = GeneticSolver(maze)

    # ----------------- ALGORITMO GENÉTICO -----------------
    print("\n=== ALGORITMO GENÉTICO ===\n")

    chrom, ga_path, found_exit = solver.run(detailed=detailed, print_interval=10)

    # Se não encontrou a saída, aborta
    if not found_exit or not ga_path or ga_path[-1] != maze.exit:
        print("\nAlgoritmo Genético não conseguiu encontrar a saída S.")
        return 1

    # Aqui temos certeza que o ÚLTIMO ponto do caminho é a saída S
    print("\nCaminho encontrado pelo Algoritmo Genético (atingiu S):")
    print(format_path_with_spaces(ga_path))
    ga_out = lab_file + "_saida_genetico.txt"
    write_output_file(ga_out, maze, ga_path)
    print(f"Arquivo de saída (genético): {ga_out}")

    # ----------------- ALGORITMO A* -----------------
    print("\n=== ALGORITMO A* ===\n")
    # A saída usada pelo A* é a coordenada final do caminho encontrado pelo GA
    goal = ga_path[-1]
    a_path = astar(maze, maze.start, goal)

    if a_path:
        print("Caminho ótimo encontrado pelo A*:")
        print(format_path_with_spaces(a_path))
        a_out = lab_file + "_saida_aestrela.txt"
        write_output_file(a_out, maze, a_path)
        print(f"Arquivo de saída (A*): {a_out}")
    else:
        print("A* não encontrou caminho até a saída descoberta pelo GA.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())