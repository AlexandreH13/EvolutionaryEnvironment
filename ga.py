"""

@author: Alexandre Alves, Msc.

"""

import random
from population import Population
from individual import Individual
from properties import GENERATIONS, MUTATION_RATE, POPULATION_SIZE

class GeneticAlgorithm:

    def __init__(self):
        self.best_of = None
        self.population = []
        self._best_execution = None # Melhor da execução

    def roulete_selection(self, sum_fitness):
        """Seleção dos pais com método da roleta."""
        father = -1
        sorted_value = random.random()*sum_fitness
        sum = 0
        i = 0

        while i < POPULATION_SIZE and sum < sorted_value:
            sum += self.population[i].get_fitness()
            father += 1
            i += 1
        return father
    
    def set_best_execution(self, best_of):
        """Atualiza o melhor indivíduo."""
        self._best_execution = best_of

    def evolve(self, data):

        # Initial pop
        self.population = Population()
        self.population.initialize_pop()

        # Evaluate population
        self.population.evaluate_pop(data)

        # Ordena pop reverse=True
        self.population.sort_pop()

        # Melhor indivíduo da população atual
        self.best_of = self.population.get_best_of()
        self.set_best_execution(self.best_of)

        print(f"MELHOR DA GERAÇÃO: {self.best_of}")

        for geracao in range(GENERATIONS):
            population_total_fitness = self.population.get_total_fitness()

            next_generation_pop = []

            # De dois em dois pois vamos gerar 2 filhos e no fim das iterações teremos um número de filhos igual ao total da população
            for new_individuals in range(0, POPULATION_SIZE, 2):
                father1 = self.roulete_selection(population_total_fitness)
                father2 = self.roulete_selection(population_total_fitness)

                '''
                ATENÇÃO: nas primeiras gerações são pouquíssimos indivíduos com bom fitness. a seleção dos pais vai considerar indivíduos muito parecidos.
                '''
                childs = self.population[father1].one_slice_crossover(self.population[father2]) # Cromossomo dos filhos
                
                # Criação dos filhos
                child1 = Individual()
                child1.set_chromossome(childs[0])
                child2 = Individual()
                child2.set_chromossome(childs[1])

                # Mutação dos filhos
                child1.bitflip_mutation(MUTATION_RATE)
                child2.bitflip_mutation(MUTATION_RATE)

                # Atualiza geração dos filhos
                child1.set_generation(geracao+1)
                child2.set_generation(geracao+1)

                next_generation_pop.append(child1)
                next_generation_pop.append(child2)

            # Reinserção. Apenas filhos
            self.population.set_pop(next_generation_pop)

            # Avalia nova populaçã
            self.population.evaluate_pop(data)

            # Ordena pop reverse=True
            self.population.sort_pop()

            # Melhor indivíduo da população atual
            self.best_of = self.population.get_best_of()
            # Se melhor da população atual for melhor que melhor da execução
            if self.best_of > self._best_execution:
                self.set_best_execution(self.best_of)

            print(f"MELHOR DA GERAÇÃO: {self.best_of}")