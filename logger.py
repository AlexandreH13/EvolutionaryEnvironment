'''

Existem dois níveis de logs:
* logs_arq: Salva os logs no arquivo rules.log. Para verificar os melhores de cada geração
e a melhor regra encontrada. Mais usado para salvar os experimentos.

* logs_term: Logs do terminal. Mais detalhado e para validações.

'''

import logging

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 1. Logger exclusivo para o Arquivo
logger_arq = logging.getLogger("log_arquivo")
logger_arq.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("rules.log", encoding="utf-8", mode="w")
file_handler.setFormatter(formatter)
logger_arq.addHandler(file_handler)
logger_arq.propagate = False # Impede que o log suba para o root handler

# 2. Logger exclusivo para o Terminal
logger_term = logging.getLogger("log_terminal")
logger_term.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger_term.addHandler(stream_handler)
logger_term.propagate = False

# 3. Logger exclusivo para salvar dados e gerar os gráficos e tabelas dos experimentos
logger_exp = logging.getLogger("log_exp")
logger_exp.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("exp.log", encoding="utf-8", mode="w")
#file_handler.setFormatter(formatter) # Sem o formatter
logger_exp.addHandler(file_handler)
logger_exp.propagate = False # Impede que o log suba para o root handler

# 3. Logger exclusivo para salvar dados e gerar os gráficos e tabelas dos experimentos
logger_test = logging.getLogger("test")
logger_test.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("test.log", encoding="utf-8", mode="w")
#file_handler.setFormatter(formatter) # Sem o formatter
logger_test.addHandler(file_handler)
logger_test.propagate = False # Impede que o log suba para o root handler