---
title: "Empty Column Misinitialization"
disableShare: true
summary:
tags: 
weight: 
# ShowReadingTime: true	
---

### Description

#### Context

#### Problem

#### Solution


### Type


### Existing Stage


### Effect


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

#### GitHub Commit

#### Stack Overflow

#### Documentation

