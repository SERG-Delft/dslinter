---
title: "Backend Engine Mischoosed"
disableShare: true
# ShowReadingTime: true
tags: ["not sure"]
weight: 17
---

### Description

As noted in \ref{grey:so_backend}, when using \textit{pd.eval()} in Pandas library, the "\textit{numexpr}" is optimized for performance and "\textit{python}" options offer no performance benefit over "\textit{numexpr}". Generally, it is not recommended to set the parameter to "\textit{python}". The developers should be careful when explicitly set this parameter.

### Type

API Specific

### Existing Stage

Data Preparation

### Effect

Efficiency

### Example

```python
# Violated Code

# Recommended Fix

```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/53779986/dynamically-evaluate-an-expression-from-a-formula-in-pandas/53779987#53779987

#### Documentation

