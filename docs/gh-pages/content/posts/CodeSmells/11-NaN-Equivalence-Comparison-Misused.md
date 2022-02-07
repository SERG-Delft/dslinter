---
title: "NaN Equivalence Comparison Misused"
disableShare: true
# ShowReadingTime: true
tags: ["api-specific", "data cleaning", "error-prone"]
weight: 11
summary: "Be careful when using the `NaN` equivalence comparison in NumPy and Pandas."
---

### Description

#### Context
`NaN` equivalence comparison in NumPy and Pandas behaves differently from Python `None` equivalence comparison.

#### Problem
While `None` == `None` evaluates to `True`, `np.nan` == `np.nan` evaluates to `False` in NumPy. As Pandas treats `None` like `np.nan` for simplicity and performance reasons, a comparison of `DataFrame` elements with `np.nan` always returns `False`. If the developer is not aware of this, it may lead to unintentional bugs in the code.

#### Solution
Developers need to be careful when using the `NaN` comparison in Numpy and Pandas.

### Type

API-Specific

### Existing Stage

Data Cleaning

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

