"""

@author: Alexandre Alves, Msc.

"""

from abc import ABC, abstractmethod
from properties import INDIVIDUAL_LEN
import random

class BinaryIndividual(ABC):

    def __init__(self):
        self._fitness: int = 0
        self._chromossome: list = []
        self._generation: int = 0
        self._is_mutated = False

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

    def bitflip_mutation(self, rate) -> list:
        """Mutação por troca de bit. Retorna próprio indivíduo mutado."""

        for g in range(len(self.get_chromossome())):
            if random.random() < rate:
                if not self.is_mutated():
                    self._is_mutated = True
                if self.get_chromossome()[g]==0:
                    self._chromossome[g]=1
                else:
                    self._chromossome[g]=0

        return self
    
    
    def one_slice_crossover(self, other):
        """Implementa crossover de 1 ponto de corte."""
        len_indi = len(self.get_chromossome())-1
        slice_idx = random.randint(1, len_indi) # Slice index. Not considering index 0.

        # Current parent slices
        partition_one_curr = self.get_chromossome()[0:slice_idx]
        partition_two_curr  = self.get_chromossome()[slice_idx:]

        # Other parent slices
        partition_one_other = other.get_chromossome()[0:slice_idx]
        partition_two_other  = other.get_chromossome()[slice_idx:]

        child1_chromossome = partition_one_curr + partition_two_other
        child2_chromossome = partition_one_other + partition_two_curr

        return child1_chromossome, child2_chromossome

    def two_slices_crossover(self, other):
        """Implementa o crossover com 2 pontos de corte."""
        len_indi = len(self.get_chromossome())-1
        slice_idx1 = random.randint(1, len_indi-2) # Not considering index 0 and last index to avoid ValueError on slice_idx2
        slice_idx2 = random.randint(slice_idx1+1, len_indi-1)


        # Current parent slices
        partition_one_curr = self.get_chromossome()[0:slice_idx1]
        partition_two_curr = self.get_chromossome()[slice_idx1:slice_idx2]
        partition_three_curr  = self.get_chromossome()[slice_idx2:]

        # Other parent slices
        partition_one_other = other.get_chromossome()[0:slice_idx1]
        partition_two_other = other.get_chromossome()[slice_idx1:slice_idx2]
        partition_three_other  = other.get_chromossome()[slice_idx2:]

        child1_chromossome = partition_one_curr + partition_two_other + partition_three_curr
        child2_chromossome = partition_one_other + partition_two_curr + partition_three_other

        return child1_chromossome, child2_chromossome
