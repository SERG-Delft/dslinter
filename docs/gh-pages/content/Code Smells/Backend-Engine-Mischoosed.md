---
title: "Backend Engine Mischoosed"
disableShare: true
# ShowReadingTime: true
tags: ["not sure", "api-specific", "data preparation", "efficiency"]
weight: 17
---

### Description

When using `pd.eval()` in Pandas library, the `numexpr` is optimized for performance and `python` options offer no performance benefit over `numexpr`. Generally, it is not recommended to set the parameter to `python`. The developers should be careful when explicitly set this parameter.

### Type

API Specific

### Existing Stage

Data Preparation

### Effect

Efficiency

### Example

```python
### Pandas
import pandas as pd

# Violated Code
pd.eval('df.A.str.contains("ab")', engine='python')

# Recommended Fix
pd.eval('df.A.str.contains("ab")')
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/53779986/dynamically-evaluate-an-expression-from-a-formula-in-pandas/53779987#53779987

#### Documentation

