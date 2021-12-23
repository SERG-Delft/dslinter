---
title: "Nan Equality Misused"
disableShare: true
# ShowReadingTime: true
tags: 
weight: 12
---

### Description

While \textit{None} == \textit{None} evaluates to \textit{True}, \textit{numpy.nan} == \textit{numpy.nan} evaluates to \textit{False}. As Pandas treats \textit{None} like \textit{numpy.nan} for simplicity and performance reasons, a comparison of DataFrame elements with \textit{numpy.nan} always return \textit{False} \cite{haakman2020studying}. Therefore, developers need to be careful when using the \textit{NaN} comparision in Numpy and Pandas. Otherwise, it may lead to unintentional behavior in the code.

### Type

API Specific

### Existing Stage

Data Preparation

### Effect

Error-prone

### Example

```python

### Pandas & NumPy
import pandas as pd
import numpy as np
df = pd.DataFrame([1, None, 3])

# Violated Code
df_is_nan = df == np.nan

# Recommended Fix
df_is_nan = df.isna()

```

### Source:

#### Paper 
- MPA Haakman. 2020. Studying the Machine Learning Lifecycle and ImprovingCode Quality of Machine Learning Application. (2020).

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

