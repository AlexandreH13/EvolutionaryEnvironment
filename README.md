# EvolutionaryEnvironment

### Short Description

An evolutionary environment based on Genetic Algorithms (GA), implemented in Python. Its primary goal is to provide a simple and flexible way to use the GA proposed in the paper "Binary or Integer Chromosome: Which Is the Best Structure for Supervised Machine Learning Using Genetic Algorithms?" called Binary Non-Linear Computation Evolutionary Environment (BIN-NLCEE).

### How to run

The main script its the `search.py`. It contains the `Seach` class and the static method `class_search()`. A reminder: each execution of the AG classifiers searches for the best classification rules for one class. Also, the configurations can be set in the `properties.py` script. By default, you should set the parameters as args in terminal. The example bellow run the GA classifier for the blood transfusion dataset:

```bash
python3 search.py -b 8 -d 1464 -bts 0.8 -w 0.6 -p 100 -g 100 -c 1 -t Class
```

Here is the description for each argument:

* -b: Binary size. Number of bits to represent each gene;
* -d: OpenML dataset ID;
* -bts: Batch size. Due to the AGs computation cost, we provide a way to select a batch size;
* -w: Weight threshold;
* -p: Population size;
* -g: Number of generations;
* -c: Name of the class the AG is searching for rules;
* -t: The target column;
* -r (optional): Columns to remove from the dataset.

**Please always check your dataset to see the data formats and existence of null values**.

### Citation

If you use this software in your research, please cite its research as follows:

**BibTex**
```bibtex
@Article{app15052608,
AUTHOR = {Alves, Alexandre Henrick da Silva and Neto, Guilherme Antonio Coelho and Gomes, Matheus de Souza and Santos, Líbia Diniz and Bertarini, Pedro Luiz Lima and do Amaral, Laurence Rodrigues},
TITLE = {Binary or Integer Chromosome: Which Is the Best Structure for Supervised Machine Learning Using Genetic Algorithms?},
JOURNAL = {Applied Sciences},
VOLUME = {15},
YEAR = {2025},
NUMBER = {5},
ARTICLE-NUMBER = {2608},
URL = {https://www.mdpi.com/2076-3417/15/5/2608},
ISSN = {2076-3417},
DOI = {10.3390/app15052608}
}
```

**APA Format**
Alves, A. H. d. S., Neto, G. A. C., Gomes, M. d. S., Santos, L. D., Bertarini, P. L. L., & do Amaral, L. R. (2025). Binary or Integer Chromosome: Which Is the Best Structure for Supervised Machine Learning Using Genetic Algorithms? Applied Sciences, 15(5), 2608. https://doi.org/10.3390/app15052608 