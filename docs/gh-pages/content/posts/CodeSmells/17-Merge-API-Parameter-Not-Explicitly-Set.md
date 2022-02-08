---
title: "Merge API Parameter Not Explicitly Set"
disableShare: true
tags: ["api-specific", "data cleaning", "readability", "error-prone"]
weight: 17
# ShowReadingTime: true	
summary: "Explicitly specify `on`, `how` and `validate` parameter for `df.merge()` API in Pandas for better readability."
---

### Description

#### Context
`df.merge()` API merges two `DataFrame`s in Pandas. 

#### Problem
Although using the default parameter can produce the same result, explicitly specify `on` and `how` produce better readability. The parameter `on` states which columns to join on, and the parameter `how` describes the join method (e.g., outer, inner). Also, the `validate` parameter will check whether the merge is of a specified type. If the developer assumes the merge keys are unique in both left and right datasets, but that is not the case, and he does not specify this parameter, the result might silently go wrong. The merge operation is usually computationally and memory expensive. It is preferable to do the merging process in one stroke for performance consideration.

#### Solution
Developers should explicitly specify `on`, `how` and `validate` parameters for `df.merge()` API for better readability. 

### Type

API-Specific

### Existing Stage

Data Cleaning

### Effect

Readability & Error-prone

### Example

```diff
import pandas as pd
df1 = pd.DataFrame({'key': ['foo', 'bar', 'baz', 'foo'],
                    'value': [1, 2, 3, 5]})
df2 = pd.DataFrame({'key': ['foo', 'bar', 'baz', 'foo'],
                    'value': [5, 6, 7, 8]})                  
- df3 = df1.merge(df2)
+ df3 = df1.merge(
+    df2,
+    how='inner',
+   on='key',
+   validate='m:m'
+ )
```

### Source:

#### Paper 

#### Grey Literature
- https://github.com/joshlk/pandas_style_guide

#### GitHub Commit

#### Stack Overflow

#### Documentation

