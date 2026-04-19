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

def get_operator(value: int):
    """
    Retorna operador de comparação.
    """
    return ">=" if value==0 else "<"

def get_rule_attribute_str(binary_weight: list, binary_value: list, operator: int):
    """
    Retorna uma string com o antecedente da regra de um atributo.
    """
    _d_weight = get_decimal(binary_weight) # Decimal do segmento peso
    _d_value = get_decimal(binary_value) # Decimal do segmento valor
    _s_operator = get_operator(operator) # String do operador

    return f"{_d_weight}{_s_operator}{_d_value}"

if __name__=="__main__":

    w = [1,1,1,1,0,0]
    v = [0,1,0,1,1,1]
    o = 1
    print(get_rule_attribute_str(w, v, o))
    