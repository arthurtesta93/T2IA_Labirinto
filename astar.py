
# astar.py
# Implementação do algoritmo A* em cima do labirinto (representado como grafo implícito).

from typing import List, Tuple, Dict
import heapq
import math
from maze import Maze

# Mesma codificação de movimentos usada no algoritmo genético.
MOVES = {
    1: (-1, 0),   # cima
    2: (0, 1),    # direita
    3: (1, 0),    # baixo
    4: (0, -1),   # esquerda
    5: (-1, 1),   # cima-direita
    6: (1, 1),    # baixo-direita
    7: (1, -1),   # baixo-esquerda
    8: (-1, -1),  # cima-esquerda
}

def _heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """Heurística admissível: distância Euclidiana."""
    (x1, y1), (x2, y2) = a, b
    return math.hypot(x1 - x2, y1 - y2)

def astar(maze: Maze, start: Tuple[int, int], goal: Tuple[int, int]):
    """Retorna o caminho de start até goal (lista de coordenadas) usando A*.

    Se não houver caminho, retorna None.
    """
    open_heap: List[Tuple[float, Tuple[int, int]]] = []
    heapq.heappush(open_heap, (0.0, start))

    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], float] = {start: 0.0}

    while open_heap:
        current_f, current = heapq.heappop(open_heap)
        if current == goal:
            # reconstrói caminho
            path: List[Tuple[int, int]] = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        if current_f > g_score.get(current, float('inf')) + _heuristic(current, goal):
            # nó desatualizado
            continue

        cr, cc = current
        for dr, dc in MOVES.values():
            nr, nc = cr + dr, cc + dc
            if not maze.is_free(nr, nc):
                continue

            # custo de passo: 1 para ortogonais, sqrt(2) para diagonais
            step_cost = math.sqrt(2.0) if abs(dr) + abs(dc) == 2 else 1.0
            tentative_g = g_score[current] + step_cost

            neighbor = (nr, nc)
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + _heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_score, neighbor))

    return None
