---
title: "Data Leakage"
disableShare: true
# ShowReadingTime: true
tags: ["can be automated", ""]
weight: 5
---

### Description

"Data Leakage happens when the data you are using to train a machine learning algorithm happens to have the information you are trying to predict."\ref{grey:data_leakage} It results in overly optimistic performance during testing and poor performance in real-world usage. There are two main sources of data leakage: leaky predictors and a leaky validation strategy \ref{grey:data_leakage_kaggle}. Leaky predictors refer to the situation where some features updated or created after the target value is realized are included. This kind of data leakage can only be inspected at the data level rather than the code level. Leaky validation strategy refers to the scene where information from training data is getting mixed with validation data. This kind of pitfall can be avoided by checking the code carefully. One best practice in Scikit-Learn is to use Pipeline API to prevent data leakage.

### Type

Generic

### Existing Stage

Data Preparation

### Effect

Error-prone

### Example

```python

### Scikit-Learn

import numpy as np
from sklearn.feature_selection import SelectPercentile, f_regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
rnd = np.random.RandomState(seed=0)
X = rnd.normal(size=(100, 10000))
y = rnd.normal(size=(100,))

# Violated Code
select = SelectPercentile(score_func=f_regression, percentile=5).fit(X, y)
X_selected = select.transform(X)
accuracy = np.mean(cross_val_score(Ridge(), X_selected, y, cv=5))

# Recommended Fix
select = SelectPercentile(score_func=f_regression, percentile=5)
pipe = Pipeline([("select", select), ("ridge", Ridge())])
accuracy = np.mean(cross_val_score(pipe, X, y, cv=5))

```

### Source:

#### Paper 
- MPA Haakman. 2020. Studying the Machine Learning Lifecycle and ImprovingCode Quality of Machine Learning Applications. (2020).

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/43816718/keras-regression-using-scikit-learn-standardscaler-with-pipeline-and-without-pip/43816833#43816833

#### Documentation
- https://scikit-learn.org/stable/common_pitfalls.html

