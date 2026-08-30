"""

@author: Alexandre Alves, Msc.

"""

from evolve.properties import POPULATION_SIZE
from evolve.individual import RuleIndividual
from logger import logger_term

class Population:

    def __init__(self):
        self._pop = []
        self.max_fitness = 0

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __getitem__(self, key):
        """Permite acessar cada indivíduo da população via índice."""
        if len(self._pop) < 1:
            raise IndexError("População vazia.")
        return self._pop[key]
    
    def initialize_pop(self):
        """Gera população inicial com tamanho POPULATION_SIZE"""
        logger_term.info("Gerando população inicial...")
        for i in range(POPULATION_SIZE):
            ind = RuleIndividual()
            ind._generate_chromossome()
            self._pop.append(ind)

    def evaluate_pop(self, data):
        for i in self._pop:
            i.calculate_fitness(data)

    def set_pop(self, new_pop):
        """Atualiza população"""
        self._pop = new_pop

    def sort_pop(self):
        """
        Ordena de maneira ascendente em relação ao fitness.
        Implementado no método __lt__ da representação do indivíduo.
        """
        self._pop = sorted(self._pop, reverse=True) # Melhor indivíduo no índice 0

    def get_best_of(self):
        """Retorna melhor indivíduo. APENAS APÓS ORDENAÇÃO"""
        if self._pop[0].get_fitness()==0:
            print("População não tem indivíduos com fitness maior que 0. Retornando primeiro indivíduo da lista.")
        return self._pop[0]

    def get_total_fitness(self):
        """DEPRECIADO. Calcular todos os fitness apenas para obter o total pode ser ineficiente."""
        """Retorna soma de todos os valores de fitness. Usado para seleção dos pais."""
        fitness_list = [x.get_fitness() for x in  self._pop]
        return sum(fitness_list)

    def get_mean_fitness(self):
        """Retorna fitness médio da população"""

        fitness_list = [x.get_fitness() for x in  self._pop]
        return sum(fitness_list) / len(fitness_list)
