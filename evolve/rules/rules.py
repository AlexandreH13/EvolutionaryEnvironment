import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from itertools import compress, cycle, batched
import evolve.properties as properties
from logger import logger_term

class Rules:

    @staticmethod
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

    @staticmethod
    def get_min_max(min, max, d):
        """
        Algoritmo: 
            BIN-NLCEE
        Descrição:
            Com o valor decimal do segmento valor (V), calcula normalização com min-max.
        """


        _d = (d - min)/(max-min)

        return _d

    @staticmethod
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

    @staticmethod
    def get_string_operator(value: int):
        return ">=" if value==0 else "<"

    @staticmethod
    def get_operator(data: list, binary_size: int, is_string: bool=False):
        """
        Utiliza a mesma estratégia de máscara das funções get_decimal_weights e get_decimal_value
        para obter os operadores do cromossomo.
        """

        operator_mask = [False] * binary_size + [True] + [False] * binary_size
        operator_list_result = list(compress(data, cycle(operator_mask)))

        if is_string:
            operator_list_result = [Rules.get_string_operator(bit) for bit in operator_list_result]

        return operator_list_result
        
    @staticmethod
    def get_decimal_weights(data: list, binary_size: int):
        """
        Cria uma máscara para obter os 'batches' do indivíduo (list) que representam os pesos (W).
        A máscara itera sobre a lista indicando 'True' apenas nos bits que representam o segmento peso (W).

        Exemplo: Se o número de bits para representar for 4, vamos ter uma máscara como abaixo:
            mascara = [True, True, True, True, False, False, False, False, False]
        Ou seja, 4 primeiros bits para o peso, e os 5 próximos bits para o segmento valor (V) e operador (O); 4 para o valor e 1 para o operador.

        binary_size: int
            Número de bits usado para representar os segmentos peso (W) e valor (V).
        data: list
            A lista que representa a versão binária do cromossomo.
        """


        # mascara = [True, True, True, True, False, False, False, False, False]
        weight_mask = [True] * binary_size + [False] * (binary_size+1)

        weight_list_result = list(compress(data, cycle(weight_mask)))

        batch_iterator = batched(weight_list_result, binary_size)

        #binary_weight_batches = [list(batch) for batch in batch_iterator]
        decimal_weight_batches = [Rules.get_decimal(list(batch)) for batch in batch_iterator]

        return decimal_weight_batches

    @staticmethod
    def get_decimal_value(data: list, binary_size: int):

        '''
        Cria uma máscara para obter os 'batches' do indivíduo (list) que representam os pesos (W).
        A máscara itera sobre a lista indicando 'True' apenas nos bits que representam o segmento peso (W).

        Mesmo algoritmo usado em get_decimal_weights.

        binary_size: int
            Número de bits usado para representar os segmentos peso (W) e valor (V).
        data: list
            A lista que representa a versão binária do cromossomo.
        '''
        value_mask = [False] * (binary_size+1) + [True] * binary_size
        value_mask_list_result = list(compress(data, cycle(value_mask)))

        batch_iterator = batched(value_mask_list_result, binary_size)

        decimal_value_batches = [Rules.get_decimal(list(batch)) for batch in batch_iterator]

        return decimal_value_batches

    @staticmethod
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

    @staticmethod
    def get_active_segment(weight_list: list, threshold: float):
        """
        Verifica a lista de pesos e retorna os índices onde os segmentos
        estarão presentes, isto é, peso >= limiar.
        """

        true_indexes = [i for i, x in enumerate(weight_list) if x >= threshold]
        return true_indexes

    @staticmethod
    def get_condition_for_gene(operator_value: int, value_segment: float, attr_value: float):
        """
        Função que retorna o valor booleano de uma condição para um gene.
        Por exemplo: recebe um gene e o valor do atributo. o gene vai possuir o valor e o operador.
        A depender do operador, criamos a condição abaixo e retornamos o valor booleano.
        Gene-> operador: >=; valor: 0.5
        Atributo-> 0.6
        Resultado-> 0.6>=0.5 => True

        operator_value: int
            Valor que representa o operador. 0 é '>=' e 1 é '<'.
        value_segment: float
            Segmento do gene que representa o valor
        atrr_value: float
            Valor do atributo que estamos comparando
        """

        condicao = False
        # 0 é >=
        if operator_value==0:
            condicao = attr_value>=value_segment
        # 1 é <
        else:
            condicao = attr_value<value_segment
        return condicao

    @staticmethod
    def get_rule_attribute_str(crom: list, attr_list: list):
        """
        Retorna uma string com o antecedente da regra de um atributo.
        """

        # Lista dos segmentos peso (W)
        pesos = Rules.get_decimal_weights(crom, properties.BINARY_REPRESENTATION_SIZE)
        # Operadores do cromossomo
        operators = Rules.get_operator(crom, properties.BINARY_REPRESENTATION_SIZE)
        # Valores (V) do cromossomo
        values = Rules.get_decimal_value(crom, properties.BINARY_REPRESENTATION_SIZE)

        # Obtém apenas os intervalos ativos
        _valid_interval = Rules.get_active_segment(pesos, properties.WEIGHT_THRESHOLD)

        condicoes_list = []
        _i = 0
        while _i < len(_valid_interval):
            
            _interval = _valid_interval[_i] # intervalo verificado
            atributo_verificado = _interval//2 # a qual atributo pertence o intervalo

            # String da condição
            condicao_attr = f"{attr_list[atributo_verificado]} {Rules.get_string_operator(operators[_interval])} {values[_interval]}"
            # Se não for o último intervalo do cromossomo
            if _i+1 < len(_valid_interval):
                # Se o próximo intervalo for do mesmo atributo que intervalo dessa iteração, é uma condição com OU
                proximo_intervalo = _valid_interval[_i + 1]
                if proximo_intervalo //2 == atributo_verificado:
                    condicao_attr_dir = f"OR {attr_list[atributo_verificado]} {Rules.get_string_operator(operators[proximo_intervalo])} {values[proximo_intervalo]}"
                    condicao_attr = "("+condicao_attr + " " + condicao_attr_dir+")"
                    condicoes_list.append(condicao_attr)
                    _i+=2
                else:
                    condicoes_list.append("("+condicao_attr+")")
                    _i+=1
            else:
                condicoes_list.append("("+condicao_attr+")")
                _i+=1

            
            #condicoes_list.append(condicao_attr)
            #_i+=1

        rule_str = "IF"+" AND ".join(condicoes_list)
        return rule_str

    @staticmethod
    def get_rule_attribute_str_final(crom: list):
        """
        Retorna uma string com o antecedente da regra de um atributo.
        """

        # Lista dos segmentos peso (W)
        pesos = Rules.get_decimal_weights(crom, properties.BINARY_REPRESENTATION_SIZE)
        # Operadores do cromossomo
        operators = Rules.get_operator(crom, properties.BINARY_REPRESENTATION_SIZE)
        # Valores (V) do cromossomo
        values = Rules.get_decimal_value(crom, properties.BINARY_REPRESENTATION_SIZE)

        # Obtém apenas os intervalos ativos
        _valid_interval = Rules.get_active_segment(pesos, properties.WEIGHT_THRESHOLD)

        condicoes_list = []
        _i = 0
        while _i < len(_valid_interval):
            
            _interval = _valid_interval[_i] # intervalo verificado
            atributo_verificado = _interval//2 # a qual atributo pertence o intervalo

            # String da condição
            condicao_attr = f"ATTR{atributo_verificado} {Rules.get_string_operator(operators[_interval])} {values[_interval]}"
            # Se não for o último intervalo do cromossomo
            if _i+1 < len(_valid_interval):
                # Se o próximo intervalo for do mesmo atributo que intervalo dessa iteração, é uma condição com OU
                proximo_intervalo = _valid_interval[_i + 1]
                if proximo_intervalo //2 == atributo_verificado:
                    condicao_attr_dir = f"OR ATTR{atributo_verificado} {Rules.get_string_operator(operators[proximo_intervalo])} {values[proximo_intervalo]}"
                    condicao_attr = "("+condicao_attr + " " + condicao_attr_dir+")"
                    condicoes_list.append(condicao_attr)
                    _i+=2
                else:
                    condicoes_list.append("("+condicao_attr+")")
                    _i+=1
            else:
                condicoes_list.append("("+condicao_attr+")")
                _i+=1

            
            #condicoes_list.append(condicao_attr)
            #_i+=1

        rule_str = "IF"+" AND ".join(condicoes_list)
        return rule_str

    @staticmethod
    def map_cromosome_to_rule(crom: str, attr_list: list):
        """Mapeamento do genótipo para o fenótipo. Verifica se a regra obtida pelo cromossomo classifica
        um dado. Recebe a lista dos valores dos atributos, transforma o cromossomo na regra e classifica.
        A classificação ocorre verificando cada intervalo dos genes que estão ativos. É verificado também a qual
        atributo o intervalo pertence (intervalo//2). Se dois intervalos estiverem ativos para um atributo eles são concatenados
        com o conector OU. Senão, apenas uma condição é utilizada. Uma regra só é válida se todas as condições forem
        True.

        Um exemplo:
            intervalo esquerdo: ativo | >= | 0.4
            intervalor direito: ativo | < | 0.78
            Regra: SE ATTR >= 0.4 OU ATTR < 0.78
        Outro exemplo:
            intervalo esquerdo: não ativo | >= | 0.2
            intervalor direito: ativo | < | 0.55
            Regra: SE ATTR < 0.55

        crom: str
            Cromossomo no formato binário.
        attr_list: list
            Lista com os valores dos atributos.
        """

        if not crom:
            return None

        # Uma regra válida (cromossomo) é aquela onde todas as condições (genes) são True
        valid_rule = True

        pesos = Rules.get_decimal_weights(crom, properties.BINARY_REPRESENTATION_SIZE)

        # Indices da partição válida. É uma lista
        # Cada gene tem duas partições (intervalo superior e inferior)
        # Para obter o atributo da partição ativa, usamos: índice_particao//2
        _valid_interval = Rules.get_active_segment(pesos, properties.WEIGHT_THRESHOLD)
        logger_term.debug("PESOS: %s", pesos)
        logger_term.debug("INTERVALOS ATIVOS: %s", _valid_interval)

        # Se nenhum intervalo (esquerdo ou direito) for válido, regra não é válida.
        if not _valid_interval:
            valid_rule = False

        # Operadores do cromossomo
        operators = Rules.get_operator(crom, properties.BINARY_REPRESENTATION_SIZE)
        # Valores (V) do cromossomo
        values = Rules.get_decimal_value(crom, properties.BINARY_REPRESENTATION_SIZE)
        logger_term.debug("VALORES: %s", values)

        # Faz mapeamento apenas se houver intervalos válidos
        if valid_rule:
            _i = 0

            # Itera sobre os intervalos válidos e não sobre os atributos
            # Mais eficiente uma vez que podemos ter atributos sem intervalos válidos
            while _i < len(_valid_interval):
                # Intervalo verificado na iteração
                _interval = _valid_interval[_i]
                # Índice do atributo que pertence ao intervalo
                atributo_verificado = _interval//2
                logger_term.debug("VERIFICAÇÃO DO INTERVALO %s PARA O ATRIBUTO %s", _interval, attr_list[atributo_verificado])

                # Obtém valor booleano da condição formada pelo gene
                valor_bool_condicao_esq = Rules.get_condition_for_gene(operators[_interval], values[_interval], attr_list[atributo_verificado])

                # Verifica se existe um próximo intervalo na lista (out of bounds)
                if _i+1 < len(_valid_interval):
                    proximo_intervalo = _valid_interval[_i + 1]
                    # Se o próximo segmento válido pertence ao mesmo atributo (gene), é uma regra com conector OU
                    if proximo_intervalo //2 == atributo_verificado:
                        logger_term.debug("Intervalo %s e seu conseguinte %s são do mesmo atributo %s", _interval, proximo_intervalo, atributo_verificado)
                        # Primeira condição à esquerda é o valor_bool_condicao_esq
                        # Segunda condição à direita
                        valor_bool_condicao_dir = Rules.get_condition_for_gene(operators[proximo_intervalo], values[proximo_intervalo], attr_list[atributo_verificado])
                        # OU
                        valor_bool_condicao = valor_bool_condicao_esq or valor_bool_condicao_dir
                        # Pula o próximo intervalo válido já que usamos nessa condição
                        _i+=2
                    else:
                        valor_bool_condicao = valor_bool_condicao_esq
                        _i+=1
                else:
                    valor_bool_condicao = valor_bool_condicao_esq
                    _i+=1

                # Se uma condição for falsa, a regra é falsa
                if not valor_bool_condicao:
                    valid_rule = False
                    break

        if valid_rule:
            logger_term.debug("REGRA CLASSIFICA")
        else:
            logger_term.debug("REGRA NÃO CLASSIFICA")

        return valid_rule


if __name__=="__main__":

    '''
    Tamanho do gene: g(s) = 2 + 4*s
        onde: s é o número de bits escolhido para a representação binária
        2 operadores (< e >=)
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
        DEPRECIADO(?)
        Para um atributo (1 gene), a cada aumento de 1 bit são inseridos 4 bits no cromossomo. A cada 2 bits, 8 bits são inseridos.
        Para 2 atributos (2 genes), a cada aumento de 1 bit são inseridos 8 bists no cromossomo.

        Os bits são inseridos em 4 segmentos: WL (peso da esquerda), WR (peso da direita), VL (valor da esquerda) e VR (valor da direita)
    '''

    atributos = [0.5]
    NUM_ATTR = len(atributos)
    crom = Rules._generate_chromossome(properties.BINARY_REPRESENTATION_SIZE, NUM_ATTR)
    pesos = Rules.get_decimal_weights(crom, properties.BINARY_REPRESENTATION_SIZE)

    print(f"CROMOSSOMO: {crom}")
    print(f"TAMANHO DO CROMOSSOMO: {len(crom)}")
    print(f"TAMANHO DO GENE: {len(crom)/NUM_ATTR}")

    print()

    print(f"VALORES DECIMAIS DOS SEGMENTOS 'PESO': {pesos}")

    print()

    print(f"VALORES DECIMAIS DOS SEGMENTOS 'VALOR': {Rules.get_decimal_value(crom, properties.BINARY_REPRESENTATION_SIZE)}")

    print()

    print(f'OPERADOR: {Rules.get_operator(crom, properties.BINARY_REPRESENTATION_SIZE)}')
    print(f'OPERADOR STRING: {Rules.get_operator(crom, properties.BINARY_REPRESENTATION_SIZE, is_string=True)}')

    print()

    print(f"MAPEAMENTO")
    print(f"ATRIBUTOS: {atributos}")
    Rules.map_cromosome_to_rule(crom, atributos)

    