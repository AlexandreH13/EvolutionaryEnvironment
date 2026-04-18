"""

@author: Alexandre Alves, Msc.

"""
from properties import MUTATION_RATE
from ga import GeneticAlgorithm
from individual import Individual
from crossover.crossover import OnePoint, TwoPoint
from mutation.mutation import BitFlipMutation

if __name__=="__main__":

    # (peso, valor)
    itens = [
    (2, 10),
    (3, 7),
    (5, 13),
    (7, 17),
    (1, 5),
    (4, 10),
    (6, 14),
    (4, 20),
    (8, 7),
    (7, 12),
    (5, 9),
    (3, 6),
    (2, 8),
    (6, 15),
    (4, 11),
    (5, 14),
    (3, 9),
    (7, 18)
    ]

    runner = GeneticAlgorithm(
        crossover=TwoPoint(),
        mutation=BitFlipMutation(MUTATION_RATE)
        )
    runner.evolve(itens)