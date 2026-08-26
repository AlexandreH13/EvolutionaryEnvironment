### Busca por regras de classificação usando Algoritmos Genéticos

---

**CEE**

Regras lineares de classificação:

``IF(ATTR1 >= X) AND (ATTR2 < Y)``.

Cada gene é o antecedente de um atributo.

---

**NLCEE**

Regras não-lineares de classificação, permitindo a representação de dois intervalos de um mesmo atributo usando o operador lógico **OR**:

``IF(ATTR1 >= X OR ATTR1 < Y) AND (ATTR2 < Y)``

A mutação e o crossover pode gerar regras inválidas com antecedentes como ``IF(ATTR1 >= X AND ATTR1 >= Y)``, mas espera-se que a pressão evolutiva descarte essas regras, uma vez que podem ter fitness inferior.