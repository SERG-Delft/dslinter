---
title: "Nan Equality Misused"
disableShare: true
# ShowReadingTime: true
tags: ["api-specific", "data preparation", "error-prone"]
weight: 12
---

### Description

While `None` == `None` evaluates to `True`, `numpy.nan` == `numpy.nan` evaluates to `False`. As Pandas treats `None` like `numpy.nan` for simplicity and performance reasons, a comparison of DataFrame elements with `numpy.nan` always return `False` . Therefore, developers need to be careful when using the `NaN` comparision in Numpy and Pandas. Otherwise, it may lead to unintentional behavior in the code.

### Type

API Specific

### Existing Stage

Data Preparation

### Effect

Error-prone

### Example

```diff
### Pandas & NumPy
import pandas as pd
- import numpy as np

df = pd.DataFrame([1, None, 3])
- df_is_nan = df == np.nan
+ df_is_nan = df.isna()
```

### Source:

#### Paper 
- MPA Haakman. 2020. Studying the Machine Learning Lifecycle and ImprovingCode Quality of Machine Learning Application. (2020).

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

