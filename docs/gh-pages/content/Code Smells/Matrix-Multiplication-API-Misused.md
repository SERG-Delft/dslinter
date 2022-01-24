---
title: "Matrix Multiplication API Misused"
disableShare: true
# ShowReadingTime: true
tags: ["not sure", "api-specific", "model training", "readability"]
weight: 19
---

### Description

`np.matmul()` in Numpy library is more readable than `np.dot()` in the semantic way. While`np.dot()` provides heterogeneous behaviors depending on the shape of the data, `np.matmul()` behaves in a consistent way. When the multiply operation is performed on two-dimension matrixes, two APIs give a same result. However, `np.matmul()` is preferred than `np.dot()` for its clear semantic.

### Type

API Specific

### Existing Stage

Model Training

### Effect

Readability

### Example

```diff
### NumPy
import numpy as np
a = [[1, 0], [0, 1]]
b = [[4, 1], [2, 2]]
- np.dot(a, b)
+ np.matmul(a, b)
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/54160155/does-np-dot-automatically-transpose-vectors/54161169#54161169

#### Documentation
- https://numpy.org/doc/stable/reference/generated/numpy.dot.html#numpy.dot

