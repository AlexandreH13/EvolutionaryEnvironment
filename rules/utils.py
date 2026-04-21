import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from itertools import compress, cycle, batched
from properties import BINARY_REPRESENTATION_SIZE

def get_decimal(binary_values: list):
    """
    Algoritmo: 
        BIN-NLCEE
    Descrição:
        Representação baseada nos algoritmos CEE e NLCEE. Recebe representação binária e converte para decimal
        para ser utilizado na regra. Função deve ser usada para obter os valores decimais dos segmentos
        peso (W) e valor (V).
    """
    sum=0

    for i in range(len(binary_values)):
        x = binary_values[i]*(2**-(i+1))
        sum+=x

    return sum

def get_min_max(min, max, d):
    """
    Algoritmo: 
        BIN-NLCEE
    Descrição:
        Com o valor decimal do segmento valor (V), calcula normalização com min-max.
    """


    _d = (d - min)/(max-min)

    return _d

def denormalize_min_max(n, min, max):
    """
    'Desnormaliza' valor do min max. Obtém valor original.
    n:
        Valor normalizado.
    min:
        Valor mínimo.
    max:
        Valor máximo.
    """

    _n = n*(max-min)+min
    return _n

def get_string_operator(value: int):
    return ">=" if value==0 else "<"

def get_operator(data: list, binary_size: int):
    """
    Retorna operador de comparação.
    """

    operator_mask = [False] * binary_size + [True] + [False] * binary_size
    operator_list_result = list(compress(data, cycle(operator_mask)))

    string_operator_batches = [get_string_operator(bit) for bit in operator_list_result]

    return string_operator_batches
    

def get_rule_attribute_str(binary_weight: list, binary_value: list, operator: int):
    """
    Retorna uma string com o antecedente da regra de um atributo.
    """
    _d_weight = get_decimal(binary_weight) # Decimal do segmento peso
    _d_value = get_decimal(binary_value) # Decimal do segmento valor
    _s_operator = get_operator(operator) # String do operador

    return f"{_d_weight}{_s_operator}{_d_value}"

def get_decimal_weights(data: list, binary_size: int):
    """
    Cria uma máscara para obter os 'batches' do indivíduo (list) que representam os pesos (W).
    A máscara itera sobre a lista indicando 'True' apenas nos bits que representam o segmento peso.

    binary_size: int
        Número de bits usado para representar os segmentos peso (W) e valor (V).
    """


    # mascara = [True, True, True, True, False, False, False, False, False]
    weight_mask = [True] * binary_size + [False] * (binary_size+1)
    weight_list_result = list(compress(data, cycle(weight_mask)))
    
    batch_iterator = batched(weight_list_result, binary_size)

    #binary_weight_batches = [list(batch) for batch in batch_iterator]
    decimal_weight_batches = [get_decimal(list(batch)) for batch in batch_iterator]

    return decimal_weight_batches

def get_decimal_value(data: list, binary_size: int):

    '''
    Exemplo de máscara onde o número de bits usado na representação é 4:
    mascara = [False, False, False, False, False, True, True, True, True]
    '''
    value_mask = [False] * (binary_size+1) + [True] * binary_size
    value_mask_list_result = list(compress(data, cycle(value_mask)))

    batch_iterator = batched(value_mask_list_result, binary_size)

    decimal_value_batches = [get_decimal(list(batch)) for batch in batch_iterator]

    return decimal_value_batches

def _generate_chromossome(binary_size: int, num_attr: int) -> None:
    """
    Apenas para testes
    
    binary_size: Número de bits da representação binária
    num_attr: Quantidade de atributos
    """

    _chromossome = []
    chromosome_size = (2 + (4*binary_size)) * num_attr
    for i in range(chromosome_size):
        _chromossome.append(random.randint(0,1))

    return _chromossome

if __name__=="__main__":

    '''
    Tamanho do gene: g(s) = 2 + 4*s
        onde: s é o número de bits escolhido para a representação binária
        2 operadores
        4 são os segmentos W e V à esquerda e à direita

    Tamanho do cromossomo: c(s) = g(s)*n
        onde: n é a quantidade de atributos

    Exemplo:
        s = 12
        n = 400
        g(s) = 2 + 4*12 = 50
        c(s) = 20.000

        Representação binária com 12 bits e dataset com 400 atributos = cromossomo com 20.000 bits.

    Exemplo:
        Para um atributo (1 gene), a cada aumento de 1 bit são inseridos 4 bits no cromossomo. A cada 2 bits, 8 bits são inseridos.
        Para 2 atributos (2 genes), a cada aumento de 1 bit são inseridos 8 bists no cromossomo.

        Os bits são inseridos em 4 segmentos: WL (peso da esquerda), WR (peso da direita), VL (valor da esquerda) e VR (valor da direita)
    '''

    NUM_ATTR = 2
    BIN_SIZE = 5

    gene = _generate_chromossome(BIN_SIZE, NUM_ATTR)

    print(f"Cromossomo: {gene}")
    print(f"Tamanho do cromossomo: {len(gene)}")
    print()
    print(f'PESOS: {get_decimal_weights(gene, BIN_SIZE)}')
    print(f'OPERADOR: {get_operator(gene, BIN_SIZE)}')
    print(f'VALORES: {get_decimal_value(gene, BIN_SIZE)}')