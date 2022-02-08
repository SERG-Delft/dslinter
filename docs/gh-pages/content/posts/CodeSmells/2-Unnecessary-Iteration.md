---
title: "Unnecessary Iteration"
disableShare: true
# ShowReadingTime: true
tags: ["generic","data cleaning","efficiency"]
weight: 2
summary: "Avoid unnecessary iterations. Use vectorized solutions instead of loops."
---

### Description

#### Context
Loops are typically time-consuming and verbose, while developers can usually use some vectorized solutions to replace the loops.

#### Problem
As stated in the Pandas documentation: "Iterating through pandas objects is generally slow. In many cases, iterating manually over the rows is not needed and can be avoided". In `EffectiveTensorflow` github repository, it is also stated that the slicing operation with loops in TensorFlow is slow, and there is a substitute for better performance.

#### Solution
Machine learning applications are typically data-intensive, requiring operations on data sets rather than an individual value. Therefore, it is better to adopt a vectorized solution instead of iterating over data. In this way, the program runs faster and code complexity is reduced, resulting in more efficient and less error-prone code. Pandas' built-in methods (e.g., join, groupby) are vectorized. It is therefore recommended to use Pandas built-in methods as an alternative to loops. In TensorFlow, using the `tf.reduce_sum()` API to perform reduction operation is much faster than combining slicing operation and loops.

### Type

Generic

### Existing Stage

Data Cleaning

### Effect

Efficiency

### Example

```diff
### Pandas
import pandas as pd
df = pd.DataFrame([1, 2, 3])
- result = []
- for index, row in df.iterrows():
- 	result.append(row[0] + 1)
- result = pd.DataFrame(result)
+ result = df.add(1)

### TensorFlow 2
import tensorflow as tf
x = tf.random.uniform([500, 10])
- z = tf.zeros([10])
- for i in range(500):
-    z += x[i]
+ z = tf.reduce_sum(x, axis=0)
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

