import openml
import pandas as pd
import numpy as np
from pathlib import Path
import evolve.properties as properties
from logger import logger_term

class DataProperties:
    """Classe que prepara os dados para a classificação com o AG.
    Pode ser usado um .csv ou carregado um dataset no OpenML.
    Independente da meneira, é necessário carregar o dataset (load_dataset ou load_openml_dataset)
    antes de chamar o get_data().
    """

    def __init__(self, dataset_name: str="", openml_dataset_id: int=0):

        self.dataset_path = "data/"
        self.dataset_name = dataset_name
        self.openml_dataset_id = openml_dataset_id
        self.dataframe = None
        self.data_properties = {}

    def get_data(self):

        if self.dataframe.empty:
            logger_term.error("Nenhum dataframe foi carregado.")
            logger_term.error("Execute load_dataset ou load_openml_dataset.")
        return self.dataframe

    def load_dataset(self):

        if self.dataset_name=="":
            logger_term.error("Dataset não encontrado!")
            logger_term.error("Para datasets locais, informe o caminho do mesmo!")
            return 0

        logger_term.info("Carregando dataset...")
        ext = Path(self.dataset_path+self.dataset_name).suffix
        if ext != ".csv":
            logger_term.error("Dataset não está no formato adequado: CSV")
            logger_term.error(f"Formato encontrado: {ext}")
            return None
        df = pd.read_csv(self.dataset_path+self.dataset_name)
        self.dataframe = df

    def load_openml_dataset(self):

        dataset = openml.datasets.get_dataset(self.openml_dataset_id)
        self.dataset_name = dataset.name
        df_data = dataset.get_data(dataset_format="dataframe")[0]
        self.dataframe = df_data

    def remove_column(self, cols=[]):
        if not cols:
            logger_term.error("Lista de colunas vazia")
        self.dataframe.drop(columns=cols, inplace=True)

    def get_num_attr(self, cols_to_remove=[]):
        if not cols_to_remove:
            logger_term.error("Deve ser passado as colunas a serem removidas para calcular o número de atibutos.")
        return len(self.dataframe.columns)-len(cols_to_remove) # Descarta coluna target

    def prepare_for_ga(self, cols_to_remove=[], target_column="", class_name=""):
        """Prepara o conjunto de dados para o AG classificador.
        Segue os seguintes passos:
        1. Batch size, se passado
        2. Remove coluna, quando passado
        3. Normaliza com min-max
        4. Dividir X e y

        Argumentos:
            batch_size (int): Tamanho da amostra que o AG irá usar para descobrir regras.
            cols_to_remove (list): Remove colunas passadas.
        """

        logger_term.info("PREPARANDO DADOS PARA O AG...")

        if not target_column in self.dataframe.columns:
            logger_term.error(f"A coluna target {target_column} não existe.")
            return None

        if class_name=="":
            logger_term.error("Uma classe deve ser informada.")
            return None

        # Batch
        self.dataframe = self.dataframe.sample(frac=properties.BATCH_SIZE)

        # Cópia do dataframe original
        ga_data = self.dataframe

        # Shuffle
        ga_data = ga_data.sample(frac=1)

        if cols_to_remove:
            if not set(cols_to_remove).issubset(self.dataframe.columns):
                logger_term.error("Alguma coluna passada para remoção não existe")
                return None
            ga_data.drop(columns=cols_to_remove, inplace=True)
            logger_term.info(f"Colunas removidas: {cols_to_remove}")

        # Min-max nas colunas, exceto na target
        for col in ga_data.columns:
            if not col==target_column:
                ga_data[col] = (ga_data[col] - ga_data[col].min())/(ga_data[col].max() - ga_data[col].min())

        logger_term.info(f"Dados filtrados. A classe selecionada foi {class_name}. O conjunto de dados para o treinamento agora é de {len(ga_data)}")
        # Obtém X
        X = ga_data.drop(columns=[target_column]).to_numpy()

        # Obtém y
        y = ga_data[target_column].to_numpy()

        logger_term.info("DADOS PREPARADOS")

        return (X,y)
