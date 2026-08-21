import pandas as pd
from pathlib import Path

class DataProperties:

    def __init__(self, dataset_name: str):

        self.dataset_path = "data/"
        self.dataset_name = dataset_name
        self.dataframe = self._load_dataset()
        self.data_properties = {}

    def get_data(self):
        return self.dataframe

    def _load_dataset(self):

        ext = Path(self.dataset_path+self.dataset_name).suffix
        if ext != ".csv":
            print("Dataset não está no formato adequado: CSV")
            print(f"Formato encontrado: {ext}")
            return None
        df = pd.read_csv(self.dataset_path+self.dataset_name)

        return df


    def remove_column(self, cols=[]):
        if not cols:
            print("Lista de colunas vazia")
        self.dataframe.drop(columns=cols, inplace=True)


if __name__=="__main__":

    dt = DataProperties("Iris.csv")
    print(dt.get_data().head())
    dt.remove_column(cols=["Id", "Species"])
    print(dt.get_data().head())
    