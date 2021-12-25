---
title: "Excessive Hyperparameter"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "model training", "error-prone"]
weight: 7
---

### Description

Excessive hyperparameter precision is a potential risk for overtuning. Overtuning occurs if an overly high precision hyperparameter value allows the model to perform particularly well while values in close range of it do not. Further, the choice of such a hyperparameter might be uninterpretable to users, which leads to an untrustworthy result.

### Type

Generic

### Existing Stage

Model Training

### Effect

Error-prone

### Example

```python

### Scikit-Learn
from sklearn.naive_bayes import MultinomialN

# Violated Code
mnb = MultinomialNB(alpha = 0.1001)

# Recommended Fix
mnb = MultinomialNB(alpha = 0.1)

```

### Source:

#### Paper 

#### Grey Literature
- https://towardsdatascience.com/my-machine-learning-model-is-perfect-9a7928e0f604

#### GitHub Commit

#### Stack Overflow

#### Documentation

