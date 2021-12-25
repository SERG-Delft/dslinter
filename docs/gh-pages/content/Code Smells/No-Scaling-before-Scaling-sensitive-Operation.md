---
title: "No Scaling Before Scaling Sensitive Operation"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "data preparation", "efficiency"]
weight: 4
---

### Description

Principle Component Analysis (PCA) is used for finding the components that maximize the data's variation and reduce its dimensions, which is an essential data processing method. Scaling is pretty crucial to PCA because of the way the principal components are calculated. If one variable is on a larger scale than another, it will dominate the PCA procedure. Similarly, there are some other scaling-sensitive operations. Support Vector Machine (SVM), Stochastic Gradient Descent (SGD), Multi-layer Perceptron classifier, L1 and L2 regularization are all sensitive to feature scaling. To avoid bugs, whether feature scaling is added before these operations should be checked.

### Type
Generic

### Existing Stage
Data Preparation

### Effect
Efficiency

### Example

```python

### Scikit-Learn PCA
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.naive_bayes import Gaussia

# Violated Code
clf = make_pipeline(PCA(n_components=2),GaussianNB())

# Recommended Fix
from sklearn.preprocessing import StandardSca
clf = make_pipeline(StandardScaler(),PCA(n_components=2), GaussianNB())

### Scikit-Learn SVC
from sklearn.svm import SVC

# Violated Code
clf = SVC()

# Recommended Fix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
clf = make_pipeline(StandardScaler(), SVC())
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

