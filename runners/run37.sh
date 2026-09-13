#!/bin/bash

# Runs from the folder root "EvolutionaryEnvironment"
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

# 20 seeds
SEEDS=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20)

# GA configs
for CONFIG in 1 2 3 4
do

    for SEED in "${SEEDS[@]}"
    do

        echo "=========================================="
        echo "Configuração: $CONFIG"
        echo "Seed: $SEED"
        echo "=========================================="

        if [ "$CONFIG" -eq 1 ]; then

            python3 search.py \
                -b 6 \
                -d 37 \
                -bts 1 \
                -w 0.6 \
                -p 100 \
                -g 100 \
                -c "tested_positive" \
                -t class\
                -s $SEED\
                -cf $CONFIG

        elif [ "$CONFIG" -eq 2 ]; then

            python3 search.py \
                -b 8 \
                -d 37 \
                -bts 1 \
                -w 0.6 \
                -p 100 \
                -g 100 \
                -c "tested_positive" \
                -t class\
                -s $SEED\
                -cf $CONFIG

        elif [ "$CONFIG" -eq 3 ]; then

            python3 search.py \
                -b 10 \
                -d 37 \
                -bts 1 \
                -w 0.6 \
                -p 100 \
                -g 100 \
                -c "tested_positive" \
                -t class\
                -s $SEED\
                -cf $CONFIG

        elif [ "$CONFIG" -eq 4 ]; then

            python3 search.py \
                -b 12 \
                -d 37 \
                -bts 1 \
                -w 0.6 \
                -p 100 \
                -g 100 \
                -c "tested_positive" \
                -t class\
                -s $SEED\
                -cf $CONFIG

        fi

    done

done