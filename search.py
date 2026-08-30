import evolve.properties as properties
from evolve.ga import GeneticAlgorithm
from evolve.crossover.crossover import OnePoint, TwoPoint
from evolve.mutation.mutation import BitFlipMutation
from data_properties import DataProperties
from logger import logger_arq


class Search:

    """Classe que implementa a lógica da busca por regras de classificação para determinada
    classe usando o algoritmo genético implementado no módulo "evolve".

    Algoritmo:
        Cada indivíduo do AG passa em todos os dados tentando classificá-los. O seu fitness
        é a média das medidas de sensibilidade e especificidade.
    """

    @staticmethod
    def class_search(data: tuple, cols_to_remove: list, target_column: str, class_name: str, batch_size: int):

        ## FAZER: Função que verifica se colunas são do tipo float

        X,y = data.prepare_for_ga(
            batch_size=batch_size, 
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

    logger_arq.info("INICIANDO EXECUÇÃO")
    dataset_name = "bc_wisconsin.csv"
    logger_arq.info(f"DATASET: {dataset_name}")

    # Fórmula do tamanho do gene: 2+4*s, onde s = representação binária
    gene_size = 2+4*properties.BINARY_REPRESENTATION_SIZE

    data = DataProperties("bc_wisconsin.csv")

    dt = data.get_data()
    
    # Número de atributos, desconsiderando a classe
    num_attr = data.get_num_attr(cols_to_remove=["id", "diagnosis", "Unnamed: 32"])
    properties.NUM_ATTR = num_attr

    # Fórmula do tamanho do cromossomo
    properties.INDIVIDUAL_LEN = gene_size*num_attr

    config_exec = f"""CONFIGURAÇÃO DA EXECUÇÃO: \n
                      NÚMERO DE ATRIBUTOS: {num_attr} \n
                      TAMANHO DA REPRESENTAÇÃO BINÁRIA: {properties.BINARY_REPRESENTATION_SIZE} \n
                      TAMANHO DO GENE: {gene_size} \n
                      TAMANHO DO CROMOSSOMO: {properties.INDIVIDUAL_LEN}"""
    logger_arq.info(config_exec)

    Search.class_search(data, cols_to_remove=["id", "Unnamed: 32"], target_column="diagnosis", class_name="M", batch_size=properties.BATCH_SIZE)
    