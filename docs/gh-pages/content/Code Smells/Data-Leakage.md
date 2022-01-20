---
title: "Data Leakage"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "data preparation", "error-prone"]
weight: 5
---

### Description

"Data Leakage happens when the data you are using to train a machine learning algorithm happens to have the information you are trying to predict." It results in overly optimistic performance during testing and poor performance in real-world usage. There are two main sources of data leakage: leaky predictors and a leaky validation strategy. Leaky predictors refer to the situation where some features updated or created after the target value is realized are included. This kind of data leakage can only be inspected at the data level rather than the code level. Leaky validation strategy refers to the scene where information from training data is getting mixed with validation data. This kind of pitfall can be avoided by checking the code carefully. One best practice in Scikit-Learn is to use Pipeline API to prevent data leakage.

### Type

Generic

### Existing Stage

Data Preparation

### Effect

Error-prone

### Example

```diff
### Scikit-Learn
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import numpy as np
+ from sklearn.pipeline import make_pipeline

n_samples, n_features, n_classes = 200, 10000, 2
rng = np.random.RandomState(42)
X = rng.standard_normal((n_samples, n_features))
y = rng.choice(n_classes, n_samples)

- X_selected = SelectKBest(k=25).fit_transform(X, y)
- X_train, X_test, y_train, y_test = train_test_split(X_selected, y, random_state=42)
- gbc = GradientBoostingClassifier(random_state=1)
- gbc.fit(X_train, y_train)
- y_pred = gbc.predict(X_test)
+ X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
+ pipeline = make_pipeline(SelectKBest(k=25), GradientBoostingClassifier(random_state=1))
+ pipeline.fit(X_train, y_train)
+ y_pred = pipeline.predict(X_test)

accuracy_score(y_test, y_pred)
```

### Source:

#### Paper 
- MPA Haakman. 2020. Studying the Machine Learning Lifecycle and Improving Code Quality of Machine Learning Applications. (2020).

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/43816718/keras-regression-using-scikit-learn-standardscaler-with-pipeline-and-without-pip/43816833#43816833

#### Documentation
- https://scikit-learn.org/stable/common_pitfalls.html

