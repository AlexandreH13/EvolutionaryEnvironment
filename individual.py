"""

@author: Alexandre Alves, Msc.

"""

from typing import override
from representations.binary_individual import BinaryIndividual

class Individual(BinaryIndividual):
    """
    Sua implementação vem aqui. Escolha a representação desejada do indivíduo e realize a herança.
    Implemente o cálculo do fitness.
    """

    def __init__(self):
        super().__init__()
        self._total_weight = 0

    def __str__(self):
        return f"Cromossomo: {self.get_chromossome()} | Geração: {self.get_generation()} | Fitness: {self.get_fitness()} | Peso total: {self._total_weight}"

    @override
    def calculate_fitness(self, itens):
        constraint = 20 # MAX CAPACITY
        value = 0
        weight = 0

        for i in range(len(itens)-1):
            if self.get_chromossome()[i]==1:
                weight += itens[i][0]
                value += itens[i][1]

        self.set_fitness(value)
        self._total_weight = weight
        
        if weight > constraint:
            self.set_fitness(0)
           
        

