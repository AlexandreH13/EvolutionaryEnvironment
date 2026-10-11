## Runners

Each dataset folder has a bash script for each one of the classes. The script executes the GA classifier to mine the classification rules.

The "california housing" (43939) is a regression dataset. It needs to transform the labels into categorical values.

### OpenML datasets

The scripts inside `dataset<id>/` load the dataset directly from OpenML (`search.py -d <id>`). They only work for datasets whose attributes are all numeric, since the GA only represents interval conditions (`>=`, `<`).

### CSV datasets (`run_csv.sh`)

Datasets with categorical attributes must be preprocessed first with `preprocess_categorical.ipynb`, which saves a CSV in `data/preprocessed/`. The generic runner `run_csv.sh` runs the GA over that CSV (`search.py -f <csv>`) for one class, with seeds 1 to 50 and the configuration from `../../EXPERIMENTOS.md` (Section 1.1): `-bts 1 -w 0.6 -p 100 -g 100 -cf 1`.

```bash
runners/run_csv.sh <csv> <class> <target_column> [bin_size]
```

- `<csv>`: path relative to the `EvolutionaryEnvironment` root (or absolute).
- `<class>`: class to be mined (one-vs-all).
- `<target_column>`: name of the target column in the CSV.
- `[bin_size]`: optional, default `8`.

Example (credit approval):

```bash
runners/run_csv.sh data/preprocessed/credit-approval_29_classx2b.csv "+" class
runners/run_csv.sh data/preprocessed/credit-approval_29_classx2b.csv "-" class
```

Notes:

- In binary problems, the same CSV is used for both classes: the category ordering for the other class is just the reverse, and the GA has both `>=` and `<`. In multiclass problems, generate one CSV per class in the notebook (`TARGET_CLASS`).
- Logs are saved in `data/experiments/` and named after the CSV file, e.g. `rules_datasetcredit-approval_29_classx2b_class+_seed1_config1.log`.
- The script uses the `python3` from the terminal: activate the `experimentos` venv before running it.
