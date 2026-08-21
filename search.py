from data_properties import DataProperties

class Search:

    """Classe que implementa a lógica da busca por regras de classificação para determinada
    classe usando o algoritmo genético implementado no módulo "evolve".

    Algoritmo:
        Cada indivíduo do AG passa em todos os dados tentando classificá-los. O seu fitness
        é a média das medidas de sensibilidade e especificidade.
    """

    @staticmethod
    def class_search(data: DataProperties, target_column: str, class_name: str):

        if not target_column in data.columns:
            print("Coluna target não existe")
            return None


        _data_filtered_by_class = data[data[target_column]==class_name]
        if _data_filtered_by_class.empty:
            print("A classe passada não existe no conjunto de dados.")
            return None

        # Itera usando itertuples por ser mais eficiente computacionalmente
        for row in _data_filtered_by_class.itertuples(index=True):
            print(f"Dado: {row}")
            # Verificar se os valores estão como float
            # Obter lista dos atributos

        
        

if __name__=="__main__":

    data = DataProperties("Iris.csv")
    data.remove_column(cols=["Id"])
    df = data.get_data()
    Search.class_search(df, "Species", "Iris-setosa")
    