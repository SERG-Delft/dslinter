---
title: "Threshold-Dependent Validation"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "model evaluation", "robustness"]
weight: 10
summary: "Use threshold-independent metrics instead of threshold-dependent ones in model evaluation."
---

### Description

#### Context
The performance of the machine learning model can be measured by different metrics, including threshold-dependent metrics (e.g., F-measure) or threshold-independent metrics (e.g., Area Under the Curve (AUC)).

#### Problem
Choosing a specific threshold is tricky and can lead to a less-interpretable result.

#### Solution
Threshold-independent metrics are more robust and should be preferred over threshold-dependent metrics.

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
- Gopi Krishnan Rajbahadur, Gustavo Ansaldi Oliva, Ahmed E Hassan, and JuergenDingel. 2019. Pitfalls Analyzer: Quality Control for Model-Driven Data SciencePipelines. In2019 ACM/IEEE 22nd International Conference on Model DrivenEngineering Languages and Systems (MODELS). IEEE, 12–22.

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

