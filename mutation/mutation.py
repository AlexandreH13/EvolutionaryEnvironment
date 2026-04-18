"""

@author: Alexandre Alves, Msc.

"""

import random
from abc import ABC, abstractmethod

class Mutation(ABC):

    def __init__(self, mutation_rate=0.01):
        self._mutation_rate = mutation_rate
        self._individual = None

    def set_individual(self, individual):
        self._individual = individual
    
    @abstractmethod
    def run(self):
        pass

class BitFlipMutation(Mutation):

    def __init__(self, mutation_rate=0.01):
        super().__init__(mutation_rate)

    def run(self):
        for g in range(len(self._individual.get_chromossome())):
            if random.random() < self._mutation_rate:
                if not self._individual.is_mutated():
                    self._individual._is_mutated = True
                if self._individual.get_chromossome()[g]==0:
                    self._individual._chromossome[g]=1
                else:
                    self._individual._chromossome[g]=0

        return self._individual
