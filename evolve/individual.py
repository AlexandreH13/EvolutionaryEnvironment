"""

@author: Alexandre Alves, Msc.

"""

from evolve.rules.rules import Rules
from typing import override
from evolve.representations.binary_individual import BinaryIndividual


class RuleIndividual(BinaryIndividual):

    def __init__(self):
        super().__init__()

    def __str__(self):
            return f"Cromossomo: {self.get_chromossome()} | Geração: {self.get_generation()} | Fitness: {self.get_fitness()}"

    @override
    def calculate_fitness(self, dados):

        X = dados[0]
        y = dados[1]
        print(self.get_chromossome())

        vp = 0
        fp = 0
        acc = 0
        for data in X:
            print(f"============================ Dado: {data} ============================")
            classify = Rules.map_cromosome_to_rule(self.get_chromossome(), data)
            if classify:
                vp+=1
            else:
                fp+=1

        if vp==0:
            print(f"Acurácia (fitness) da regra: {acc}")
            self.set_fitness(0)
        else:
            acc = vp/(vp+fp)
            print(f"Acurácia (fitness) da regra: {acc}")
            self.set_fitness(acc)
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