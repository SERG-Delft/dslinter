---
title: "No Scaling Before Scaling-sensitive Operation"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "feature engineering", "error-prone"]
weight: 3
summary: "Check whether feature scaling is added before scaling-sensitive operations."
---

### Description

#### Context
Feature scaling is a method of aligning features from various value ranges to the same range.

#### Problem
There are many operations sensitive to feature scaling, including Principal Component Analysis (PCA), Support Vector Machine (SVM), Stochastic Gradient Descent (SGD), Multi-layer Perceptron classifier and L1 and L2 regularization. Missing scaling can lead to a wrong conclusion. For example, if one variable is on a larger scale than another, it will dominate the PCA procedure. Therefore, PCA without feature scaling can produce a wrong principal component result. 

#### Solution
To avoid bugs, whether feature scaling is added before scaling-sensitive operations should be checked.

### Type
Generic

### Existing Stage
Feature Engineering

### Effect
Error-prone

### Example

```diff
### Scikit-Learn PCA
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
+ from sklearn.preprocessing import StandardScaler

# Code source: Tyler Lanigan <tylerlanigan@gmail.com>
#              Sebastian Raschka <mail@sebastianraschka.com>
# License: BSD 3 clause

# Make a train/test split using 30% test size
RANDOM_STATE = 42
features, target = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.30, random_state=RANDOM_STATE
)

# Fit to data and predict using pipeline
- clf = make_pipeline(PCA(n_components=2), GaussianNB())
+ clf = make_pipeline(StandardScaler(), PCA(n_components=2), GaussianNB())
clf.fit(X_train, y_train)
pred_test = clf.predict(X_test)
ac = accuracy_score(y_test, pred_test)


### Scikit-Learn SVC
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
+ from sklearn.pipeline import make_pipeline
+ from sklearn.preprocessing import StandardScaler

# Make a train/test split using 30% test size
RANDOM_STATE = 42
features, target = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.30, random_state=RANDOM_STATE
)

# Fit to data and predict using pipelined GNB and PCA
- clf = SVC()
+ clf = make_pipeline(StandardScaler(), SVC())
clf.fit(X_train, y_train)
pred_test = clf.predict(X_test)
ac = accuracy_score(y_test, pred_test)
```

### Source:

#### Paper 
#### Grey Literature
- https://towardsdatascience.com/my-machine-learning-model-is-perfect-9a7928e0f604
- https://ml.posthaven.com/machine-learning-done-wrong

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/17455302/gridsearchcv-extremely-slow-on-small-dataset-in-scikit-learn/23813876#23813876

#### Documentation
- https://scikit-learn.org/stable/modules/preprocessing.html
- https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html#sphx-glr-download-auto-examples-preprocessing-plot-scaling-importance-py

