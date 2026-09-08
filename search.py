import evolve.properties as properties
from evolve.ga import GeneticAlgorithm
from evolve.crossover.crossover import OnePoint, TwoPoint
from evolve.mutation.mutation import BitFlipMutation
from data_properties import DataProperties
from logger import logger_arq
import openml


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

    """

    logger_arq.info("INICIANDO EXECUÇÃO")

    # ID do dataset no OpenML
    dataset_id=1464

    # Fórmula do tamanho do gene: 2+4*s, onde s = representação binária
    gene_size = 2+4*properties.BINARY_REPRESENTATION_SIZE

    data = DataProperties(openml_dataset_id=dataset_id)

    # Carrega o dataframe
    data.load_openml_dataset()

    # DataFrame
    dt = data.get_data()

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
                      NÚMERO DE ATRIBUTOS: {num_attr}
                      TAMANHO DA REPRESENTAÇÃO BINÁRIA: {properties.BINARY_REPRESENTATION_SIZE}
                      TAMANHO DO GENE: {gene_size}
                      TAMANHO DO CROMOSSOMO: {properties.INDIVIDUAL_LEN}"""
    logger_arq.info(config_exec)

    colunas_para_desconsiderar = []
    coluna_target = "Class"
    nome_classe = "1" # Classe que o AG vai minerar regra
    properties.CLASS_NAME=nome_classe

    Search.class_search(data, cols_to_remove=[], target_column=coluna_target, class_name=nome_classe, batch_size=properties.BATCH_SIZE)
    