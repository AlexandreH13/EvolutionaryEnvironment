"""

@author: Alexandre Alves, Msc.

Script utilitário para gerar a regra de um cromossomo do BIN-NLCEE com os valores reais do dataset.

Recebe o cromossomo (lista de bits, como aparece no rules_*.log) e os nomes das colunas na ordem
de X (todas as colunas usadas pelo AG, sem a target e sem as removidas com -r). ATTR{i} do AG é a
i-ésima coluna dessa lista. O tamanho da representação binária (bin size) é inferido do tamanho
do cromossomo: len = (4*s + 2) * número de colunas.

Os valores do cromossomo estão na escala min-max [0...1] usada pelo AG. Para desnormalizar, é
preciso informar a origem dos min/max de cada coluna (--data, --openml ou --minmax). Sem nenhuma
delas, a regra é impressa com os valores normalizados.

Colunas categóricas codificadas pelo preprocess_categorical.ipynb são traduzidas para conjuntos de
categorias (ex. "A6 in {q, r, cc, x}") quando o JSON de mapeamentos é passado em --mappings.

ATENÇÃO: os min/max só são exatos se o AG rodou com -bts 1.0 (dataset completo). Com batch size
menor, o AG normaliza sobre a amostra, e os limiares desnormalizados podem diferir um pouco.

Uso:
    python3 denormalize_rule.py \\
        --chromosome "[0, 1, 1, 1, 0, ...]" \\
        --columns preg plas pres skin insu mass pedi age \\
        --weight 0.6 --openml 37

    python3 denormalize_rule.py \\
        --chromosome cromossomo.txt \\
        --columns A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 \\
        --data data/preprocessed/credit-approval_29_classx2b.csv \\
        --mappings data/preprocessed/credit-approval_29_classx2b.json
"""

import argparse
import json
import re
from pathlib import Path

from evolve.rules.rules import Rules


def parse_chromosome(text):
    """Converte o texto do cromossomo ("[0, 1, 1, ...]" ou "0 1 1 ...") em lista de bits.
    Se o texto for o caminho de um arquivo existente, lê o cromossomo do arquivo."""

    if Path(text).is_file():
        text = Path(text).read_text(encoding="utf-8")

    bits = [int(x) for x in re.findall(r"\d+", text)]
    if not bits:
        raise ValueError("Nenhum bit encontrado no cromossomo.")
    invalid = sorted(set(bits) - {0, 1})
    if invalid:
        raise ValueError(f"O cromossomo deve conter apenas 0 e 1. Valores inválidos: {invalid}")
    return bits


def infer_bin_size(chromosome_len, num_attr):
    """Inverte a fórmula do tamanho do cromossomo: len = (2 + 4*s) * num_attr."""

    if chromosome_len % num_attr != 0 or (chromosome_len // num_attr - 2) % 4 != 0:
        raise ValueError(
            f"Cromossomo com {chromosome_len} bits não é compatível com {num_attr} colunas "
            f"(esperado (2 + 4*s) * {num_attr}). Verifique a lista de colunas.")
    return (chromosome_len // num_attr - 2) // 4


def decode_chromosome(chromosome, num_attr, weight_threshold):
    """Decodifica o cromossomo em uma lista de condições por atributo, na mesma lógica do AG
    (Rules.map_cromosome_to_rule): cada atributo tem dois intervalos; os ativos (peso >= limiar)
    entram na regra, unidos por OR quando são do mesmo atributo.

    Retorna: lista de (indice_atributo, [(operador, valor_normalizado), ...]).
    """

    bin_size = infer_bin_size(len(chromosome), num_attr)

    weights = Rules.get_decimal_weights(chromosome, bin_size)
    operators = Rules.get_operator(chromosome, bin_size, is_string=True)
    values = Rules.get_decimal_value(chromosome, bin_size)
    active = Rules.get_active_segment(weights, weight_threshold)

    conditions = {}
    for interval in active:
        conditions.setdefault(interval // 2, []).append((operators[interval], values[interval]))

    return sorted(conditions.items())


def denormalize(n, col_min, col_max):
    """Inverso da normalização min-max: valor_real = valor_normalizado * (max - min) + min."""
    return n * (col_max - col_min) + col_min


def normalize(x, col_min, col_max):
    return (x - col_min) / (col_max - col_min)


def format_categorical(col, conds, categories, col_min, col_max, warnings):
    """Traduz as condições de uma coluna categórica codificada (códigos 0..n-1) para o conjunto de
    categorias que satisfazem a condição. A comparação é feita na escala normalizada, igual ao AG.
    Casos degenerados (nenhuma/todas as categorias) são anotados em warnings, fora da string da regra."""

    selected = []
    for code, category in enumerate(categories):
        code_norm = normalize(code, col_min, col_max)
        if any(code_norm >= v if op == ">=" else code_norm < v for op, v in conds):
            selected.append(category)

    if not selected:
        warnings.append(f"{col}: nenhuma categoria satisfaz a condição (a regra nunca classifica)")
    elif len(selected) == len(categories):
        warnings.append(f"{col}: todas as categorias satisfazem a condição (cláusula sempre verdadeira)")
    return f"{col} in {{{', '.join(selected)}}}"


def format_rule(decoded, columns, col_min=None, col_max=None, mappings=None, decimals=2, warnings=None):
    """Monta a string da regra. Sem col_min/col_max, mantém os valores normalizados.
    Se warnings (lista) for passado, recebe avisos sobre cláusulas degeneradas."""

    mappings = mappings or {}
    warnings = warnings if warnings is not None else []
    clauses = []

    for attr_idx, conds in decoded:
        col = columns[attr_idx]

        if col in mappings and col_min is not None:
            clauses.append(f"({format_categorical(col, conds, mappings[col], col_min[col], col_max[col], warnings)})")
            continue

        parts = []
        for op, v in conds:
            value = denormalize(v, col_min[col], col_max[col]) if col_min is not None else v
            parts.append(f"{col} {op} {value:.{decimals}f}" if col_min is not None else f"{col} {op} {value}")
        clauses.append("(" + " OR ".join(parts) + ")")

    if not clauses:
        warnings.append("nenhum intervalo ativo: a regra não classifica nenhum registro")
        return "IF <vazio>"
    return "IF " + " AND ".join(clauses)


def load_min_max(columns, data_path=None, openml_id=None, minmax_path=None):
    """Obtém min/max das colunas a partir de um CSV, de um dataset do OpenML ou de um JSON
    no formato {"coluna": [min, max], ...}. Retorna (col_min, col_max) como dicionários."""

    if minmax_path:
        raw = json.loads(Path(minmax_path).read_text(encoding="utf-8"))
        missing = [c for c in columns if c not in raw]
        if missing:
            raise ValueError(f"Colunas sem min/max em {minmax_path}: {missing}")
        return ({c: raw[c][0] for c in columns}, {c: raw[c][1] for c in columns})

    if data_path:
        import pandas as pd
        df = pd.read_csv(data_path)
    else:
        import openml
        df = openml.datasets.get_dataset(openml_id).get_data(dataset_format="dataframe")[0]

    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas inexistentes no dataset: {missing}. Colunas disponíveis: {list(df.columns)}")

    non_numeric = [c for c in columns if df[c].dtype.kind not in "biuf"]
    if non_numeric:
        raise ValueError(
            f"Colunas não numéricas: {non_numeric}. Use o CSV gerado pelo preprocess_categorical.ipynb "
            "(com --mappings) para datasets com atributos categóricos.")

    return (df[columns].min().to_dict(), df[columns].max().to_dict())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera a regra (com valores reais) de um cromossomo do BIN-NLCEE")
    parser.add_argument("--chromosome", required=True,
                        help='Cromossomo: "[0, 1, 1, ...]" ou caminho de um arquivo contendo a lista')
    parser.add_argument("--columns", required=True, nargs="+",
                        help="Nomes das colunas na ordem de X (sem a target e sem as removidas com -r)")
    parser.add_argument("--weight", type=float, default=0.6,
                        help="WEIGHT_THRESHOLD usado na execução do AG (padrão: 0.6)")

    source = parser.add_mutually_exclusive_group()
    source.add_argument("--data", help="CSV de onde calcular os min/max das colunas")
    source.add_argument("--openml", type=int, help="ID do dataset no OpenML de onde calcular os min/max")
    source.add_argument("--minmax", help='JSON com {"coluna": [min, max], ...}')

    parser.add_argument("--mappings",
                        help="JSON gerado pelo preprocess_categorical.ipynb (traduz códigos em categorias)")
    parser.add_argument("--decimals", type=int, default=2, help="Casas decimais dos valores reais (padrão: 2)")
    parser.add_argument("--show-normalized", action="store_true",
                        help="Também imprime a regra com os valores normalizados (útil para conferir com o log)")
    args = parser.parse_args()

    chromosome = parse_chromosome(args.chromosome)
    decoded = decode_chromosome(chromosome, len(args.columns), args.weight)

    mappings = None
    if args.mappings:
        mappings = json.loads(Path(args.mappings).read_text(encoding="utf-8"))["mappings"]

    has_source = args.data or args.openml is not None or args.minmax
    if args.mappings and not has_source:
        parser.error("--mappings precisa de uma origem de min/max (--data, --openml ou --minmax).")

    warnings = []

    if args.show_normalized or not has_source:
        print("Regra (normalizada):")
        print(format_rule(decoded, args.columns, warnings=warnings if not has_source else None))

    if has_source:
        col_min, col_max = load_min_max(args.columns, args.data, args.openml, args.minmax)
        if args.show_normalized:
            print()
        print("Regra (valores reais):")
        print(format_rule(decoded, args.columns, col_min, col_max, mappings, args.decimals, warnings))
    else:
        warnings.append("nenhuma origem de min/max (--data, --openml ou --minmax); valores mantidos na escala [0, 1]")

    for w in warnings:
        print(f"AVISO: {w}")
