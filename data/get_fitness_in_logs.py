"""
Obtém o fitness do melhor indivíduo de cada geração nos logs e insere em um Pandas DataFrame.

Deve ser executado em uma operação separada ao AG para não influenciar no tempo de execução
"""

import pandas as pd
import matplotlib.pyplot as plt

def read_logs(logs_path: str="../exp.log"):

    df_exp = pd.read_csv(logs_path)
    if df_exp.empty:
        print("O dataframe do experimento está vazio.")
        return None

    return df_exp

if __name__=="__main__":

    df = read_logs()
    df.plot(kind="line", x="gen", y="fit")
    plt.show()