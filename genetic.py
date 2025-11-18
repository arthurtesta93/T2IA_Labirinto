
# genetic.py
# Implementação de um Algoritmo Genético para encontrar a saída do labirinto.

from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple
import random
import math

from maze import Maze

# Codificação dos movimentos (1..8).
# A numeração é arbitrária, mas consistente com o A*.
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
GENE_VALUES = list(MOVES.keys())

DIST_SCORE_CAP = 20.0
DISTANCE_PENALTY = 2.0
COLLISION_SCORE_CAP = 20.0
COLLISION_PENALTY = 4.0
LENGTH_SCORE_CAP = 20.0
LENGTH_PENALTY = 0.5

EXPLORATION_STEP_BONUS = 0.7      # ganho por célula inédita visitada
EXPLORATION_MAX_BONUS = 25.0
STRAIGHT_STEP_BONUS = 0.5         # ganho por manter direção após o primeiro passo
STRAIGHT_MAX_BONUS = 15.0

PROGRESS_STEP_REWARD = 0.6
PROGRESS_MAX_BONUS = 15.0
REVISIT_PENALTY = 0.7
COLLISION_STREAK_PENALTY = 1.5

SUCCESS_BONUS = 40.0
SUCCESS_MULTIPLIER = 1.3
TRIM_BONUS_PER_GENE = 0.8

MAX_FITNESS = 120.0

@dataclass
class IndividualInfo:
    chromosome: List[int]
    path: List[Tuple[int, int]]
    fitness: float
    reached_exit: bool


class GeneticSolver:
    def __init__(
        self,
        maze: Maze,
        population_size: int = 5,
        chromosome_length: int = 20,
        max_generations: int = 200,
        crossover_rate: float = 0.5,
        mutation_rate: float = 0.05,
        tournament_size: int = 3,
        elite_size: int | None = None,
        elite_pool_size: int | None = None,
    ):
        self.maze = maze
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.max_generations = max_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elite_size = elite_size or max(1, population_size // 5)
        if self.elite_size > population_size:
            self.elite_size = population_size
        pool_default = max(self.elite_size * 2, self.elite_size)
        self.elite_pool_size = elite_pool_size or pool_default
        if self.elite_pool_size < self.elite_size:
            self.elite_pool_size = self.elite_size
        if self.elite_pool_size > population_size:
            self.elite_pool_size = population_size

    # ------------- Utilidades básicas do GA -------------

    def _random_chromosome(self) -> List[int]:
        return [random.choice(GENE_VALUES) for _ in range(self.chromosome_length)]

    def _simulate(self, chromosome: List[int]) -> IndividualInfo:
        """Executa o caminho codificado pelo cromossomo e calcula a aptidão."""
        r, c = self.maze.start
        exit_r, exit_c = self.maze.exit
        path = [(r, c)]
        visit_counts = defaultdict(int)
        visit_counts[self.maze.start] = 1

        collisions = 0
        collision_streak = 0
        collision_penalty = 0.0
        reached_exit = False
        visited_cells = {self.maze.start}
        last_direction: Tuple[int, int] | None = None
        straight_bonus = 0.0
        progress_bonus = 0.0
        prev_dist = abs(r - exit_r) + abs(c - exit_c)

        for gene in chromosome:
            dr, dc = MOVES[gene]
            nr, nc = r + dr, c + dc
            if not self.maze.is_free(nr, nc):
                collisions += 1
                # bateu na parede -> fica parado
                collision_streak += 1
                collision_penalty += COLLISION_STREAK_PENALTY * collision_streak
                continue
            collision_streak = 0
            r, c = nr, nc
            visit_counts[(r, c)] += 1
            path.append((r, c))
            visited_cells.add((r, c))
            current_dist = abs(r - exit_r) + abs(c - exit_c)
            if current_dist < prev_dist:
                progress_bonus += PROGRESS_STEP_REWARD * (prev_dist - current_dist)
            prev_dist = current_dist

            current_direction = (dr, dc)
            if current_direction == last_direction:
                straight_bonus += STRAIGHT_STEP_BONUS
            else:
                last_direction = current_direction

            if (r, c) == (exit_r, exit_c):
                reached_exit = True
                break

        # ----------------- NOVO CÁLCULO DA APTIDÃO -----------------
        # distância Manhattan até a saída
        dist_exit = abs(r - exit_r) + abs(c - exit_c)
        path_len = len(path) - 1  # número de passos

        score = 0.0

        # Quanto mais perto da saída, melhor (até 30 pontos)
        score += max(0.0, DIST_SCORE_CAP - DISTANCE_PENALTY * dist_exit)

        # Quanto menos colisões, melhor (até 30 pontos)
        score += max(0.0, COLLISION_SCORE_CAP - COLLISION_PENALTY * collisions)

        # Caminhos muito longos perdem pontos (até 30 pontos)
        score += max(0.0, LENGTH_SCORE_CAP - LENGTH_PENALTY * path_len)

        # Ganho incremental por reduzir distância passo a passo
        score += min(progress_bonus, PROGRESS_MAX_BONUS)

        # Bônus por chegar na saída
        if reached_exit:
            trimmed_genes = max(0, self.chromosome_length - path_len)
            score += SUCCESS_BONUS
            score += trimmed_genes * TRIM_BONUS_PER_GENE

        repeat_penalty = REVISIT_PENALTY * sum(count - 1 for count in visit_counts.values() if count > 1)
        score -= repeat_penalty
        score -= collision_penalty

        # Bônus incremental por explorar novas células e manter direções retas
        exploration_bonus = min(len(visited_cells) * EXPLORATION_STEP_BONUS, EXPLORATION_MAX_BONUS)
        score += exploration_bonus
        score += min(straight_bonus, STRAIGHT_MAX_BONUS)

        if reached_exit:
            score *= SUCCESS_MULTIPLIER

        # Garante que fique dentro dos limites definidos
        if score < 0.0:
            score = 0.0
        elif score > MAX_FITNESS:
            score = MAX_FITNESS

        fitness = score
        # -------------------------------------------------------------------

        return IndividualInfo(
            chromosome=chromosome[:],
            path=path,
            fitness=fitness,
            reached_exit=reached_exit
        )

    def _evaluate_population(self, population: List[List[int]]):
        infos: List[IndividualInfo] = []
        best_idx = 0
        best_fit = -math.inf
        exit_found = False

        for i, chrom in enumerate(population):
            info = self._simulate(chrom)
            infos.append(info)
            if info.fitness > best_fit:
                best_fit = info.fitness
                best_idx = i
            if info.reached_exit:
                exit_found = True

        return infos, best_idx, exit_found

    # def _tournament_select(self, infos: List[IndividualInfo]) -> IndividualInfo:
    #     best = None
    #     for _ in range(self.tournament_size):
    #         cand = random.choice(infos)
    #         if best is None or cand.fitness > best.fitness:
    #             best = cand
    #     return best

    def _next_generation(self, infos: List[IndividualInfo]) -> List[List[int]]: # sem torneio, utiliza elitismo
        elites = sorted(infos, key=lambda inf: inf.fitness, reverse=True)
        new_pop = [elite.chromosome[:] for elite in elites[:self.elite_size]]

        while len(new_pop) < self.population_size:
            p1, p2 = random.sample(elites[:self.elite_pool_size], 2)
            c1, c2 = self._crossover(p1.chromosome, p2.chromosome)
            self._mutate(c1); self._mutate(c2)
            new_pop.append(c1)
            if len(new_pop) < self.population_size:
                new_pop.append(c2)

        return new_pop

    def _crossover(self, p1: List[int], p2: List[int]):
        if random.random() > self.crossover_rate:
            return p1[:], p2[:]
        point = random.randint(1, self.chromosome_length - 1)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
        return c1, c2

    def _mutate(self, chrom: List[int]) -> None:
        for i in range(len(chrom)):
            if random.random() < self.mutation_rate:
                chrom[i] = random.choice(GENE_VALUES)

    # def _next_generation(self, infos: List[IndividualInfo]) -> List[List[int]]:
    #     new_pop: List[List[int]] = []
    #     while len(new_pop) < self.population_size:
    #         p1 = self._tournament_select(infos)
    #         p2 = self._tournament_select(infos)
    #         c1, c2 = self._crossover(p1.chromosome, p2.chromosome)
    #         self._mutate(c1)
    #         self._mutate(c2)
    #         new_pop.append(c1)
    #         if len(new_pop) < self.population_size:
    #             new_pop.append(c2)
    #     return new_pop

    # ------------- Impressão -------------

    @staticmethod
    def _format_path(path: List[Tuple[int, int]]) -> str:
        # Formato semelhante ao exemplo: (0,0)(0,1)(1,1)...
        return ''.join(f"({r},{c})" for (r, c) in path)

    def _print_generation(self, gen: int, infos: List[IndividualInfo], only_best: bool = False):
        print(f"GERACAO: {gen}")
        if only_best:
            # imprime apenas o melhor indivíduo da geração
            best = max(infos, key=lambda inf: inf.fitness)
            idx = infos.index(best)
            chrom_str = ' '.join(str(g) for g in best.chromosome)
            path_str = self._format_path(best.path)
            print(f"(Cromossomo {idx}) {chrom_str} - Caminho: {path_str} - Aptidao: {best.fitness:.1f}")
        else:
            # imprime toda a população (modo lento)
            for idx, info in enumerate(infos):
                chrom_str = ' '.join(str(g) for g in info.chromosome)
                path_str = self._format_path(info.path)
                print(f"(Cromossomo {idx}) {chrom_str} - Caminho: {path_str} - Aptidao: {info.fitness:.1f}")

    # ------------- Execução principal -------------

    def run(self, detailed: bool = False, print_interval: int = 10):
        """
        Executa o Algoritmo Genético ATÉ encontrar a saída S.

        Retorna (melhor_cromossomo, melhor_caminho, True).
        Para labirintos solucionáveis, ele não sai do laço enquanto
        não tiver pelo menos um indivíduo que chega em 'S'.
        """
        attempt = 0

        while True:
            print(f"\n--- Tentativa {attempt+1} do GA ---\n")
            attempt += 1
            
            if attempt > 10:
                print("Número máximo de tentativas atingido. Abortando.")
                return [], [], False
            # nova população aleatória a cada tentativa
            population = [self._random_chromosome() for _ in range(self.population_size)]
            best_overall: IndividualInfo | None = None

            for gen in range(self.max_generations):
                infos, best_idx, exit_found = self._evaluate_population(population)

                gen_best = infos[best_idx]
                if best_overall is None or gen_best.fitness > best_overall.fitness:
                    best_overall = gen_best

                # impressão da geração (como antes)
                if detailed or gen == 0 or gen % print_interval == 0 or exit_found:
                    self._print_generation(gen, infos, only_best=not detailed)

                # *** CRITÉRIO DE SUCESSO: alguém chegou na saída ***
                if exit_found:
                    # pega, dentre os que chegaram em S, o de melhor aptidão
                    best_with_exit = max(
                        (inf for inf in infos if inf.reached_exit),
                        key=lambda x: x.fitness,
                    )
                    # opcional: você pode imprimir em qual tentativa/geração encontrou
                    print('\n------------------------------------------------------------')
                    print(f"Solução encontrada na tentativa {attempt}, geração {gen}")
                    print('------------------------------------------------------------')
                    return best_with_exit.chromosome, best_with_exit.path, True

                # gera próxima geração normalmente
                population = self._next_generation(infos)

            # se chegou aqui, nenhuma solução nesta tentativa -> recomeça
            print(f"Nenhuma saída encontrada na tentativa {attempt}, reiniciando população...")
            # volta para o while True e tenta de novo com outra população