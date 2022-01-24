---
title: "Merge API Parameter Not Explicitly Set"
disableShare: true
summary: " "
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

#### GitHub Commit

#### Stack Overflow

#### Documentation

