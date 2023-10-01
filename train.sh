#!/usr/bin/env bash

for EPOCHS in 1000, 3000, 5000 10000 30000 50000 100000; do
    echo -e "Training agent with $EPOCHS."
    python -m src.train -n 30 -e $EPOCHS -o "policies/model_mlp_$EPOCHS.json"
done