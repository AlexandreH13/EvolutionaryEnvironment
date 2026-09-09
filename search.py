import evolve.properties as properties
from evolve.ga import GeneticAlgorithm
from evolve.crossover.crossover import OnePoint, TwoPoint
from evolve.mutation.mutation import BitFlipMutation
from data_properties import DataProperties
from logger import logger_arq
import argparse
import openml


class Search:

    """Classe que implementa a lógica da busca por regras de classificação para determinada
    classe usando o algoritmo genético implementado no módulo "evolve".

    Algoritmo:
        Cada indivíduo do AG passa em todos os dados tentando classificá-los. O seu fitness
        é a média das medidas de sensibilidade e especificidade.
    """

    @staticmethod
    def class_search(data: tuple, cols_to_remove: list, target_column: str, class_name: str):

        ## FAZER: Função que verifica se colunas são do tipo float

        X,y = data.prepare_for_ga( 
            cols_to_remove=cols_to_remove, 
            target_column=target_column, 
            class_name=class_name)

        runner = GeneticAlgorithm(
            crossover=OnePoint(),
            mutation=BitFlipMutation(properties.MUTATION_RATE)
        )

        ## Passar y é defasado, uma vez que executa para cada classe
        runner.evolve((X,y))
       
        

if __name__=="__main__":
    """
    ATENÇÃO:
        - Sempre lembrar de verificar se o "num_attr" está correto.
        - Nome da classe a ser buscada é string, exemplo classe "1" ou classe "0"
    """

    """
    OpenML Datasets IDs, for tabular classification benchmark:

    ID     |   Name
    37     |   diabetes
    1461   |   bank
    1464   |   blood transfusion
    15     |   breast-w
    29     |   credit approval
    43939  |   california housing
    43672  |   heart disease
    21     |   car safety
    179    |   income

    Execution example for the blood transfusion dataset. No cols to remove.:
        python3 search.py -b 8 -d 1464 -bts 0.8 -w 0.6 -p 100 -g 100 -c 1 -t Class

    """

    parser = argparse.ArgumentParser(description="GA configuration")
    parser.add_argument("-b", "--binsize", 
                        type=int, help="Number of bits to define the gene size.")
    parser.add_argument("-d", "--iddata", 
                        type=int, help="OpenML dataset ID")
    parser.add_argument("-bts", "--batchsize",
                        type=float, help="Batch size")
    parser.add_argument("-w", "--weight",
                        type=float, help="Weight threshold")
    parser.add_argument("-p", "--popsize",
                        type=int, help="Population size")
    parser.add_argument("-g", "--gen",
                        type=int, help="Number of generations")
    parser.add_argument("-c", "--classname",
                        type=str, help="Class name") # Classe que o AG vai minerar regra
    parser.add_argument("-t", "--targetcol",
                        type=str, help="Target column")
    parser.add_argument("-r", "--colsremove",
                        type=str, nargs="*", 
                        help="Cols not to use")

    args = parser.parse_args()

    properties.BINARY_REPRESENTATION_SIZE = args.binsize
    properties.BATCH_SIZE = args.batchsize
    properties.WEIGHT_THRESHOLD = args.weight
    properties.POPULATION_SIZE = args.popsize
    properties.GENERATIONS = args.gen
    properties.CLASS_NAME = args.classname

    logger_arq.info("INICIANDO EXECUÇÃO")

    # ID do dataset no OpenML
    dataset_id = args.iddata

    # Fórmula do tamanho do gene: 2+4*s, onde s = representação binária
    gene_size = 2+4*properties.BINARY_REPRESENTATION_SIZE

    data = DataProperties(openml_dataset_id=dataset_id)

    # Carrega o dataframe
    data.load_openml_dataset()

    #dataset_name = "Heart/heart.csv"
    dataset_name = data.dataset_name
    logger_arq.info(f"DATASET: {dataset_name}")
    
    # Número de atributos, desconsiderando a classe e id, quando houver
    num_attr = data.get_num_attr(cols_to_remove=["Class"])
    properties.NUM_ATTR = num_attr

    # Fórmula do tamanho do cromossomo
    properties.INDIVIDUAL_LEN = gene_size*num_attr
    # Taxa de mutação dinâmica: 1/Tamanho do indivíduo
    properties.MUTATION_RATE = 1 / properties.INDIVIDUAL_LEN

    config_exec = f"""CONFIGURAÇÃO DA EXECUÇÃO:
                      BIN SIZE: {properties.BINARY_REPRESENTATION_SIZE}
                      DATASET: {args.iddata}
                      BATCH SIZE: {properties.BATCH_SIZE}
                      WEIGHT: {properties.WEIGHT_THRESHOLD}
                      POPULAÇÃO: {properties.POPULATION_SIZE}
                      GERAÇÕES: {properties.GENERATIONS}
                      CLASSE BUSCADA: {properties.CLASS_NAME}
                      COLUNA TARGET: {args.targetcol}
                      NÚMERO DE ATRIBUTOS: {num_attr}
                      TAMANHO DA REPRESENTAÇÃO BINÁRIA: {properties.BINARY_REPRESENTATION_SIZE}
                      TAMANHO DO GENE: {gene_size}
                      TAMANHO DO CROMOSSOMO: {properties.INDIVIDUAL_LEN}
                      MUTAÇÃO: {properties.MUTATION_RATE}"""
    logger_arq.info(config_exec)

    colunas_para_desconsiderar = []
    coluna_target = args.targetcol
    class_searched = str(properties.CLASS_NAME)

    Search.class_search(data, cols_to_remove=[], target_column=coluna_target, class_name=class_searched)
    