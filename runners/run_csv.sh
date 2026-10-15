#!/bin/bash

# Runner genérico para datasets em CSV (ex. gerados pelo preprocess_categorical.ipynb).
# Executa o AG para uma classe, com 50 seeds, seguindo o protocolo do EXPERIMENTOS.md (Seção 1.1).
#
# Uso:
#   runners/run_csv.sh <csv> <classe> <coluna_target> [bin_size]
#
# Exemplos (credit-approval, problema binário: o mesmo CSV serve para as duas classes):
#   runners/run_csv.sh data/preprocessed/credit-approval_29_classx2b.csv "+" class
#   runners/run_csv.sh data/preprocessed/credit-approval_29_classx2b.csv "-" class
#   runners/run_csv.sh data/preprocessed/1461/bank-marketing_1461_class1.csv "1" Class
#   runners/run_csv.sh data/preprocessed/179/adult_179_classx3cx3d50K.csv "<=50K" class
#
# O caminho do CSV é relativo à raiz "EvolutionaryEnvironment" (ou absoluto).
# Ative o venv "experimentos" antes de rodar (o script usa o python3 do terminal).

if [ "$#" -lt 3 ]; then
    echo "Uso: $0 <csv> <classe> <coluna_target> [bin_size]"
    exit 1
fi

# Runs from the folder root "EvolutionaryEnvironment"
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

CSV=$1
CLASS=$2
TARGET=$3
BIN=${4:-8} # Bin size é o quarto parâmetro ou 8 por padrão

if [ ! -f "$CSV" ]; then
    echo "Arquivo não encontrado: $CSV (caminho relativo à raiz EvolutionaryEnvironment)"
    exit 1
fi

# 50 seeds
SEEDS=$(seq 1 50)

# GA config
CONFIG=1

for SEED in $SEEDS
do

    echo "=========================================="
    echo "Dataset: $CSV"
    echo "Classe: $CLASS"
    echo "Configuração: $CONFIG"
    echo "Seed: $SEED"
    echo "=========================================="

    python3 search.py \
        -b "$BIN" \
        -f "$CSV" \
        -bts 1 \
        -w 0.6 \
        -p 100 \
        -g 100 \
        -c "$CLASS" \
        -t "$TARGET" \
        -s "$SEED" \
        -cf "$CONFIG"

done
