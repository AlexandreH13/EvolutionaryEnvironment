"""

@author: Alexandre Alves, Msc.

"""

from abc import ABC, abstractmethod
from properties import INDIVIDUAL_LEN
import random
from crossover.crossover import Crossover
from mutation.mutation import Mutation

class BinaryIndividual(ABC):

    def __init__(self):
        """
        Inicializações:

        _fitness: valor da avaliação do indivíduo
        _chromossome: lista de bits
        _generation: variável que armazena e atualiza o número da geração
        _is_mutated: armazena booleano para informar se indivíduo sofreu mutação
        _is_crossover: define o método de crossover. recebe a instância passada pelo módulo 'ga'
        """
        self._fitness: int = 0
        self._chromossome: list = []
        self._generation: int = 0
        self._is_mutated = False
        self._crossover = None
        self._mutation = None

    def __str__(self):
        '''
        Define a representação em formato de string do indivíduo,
        apresentando as suas informações mais importantes, como:
            - Cromossomo
            - Fitness
            - Geração
        '''
        
        return f"Chromossome: {self.get_chromossome()} | Fitness: {self.get_fitness()} | Generation: {self.get_generation()}"

    def __repr__(self):
        return f"Tipo : (BinaryIndividual) | Mutado: {self.is_mutated()} "

    def __eq__(self, other):
        """Compara se dois cromossomos são iguais."""

        if not isinstance(self.get_chromossome(), list):
            raise TypeError("Cromossomo não está no formato correto (list)")
        
        if not isinstance(other.get_chromossome(), list):
            raise TypeError("Cromossomo passado na comparação não está no formato correto (list)")
        
        return other.get_chromossome() == self.get_chromossome()

    def __lt__(self, other):
        '''
        Compara os indivíduos em relação ao seu fitness. Usado
        para ordenar a população usando os valores de fitness.
        '''

        if not isinstance(other, BinaryIndividual):
            return NotImplemented
        
        return self.get_fitness() < other.get_fitness()

    def __getitem__(self, key):
        """Permite acessar os genes do indivíduo sem chamar a lista chromossome."""

        if len(self.get_chromossome())<1:
            raise IndexError("O cromossomo do indivíduo não foi definido (lista vazia).")
        
        return self.get_chromossome()[key]

    def __iter__(self):
        """Permite iterar sobre os genes do indivíduo."""

        return iter(self._chromossome)
    
    @abstractmethod
    def calculate_fitness(self) -> float:
        """Método abstrato para calculo do fitness. Deve ser implementado pela subclasse."""
        pass
    
    def _generate_chromossome(self) -> None:
        """Gera aleatoriamente cromossomo com estrutura binária."""
        for i in range(INDIVIDUAL_LEN):
            self._chromossome.append(random.randint(0,1))
    
    def get_chromossome(self) -> list:
        """Retorna a lista que representa o cromossomo."""
        return self._chromossome
    
    def set_chromossome(self, chrom) -> None:
        """Atualiza cromossomo do indivíduo."""

        self._chromossome = chrom

    def set_fitness(self, value) -> None:
        """Atualiza valor de fitness do indivíduo"""
        self._fitness = value

    def get_fitness(self) -> float:
        """Retorna valor de fitness do indivíduo."""
        return self._fitness

    def get_generation(self) -> int:
        """Retorna geração do indivíduo."""

        return self._generation

    def set_generation(self, generation) -> None:
        "Atualiza geração do indivíduo."

        self._generation = generation

    def is_mutated(self):
        return self._is_mutated
    
    def set_crossover(self, method: Crossover):
        """
        Método do indivíduo que define qual crossover usar.
        É definido no indivíduo uma vez que ele é quem invoca o método.
        """
        self._crossover = method
        method.set_father(father=self)

    def set_mutation(self, method: Mutation):
        """
        Método do indivíduo que define qual mutação usar.
        É definido no indivíduo uma vez que ele é quem invoca o método.
        """
        self._mutation = method
        method.set_individual(individual=self)