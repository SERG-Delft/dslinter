---
title: "Chain Indexing Misused"
disableShare: true
summary: "Avoid using chain indexing in Pandas."
tags: ["api-specific", "data prepaation", "error-prone", "efficiency"]
weight: 13
# ShowReadingTime: true
---

### Description

#### Context
In Pandas, `df["one"]["two"]` and `df.loc[:,("one","two")]` give the same result. `df["one"]["two"]` is called chain indexing.

#### Problem
Using chain indexing may cause performance issues as well as prone-to-bug code. For example, when using `df["one"]["two"]`, Pandas see this operation as two events: call `df["one"]` first and call `["two"]` based on the result the previous operation gets. On the contrary, `df.loc[:,("one","two")]` only perform a single call. In this way, the second approach can be significantly faster than the first one. Furthermore, assigning to the product of chain indexing has inherently unpredictable results. Since Pandas makes no guarantees on whether `df["one"]` will return a view or a copy, the assignment may fail.

#### Solution
Developers using Pandas should avoid using chain indexing.


### Type

API Specific

### Existing Stage

Data Preparation

### Effect

Error-prone & Efficiency

### Example

```diff
### Pandas
import pandas as pd
df = pd.DataFrame([[1,2,3],[4,5,6]])
col = 1
x = 0
- df[col][x] = 42
+ df.loc[x, col] = 42
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/22491628/extrapolate-values-in-pandas-dataframe/35959909#35959909
- https://stackoverflow.com/questions/53806570/why-does-one-use-of-iloc-give-a-settingwithcopywarning-but-the-other-doesnt/53807453#53807453

#### Documentation
- https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-view-versus-copy

