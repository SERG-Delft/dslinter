---
title: "Empty Column Misinitialization"
disableShare: true
tags: ["api-specific", "data cleaning", "robustness"]
weight: 16
# ShowReadingTime: true	
summary: "When a new empty column is needed in a `DataFrame` in Pandas, use the `NaN` value in Numpy instead of using zeros or empty strings."
---

### Description

#### Context
Developers may need a new empty column in `DataFrame`.

#### Problem
If they use zeros or empty strings to initialize a new empty column in Pandas, the ability to use methods such as `.isnull()` or `.notnull()` is retained.

#### Solution
Use `NaN` value (e.g. `np.nan`) if a new empty column in a `DataFrame` is needed. Do not use "filler values" such as zeros or empty strings.

### Type
API-Specific

### Existing Stage
Data Cleaning

### Effect
Robustness

### Example

```diff
import pandas as pd
+ import numpy as np

df = pd.DataFrame([])
- df['new_col_int'] = 0
- df['new_col_str'] = ''
+ df['new_col_float'] = np.nan
+ df['new_col_int'] = pd.Series(dtype='int')
+ df['new_col_str'] = pd.Series(dtype='object')
```

### Source:

#### Paper 

#### Grey Literature
- https://github.com/joshlk/pandas_style_guide

#### GitHub Commit

#### Stack Overflow

#### Documentation

