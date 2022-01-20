---
title: "Threshold Dependent Validation"
disableShare: true
# ShowReadingTime: true
tags: ["added", "generic", "model evaluation", "robustness"]
weight: 25
---

### Description

The performance of the machine learning model can be measured by different metrics, including threshold-dependent metrics(e.g., F-measure) or threshold-independent metrics(e.g., Area Under the receiver operating characteristic curve (AUC)). Choosing a specific threshold is tricky and can lead to a less-interpretable result. Therefore, threshold-independent is more robust and should be preferred over threshold-independent metrics. 

### Type

Generic


### Existing Stage

Model Evaluation

### Effect

Robustness


### Example

```diff
### Scikit-Learn
from sklearn import metrics
y_true = [0, 1, 2, 0, 1, 2]
y_pred = [0, 2, 1, 0, 0, 1]
metrics.f1_score(y_true, y_pred, average='weighted')

+ y = [1, 1, 2, 2]
+ pred = [0.1, 0.4, 0.35, 0.8]
+ fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=2)
+ print(metrics.auc(fpr, tpr))
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

