---
title: "Matrix Multiplication API Misused"
disableShare: true
# ShowReadingTime: true
tags: ["api-specific", "data cleaning", "readability"]
weight: 14
summary: "When the multiply operation is performed on two-dimensional matrixes, use `np.matmul()` instead of `np.dot()` in NumPy for better semantics. "
---

### Description

#### Context
 When the multiply operation is performed on two-dimensional matrixes, `np.matmul()` and `np.dot()` give the same result, which is a matrix.

#### Problem
In mathematics, the result of the dot product is expected to be a scalar rather than a vector. The `np.dot()` returns a new matrix for two-dimensional matrixes multiplication, which does not match with its mathematics semantics. Developers sometimes use `np.dot()` in scenarios where it is not supposed to, e.g., two-dimensional multiplication.

#### Solution
 When the multiply operation is performed on two-dimensional matrixes, `np.matmul()` is preferred over `np.dot()` for its clear semantic.

### Type

API-Specific

### Existing Stage

Data Cleaning

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

