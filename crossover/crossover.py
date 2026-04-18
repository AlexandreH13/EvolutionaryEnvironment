"""

@author: Alexandre Alves, Msc.

"""

import random
from abc import ABC, abstractmethod

class Crossover(ABC):
    """
    Classe abstrata base para a implementação dos métodos de crossover.
    Todas implementações devem ter o mesmo método 'run', conforme definido no método abstrato abaixo.
    """

    def __init__(self):
        self._individual = None

    def set_father(self, father):
        """
        Define quem é o "pai" que está invocando o método para o crossover.
        """
        self._individual = father

    @abstractmethod
    def run(self, other):
        """Deve ser sobrescrito para definir o método de crossover."""
        pass

class OnePoint(Crossover):
    """
    Herda classe Crossover e implementa método run() para realizar crossover de um ponto.
    """

    def __init__(self):
        super().__init__()

    def run(self, other):
        """
        Executa crossover.
        other: outro indivíduo que será usado no crossover.
        """
        len_indi = len(self._individual.get_chromossome())-1
        slice_idx = random.randint(1, len_indi) # Slice index. Not considering index 0.

        # Current parent slices
        partition_one_curr = self._individual.get_chromossome()[0:slice_idx]
        partition_two_curr  = self._individual.get_chromossome()[slice_idx:]

        # Other parent slices
        partition_one_other = other.get_chromossome()[0:slice_idx]
        partition_two_other  = other.get_chromossome()[slice_idx:]

        child1_chromossome = partition_one_curr + partition_two_other
        child2_chromossome = partition_one_other + partition_two_curr

        return child1_chromossome, child2_chromossome
    
class TwoPoint(Crossover):
    """
    Herda classe Crossover e implementa método run() para realizar crossover de dois pontos.
    """

    def __init__(self):
        super().__init__()

    def run(self, other):
        len_indi = len(self._individual.get_chromossome())-1
        slice_idx1 = random.randint(1, len_indi-2) # Not considering index 0 and last index to avoid ValueError on slice_idx2
        slice_idx2 = random.randint(slice_idx1+1, len_indi-1)
        # Current parent slices
        partition_one_curr = self._individual.get_chromossome()[0:slice_idx1]
        partition_two_curr = self._individual.get_chromossome()[slice_idx1:slice_idx2]
        partition_three_curr  = self._individual.get_chromossome()[slice_idx2:]
        # Other parent slices
        partition_one_other = other.get_chromossome()[0:slice_idx1]
        partition_two_other = other.get_chromossome()[slice_idx1:slice_idx2]
        partition_three_other  = other.get_chromossome()[slice_idx2:]
        child1_chromossome = partition_one_curr + partition_two_other + partition_three_curr
        child2_chromossome = partition_one_other + partition_two_curr + partition_three_other
        return child1_chromossome, child2_chromossome

