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
        self.categorical_indicator = None
        self.attribute_names = None
        self.categorical_dummy_map = {}

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
        df_data, _, categorical_indicator, attribute_names = dataset.get_data(dataset_format="dataframe")
        self.dataframe = df_data
        self.categorical_indicator = categorical_indicator
        self.attribute_names = attribute_names

    def remove_column(self, cols=[]):
        if not cols:
            logger_term.error("Lista de colunas vazia")
        self.dataframe.drop(columns=cols, inplace=True)

    def encode_categoricals(self, target_column=""):
        """
        Codifica colunas categóricas via one-hot (pd.get_dummies), substituindo-as no
        dataframe por colunas binárias (uma por categoria). Necessário porque o BIN-NLCEE
        só representa condições de intervalo (>=, <), que não fazem sentido pra atributos
        nominais sem ordem.

        Detecção de quais colunas são categóricas: usa o categorical_indicator do OpenML
        quando disponível (setado por load_openml_dataset); senão, detecta automaticamente
        colunas com dtype object/category (caso de dataset local via load_dataset).

        Mantém self.categorical_dummy_map = {nome_da_dummy: (atributo_original, categoria)},
        usado depois para decodificar a regra de volta (ver denormalize_rule.py) e para
        prepare_for_ga() pular a normalização min-max nessas colunas (já estão em [0,1]).
        """
        if self.categorical_indicator is not None and self.attribute_names is not None:
            categorical_columns = [
                name for name, is_cat in zip(self.attribute_names, self.categorical_indicator)
                if is_cat and name != target_column and name in self.dataframe.columns
            ]
        else:
            categorical_columns = [
                col for col in self.dataframe.columns
                if col != target_column and self.dataframe[col].dtype.name in ("object", "category")
            ]

        if not categorical_columns:
            logger_term.info("Nenhuma coluna categórica detectada.")
            return []

        self.categorical_dummy_map = {}
        for col in categorical_columns:
            dummies = pd.get_dummies(self.dataframe[col], prefix=col).astype(float)
            for dummy_col in dummies.columns:
                category = dummy_col[len(col) + 1:]
                self.categorical_dummy_map[dummy_col] = (col, category)
            self.dataframe = pd.concat([self.dataframe.drop(columns=[col]), dummies], axis=1)

        logger_term.info(f"Colunas categóricas codificadas (one-hot): {categorical_columns}")
        return categorical_columns

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
        ga_data = ga_data.sample(frac=1, random_state=properties.SEED)

        if cols_to_remove:
            if not set(cols_to_remove).issubset(self.dataframe.columns):
                logger_term.error("Alguma coluna passada para remoção não existe")
                return None
            ga_data.drop(columns=cols_to_remove, inplace=True)
            logger_term.info(f"Colunas removidas: {cols_to_remove}")

        # Min-max nas colunas, exceto na target e nas colunas categóricas (one-hot, já em [0,1])
        for col in ga_data.columns:
            if col != target_column and col not in self.categorical_dummy_map:
                ga_data[col] = (ga_data[col] - ga_data[col].min())/(ga_data[col].max() - ga_data[col].min())

        logger_term.info(f"Dados filtrados. A classe selecionada foi {class_name}. O conjunto de dados para o treinamento agora é de {len(ga_data)}")
        # Obtém X
        X = ga_data.drop(columns=[target_column]).to_numpy()

        # Obtém y
        y = ga_data[target_column].to_numpy()

        logger_term.info("DADOS PREPARADOS")

        return (X,y)
