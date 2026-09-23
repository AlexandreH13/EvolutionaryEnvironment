#!/bin/bash

# Runs from the folder root "EvolutionaryEnvironment"
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1

# 50 seeds
SEEDS=(1 2 3 4 5 6 7 8 9 10 
       11 12 13 14 15 16 17 18 19 20
       21 22 23 24 25 26 27 28 29 30
       31 32 33 34 35 36 37 38 39 40
       41 42 43 44 45 46 47 48 49 50)

# GA configs
for CONFIG in 1
do

    for SEED in "${SEEDS[@]}"
    do

        echo "=========================================="
        echo "Configuração: $CONFIG"
        echo "Seed: $SEED"
        echo "=========================================="

        if [ "$CONFIG" -eq 1 ]; then

            python3 search.py \
                -b 8 \
                -d 15 \
                -bts 1 \
                -w 0.6 \
                -p 100 \
                -g 100 \
                -c "benign" \
                -t Class \
                -s $SEED\
                -cf $CONFIG

        elif [ "$CONFIG" -eq 2 ]; then

            python3 search.py \
                -b 8 \
                -d 15 \
                -bts 1 \
                -w 0.6 \
                -p 100 \
                -g 100 \
                -c "benign" \
                -t Class \
                -s $SEED\
                -cf $CONFIG

        elif [ "$CONFIG" -eq 3 ]; then

            python3 search.py \
                -b 10 \
                -d 15 \
                -bts 1 \
                -w 0.6 \
                -p 100 \
                -g 100 \
                -c "benign" \
                -t Class \
                -s $SEED\
                -cf $CONFIG

        elif [ "$CONFIG" -eq 4 ]; then

            python3 search.py \
                -b 12 \
                -d 15 \
                -bts 1 \
                -w 0.6 \
                -p 100 \
                -g 100 \
                -c "benign" \
                -t Class \
                -s $SEED\
                -cf $CONFIG

        fi

    done

done