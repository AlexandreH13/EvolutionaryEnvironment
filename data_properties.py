import pandas as pd
from pathlib import Path
from logger import logger_term

class DataProperties:

    def __init__(self, dataset_name: str):

        self.dataset_path = "data/"
        self.dataset_name = dataset_name
        self.dataframe = self._load_dataset()
        self.data_properties = {}

    def get_data(self):
        return self.dataframe

    def _load_dataset(self):

        logger_term.info("Carregando dataset...")
        ext = Path(self.dataset_path+self.dataset_name).suffix
        if ext != ".csv":
            logger_term.error("Dataset não está no formato adequado: CSV")
            logger_term.error(f"Formato encontrado: {ext}")
            return None
        df = pd.read_csv(self.dataset_path+self.dataset_name)

        return df


    def remove_column(self, cols=[]):
        if not cols:
            logger_term.error("Lista de colunas vazia")
        self.dataframe.drop(columns=cols, inplace=True)

    def get_num_attr(self, cols_to_remove=[]):
        if not cols_to_remove:
            logger_term.error("Deve ser passado as colunas a serem removidas para calcular o número de atibutos.")
        return len(self.dataframe.columns)-len(cols_to_remove) # Descarta coluna target

    def prepare_for_ga(self, batch_size=1, cols_to_remove=[], target_column="", class_name=""):
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

        # Cópia do dataframe original
        ga_data = self.dataframe

        # Shuffle
        ga_data = ga_data.sample(frac=1)

        if batch_size<1:
            logger_term.info(f"Selecionando amostra com batch de tamanho {batch_size}")
            ga_data = ga_data.sample(frac=batch_size)

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

        # Filtra por classe
        ga_data = ga_data[ga_data[target_column]==class_name]
        if ga_data.empty:
            logger_term.error(f"A classe informada não existe. Nome da classe {class_name}.")
            return None

        print(f"Dados filtrados. A classe selecionada foi {class_name}. O conjunte de dados para o treinamento agora é de {len(ga_data)}")
        # Obtém X
        X = ga_data.drop(columns=[target_column]).to_numpy()

        # Obtém y
        y = ga_data[target_column].to_numpy()

        return (X,y)

        logger_term.info("DADOS PREPARADOS")
if __name__=="__main__":

    dt = DataProperties("Iris.csv")
    dt.prepare_for_ga(batch_size=0.1, cols_to_remove=["Id"], target_column="Species", class_name="Iris-setosa")
    