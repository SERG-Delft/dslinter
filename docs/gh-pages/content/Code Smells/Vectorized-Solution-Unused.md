---
title: "Vectorized Solution Unused"
disableShare: true
# ShowReadingTime: true
tags: ["can be automated", "generic","data preparation","efficiency"]
weight: 3
---

### Description

"Vectorization is the process of converting an algorithm from operating on a single value at a time to operating on a set of values (vector) at one time."\ref{grey:vectorized_blog} ML applications are often data-intensive and need to apply an operation on a dataset. Therefore, it is better to adopt vectorized solution instead of iterating over data. As stated in the Pandas documentation \ref{grey:pandas_vectorized}: ”Iterating through pandas objects is generally slow. In many cases, iterating manually over the rows is not needed and can be avoided”. The built-in methods (e.g., join, groupby) in Pandas are vectorized. Thus, it is recommended to use Pandas built-in methods. Another advantage of using the vectorized solution is that code complexity is reduced, resulting in less prone-to-bugs code\cite{haakman2020studying}.

### Type

Generic

### Existing Stage

Data Preparation

### Effect

Efficiency

### Example

```python

### Pandas
import pandas as pd
df = pd.DataFrame([1, 2, 3])

# Violated Code
result = []
for index, row in df.iterrows():
result.append(row[0] + 1)
result = pd.DataFrame(result)

# Recommended Fix
result = df.add(1)

```

### Source:

#### Paper 
- MPA Haakman. 2020. Studying the Machine Learning Lifecycle and ImprovingCode Quality of Machine Learning Applic

#### Grey Literature

#### GitHub Commit
- https://github.com/tensorflow/models/commit/90f63a1e1653bfa17fde8260a4aa20231b269b7d

#### Stack Overflow

#### Documentation
- https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#iteration

