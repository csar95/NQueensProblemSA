from exceptions import *
from game import *
import time
import numpy as np
import copy
from math import exp


try:
    n = int(input("Write a number greater than 3 to be the board dimension and press (Enter)\n"))
    if n < 4:
        raise LessThanFourError(n)

except ValueError as err:
    exit("The value must be an integer.")
except LessThanFourError as err:
    exit(str(err))


strg = input("Type a solution for the {}-queens problem and press (Enter)\n".format(n))

try:
    initialSolution = np.fromiter(map(int, strg.split(' ')), dtype=int)

    if initialSolution.size != n:
        raise IncorrectInputLengthError(n)

    if np.min(initialSolution) < 0 or np.max(initialSolution) > n:
        raise IncorrectInputError(n)

    if initialSolution.size != np.unique(initialSolution).size:
        raise DuplicateValuesError(n)

except IncorrectInputLengthError as err:
    exit(str(err))
except IncorrectInputError as err:
    exit(str(err))
except DuplicateValuesError as err:
    exit(str(err))
except ValueError as err:
    exit("The characters in the solution must be integers between 0 and {}.".format(n))

# ----------------------------------------------------------------------------------------------------- #

game = Game(initialSolution)
solutions = np.empty(shape=(0, game.n), dtype=int)

beginning, lastFound = time.time(), time.time()
while time.time() - beginning < 46. and time.time() - lastFound < float(game.n * 2):

    # Evaluate the initial state
    currentFitness = game.evaluate_fitness(game.currentSolution)

    # The system has sufficiently cooled
    while game.temperature > 10**-30:

        # Perturb randomly the current state to a new state.
        neighbor = game.select_random_neighbor()

        # Evaluate the new state
        neighborFitness = game.evaluate_fitness(neighbor)

        # goal → quit
        if neighborFitness is 0:
            if not any(np.array_equal(neighbor, solution) for solution in solutions):
                game.currentSolution = copy.deepcopy(neighbor)
                game.print_solution()
                solutions = np.append(solutions, [copy.deepcopy(neighbor)], axis=0)
                lastFound = time.time()
            break
        # ΔE > 0 (new state is better) → accept new state as current state.
        elif currentFitness - neighborFitness > 0:
            game.currentSolution = copy.deepcopy(neighbor)
            currentFitness = neighborFitness
        # else → accept new state with probability
        else:
            prob = exp((currentFitness - neighborFitness) / game.temperature)
            if random.uniform(0, 1) < prob:
                game.currentSolution = copy.deepcopy(neighbor)
                currentFitness = neighborFitness

        # Decrease the temperature
        game.temperature -= game.temperature*0.1

    game.restart_game()

print("Number of solutions found in {} seconds: {}".format(lastFound - beginning, len(solutions)))

# 18 | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
