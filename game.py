import numpy as np
import random
import copy


class Game:

    def __init__(self, solution):
        self.n = solution.size
        self.currentSolution = solution
        self.temperature = self.n / 2

    # Explanation in https://arxiv.org/pdf/1802.02006.pdf
    def evaluate_fitness(self, individual):
        t1 = 0  # Number of repetitive queens in one diagonal while seen from left corner
        t2 = 0  # Number of repetitive queens in one diagonal while seen from right corner

        f1 = np.array([individual[i] - (i + 1) for i in range(self.n)])
        f2 = np.array([(1 + self.n) - individual[i] - (i + 1) for i in range(self.n)])

        f1 = np.sort(f1)
        f2 = np.sort(f2)

        for i in range(1, self.n):
            if f1[i] == f1[i - 1]:
                t1 += 1
            if f2[i] == f2[i - 1]:
                t2 += 1

        return t1 + t2

    def select_random_neighbor(self):
        neighbor = copy.deepcopy(self.currentSolution)
        positions = list(range(self.n))
        random.shuffle(positions)
        pos1 = positions.pop()
        pos2 = positions.pop()
        neighbor[pos1], neighbor[pos2] = self.currentSolution[pos2], self.currentSolution[pos1]
        return neighbor

    def restart_game(self):
        self.currentSolution = np.arange(1, self.n + 1)
        np.random.shuffle(self.currentSolution)
        self.temperature = self.n / 2

    def print_solution(self):
        result = ""
        for col in range(self.n):
            result += (str(self.currentSolution[col]) + ' ')
        print(result)
