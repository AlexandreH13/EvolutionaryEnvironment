"""

@author: Alexandre Alves, Msc.

"""

from evolve.rules.rules import Rules
from typing import override
import evolve.properties as properties
from evolve.representations.binary_individual import BinaryIndividual
from logger import logger_test, logger_term


class RuleIndividual(BinaryIndividual):

    def __init__(self):
        super().__init__()

    def __str__(self):
            return f"Cromossomo: {self.get_chromossome()} | Geração: {self.get_generation()} | Fitness: {self.get_fitness()}"

    @override
    def calculate_fitness(self, dados):
        """Calcula o fitness de cada indivíduo. Percorre todos os dados do batch verificando
        se a regra classifica para o classe que está sendo executada.

        Fitness: Média entre sensibilidade e especificidade.
                 (sensibilidade + especificidade)/2
        """

        X = dados[0]
        y = dados[1]

        logger_test.info(f"y: {y}")

        classe = properties.CLASS_NAME

        logger_test.info(f"nome da classe: {properties.CLASS_NAME}")

        vp = 0
        fp = 0
        vn = 0
        fn = 0
    
        for data, real in zip(X, y):
            logger_term.debug("============================ Dado: %s ============================", data)
            classify = Rules.map_cromosome_to_rule(
                self.get_chromossome(), 
                data)
            
            # A regra classificou o registro como pertencente
            # à classe que está sendo evoluída?
            predicted_positive = bool(classify)

            # O registro realmente pertence à classe?
            real_positive = (real == classe)

            if predicted_positive and real_positive:
                vp += 1

            elif predicted_positive and not real_positive:
                fp += 1

            elif not predicted_positive and not real_positive:
                vn += 1

            elif not predicted_positive and real_positive:
                fn += 1

        sensibilidade = (
            vp / (vp+fn)
            if (vp+fn) > 0
            else 0
        )

        especificidade = (
            vn / (vn+fp)
            if (vn+fp) > 0
            else 0
        )

        logger_test.info(f"Sensibiidade: {sensibilidade}")
        logger_test.info(f"Espacificidade: {especificidade}")

        fitness = (sensibilidade + especificidade)/2
        self.set_fitness(fitness)

        logger_test.info(f"Fitness: {fitness}")

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