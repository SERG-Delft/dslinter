---
title: "Chain Indexing Misused"
disableShare: true
# ShowReadingTime: true
tags: 
weight: 13
---

### Description

Chaining indexing in Pandas is considered a bad practice and should be avoided. Using chain indexing might cause performance issues as well as prone-to-bug code. For example, when using `df["one"]["two"]`, Pandas see this operation as two events: call `df["one"]` first and call `["two"]` based on the result the previous operation gets. On the contrary, `df.loc[:,("one","two")]` only perform a single call. In this way, the second method can be significantly faster than the first one. Furthermore, assigning to the product of chain indexing has inherently unpredictable results. Since Pandas makes no guarantees on whether `df["one"]` will return a view or a copy, the assignment might fail. Therefore, developers using Pandas should check this indexing problem carefully.

### Type

API Specific

### Existing Stage

Data Preparation

### Effect

Error-prone & Efficiency

### Example

```python

### Pandas
# Violated Code
df[col][x] = 42

# Recommended Fix
df.loc[x, col] = 42

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

