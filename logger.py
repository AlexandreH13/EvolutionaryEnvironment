'''

Existem dois níveis de logs:
* logs_arq: Salva os logs no arquivo rules.log. Para verificar os melhores de cada geração
e a melhor regra encontrada. Mais usado para salvar os experimentos.

* logs_term: Logs do terminal. Mais detalhado e para validações.

'''

import logging
import evolve.properties as properties

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 1. Logger exclusivo para o Arquivo
logger_arq = logging.getLogger("log_arquivo")
logger_arq.setLevel(logging.DEBUG)
logger_arq.propagate = False # Impede que o log suba para o root handler

# 2. Logger exclusivo para o Terminal
logger_term = logging.getLogger("log_terminal")
logger_term.setLevel(logging.INFO) # DEBUG só é ativado via properties.VERBOSE em init_file_loggers()
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger_term.addHandler(stream_handler)
logger_term.propagate = False

# 3. Logger exclusivo para salvar dados e gerar os gráficos e tabelas dos experimentos
logger_exp = logging.getLogger("log_exp")
logger_exp.setLevel(logging.DEBUG)
logger_exp.propagate = False # Impede que o log suba para o root handler


def init_file_loggers():
    """
    Cria/recria os FileHandlers de logger_arq e logger_exp com os nomes de arquivo
    baseados nos valores atuais de properties.CLASS_NAME/SEED/CONFIG.

    Precisa ser chamada explicitamente DEPOIS que o argparse já tiver atribuído
    esses valores em evolve/properties.py (em search.py). Se os handlers fossem
    criados no import do módulo, os nomes dos arquivos ficariam presos aos valores
    default de properties.py, já que o import de "logger" (via evolve.ga e
    data_properties) acontece antes do argparse rodar.
    """
    for handler in list(logger_arq.handlers):
        logger_arq.removeHandler(handler)
        handler.close()
    for handler in list(logger_exp.handlers):
        logger_exp.removeHandler(handler)
        handler.close()

    logger_term.setLevel(logging.DEBUG if properties.VERBOSE else logging.INFO)

    arq_handler = logging.FileHandler(f"data/experiments/rules_dataset{properties.IDDATASET}_class{properties.CLASS_NAME}_seed{properties.SEED}_config{properties.CONFIG}.log", encoding="utf-8", mode="w")
    arq_handler.setFormatter(formatter)
    logger_arq.addHandler(arq_handler)

    exp_handler = logging.FileHandler(f"data/experiments/exp_dataset{properties.IDDATASET}_class{properties.CLASS_NAME}_seed{properties.SEED}_config{properties.CONFIG}.log", encoding="utf-8", mode="w")
    #exp_handler.setFormatter(formatter) # Sem o formatter
    logger_exp.addHandler(exp_handler)


# 4. Logger exclusivo para salvar dados e gerar os gráficos e tabelas dos experimentos
logger_test = logging.getLogger("test")
logger_test.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("test.log", encoding="utf-8", mode="w")
#file_handler.setFormatter(formatter) # Sem o formatter
logger_test.addHandler(file_handler)
logger_test.propagate = False # Impede que o log suba para o root handler