---
title: "Threshold Dependent Validation"
disableShare: true
# ShowReadingTime: true
tags: ["added"]
weight: 25
---

### Description

The performance of the machine learning model can be measured by different metrics, including threshold-dependent metrics(e.g., F-measure) or threshold-independent metrics(e.g., Area Under the receiver operating characteristic curve (AUC)). Choosing a specific threshold is tricky and can lead to a less-interpretable result. Therefore, threshold-independent is more robust and should be preferred over threshold-independent metrics. 

### Type

Generic


### Existing Stage

Canndidate Model Evaluation

### Effect

Robustness


### Example

```python
### Scikit-Learn
import sklearn

# Violated Code
sklearn.metrics.f1_score()

# Recommended Fix
sklearn.metrics.auc(fpr, tpr)


### TensorFlow
# Violated Code

# Recommended Fix

```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

