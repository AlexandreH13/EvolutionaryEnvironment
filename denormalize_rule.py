"""

@author: Alexandre Alves, Msc.

Script utilitário para desnormalizar a regra final de uma execução do BIN-NLCEE.

A regra já decodificada (linha "REGRA DA MELHOR SOLUÇÃO" do rules_*.log) usa valores
normalizados via min-max (escala [0...1]) e nomes genéricos de atributo (ATTR0, ATTR1, ...).
Este script troca cada valor normalizado pelo valor real (desnormalizado) do atributo,
usando o dataset original do OpenML, e troca ATTR{i} pelo nome legível do atributo.

Reusa DataProperties (mesma classe usada por search.py) pra carregar e codificar o dataset
exatamente como foi feito na mineração — isso é essencial quando há colunas categóricas:
elas viram colunas one-hot (ver DataProperties.encode_categoricals), e o índice ATTR{i} só
aponta pra coluna certa se a expansão for reproduzida na mesma ordem. Pra essas colunas, a
condição não é desnormalizada numericamente (não faz sentido numa dummy 0/1) — é traduzida
de volta pra "<atributo original> = <categoria>" (ou "≠", se o operador era "<").

Uso:
    python3 denormalize_rule.py data/experiments/dataset37/rules_dataset37_classtested_positive_seed16_config1.log
    ATENÇÃO: Cada dataset deve ter seu dicionário FEATURE_NAMES
"""

import argparse
import re

from data_properties import DataProperties

FEATURE_NAMES = {
    "preg": "Number of times pregnant",
    "plas": "Plasma glucose concentration at 2 hours in an oral glucose tolerance test (GTT)",
    "pres": "Diastolic blood pressure",
    "skin": "Triceps skin fold thickness",
    "insu": "2-hour serum insulin",
    "mass": "Body mass index",
    "pedi": "Diabetes pedigree function",
    "age": "Age",
}


def denormalize(n, col_min, col_max):
    """Inverso da normalização min-max: valor_real = valor_normalizado * (max - min) + min."""
    return n * (col_max - col_min) + col_min


def parse_log(path):
    """Extrai dataset/coluna target (OpenML) e a última linha 'REGRA DA MELHOR SOLUÇÃO' do log."""
    text = open(path, encoding="utf-8").read()

    dataset_id = int(re.search(r"DATASET: (\d+)", text).group(1))
    target_column = re.search(r"COLUNA TARGET: (\S+)", text).group(1)

    rule_matches = re.findall(r"REGRA DA MELHOR SOLUÇÃO: (.+)", text)
    if not rule_matches:
        raise ValueError(f"Nenhuma linha 'REGRA DA MELHOR SOLUÇÃO' encontrada em {path}")

    return dataset_id, target_column, rule_matches[-1]


def denormalize_rule(rule_line, attr_cols, col_min, col_max, categorical_dummy_map):
    """Troca ATTR{i} <op> <valor> pela condição legível — numérica desnormalizada, ou
    "<atributo> = <categoria>" / "≠" se ATTR{i} for uma coluna categórica (one-hot)."""

    def replace_match(m):
        attr_idx, op, value = int(m.group(1)), m.group(2), float(m.group(3))
        col = attr_cols[attr_idx]

        if col in categorical_dummy_map:
            original_col, category = categorical_dummy_map[col]
            equality_op = "=" if op == ">=" else "≠"  # ">=" na dummy -> "=" ; "<" -> "≠"
            return f"{FEATURE_NAMES.get(original_col, original_col)} {equality_op} {category}"

        real_value = denormalize(value, col_min[col], col_max[col])
        return f"{FEATURE_NAMES.get(col, col)} {op} {real_value:.2f}"

    return re.sub(r"ATTR(\d+)\s*(>=|<)\s*([\d.]+)", replace_match, rule_line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Desnormaliza a regra final de um rules_*.log do BIN-NLCEE")
    parser.add_argument("log_path", help="Caminho do rules_*.log já finalizado")
    args = parser.parse_args()

    dataset_id, target_column, rule_line = parse_log(args.log_path)

    data = DataProperties(openml_dataset_id=dataset_id)
    data.load_openml_dataset()
    data.encode_categoricals(target_column=target_column)

    attr_cols = [col for col in data.dataframe.columns if col != target_column]
    col_min, col_max = data.dataframe[attr_cols].min(), data.dataframe[attr_cols].max()

    print(denormalize_rule(rule_line, attr_cols, col_min, col_max, data.categorical_dummy_map))
