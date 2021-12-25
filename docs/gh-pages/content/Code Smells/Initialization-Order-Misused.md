---
title: "Initialization Order Misused"
disableShare: true
# ShowReadingTime: true
tags: ["api-specific", "model training", "error-prone"]
weight: 20
---

### Description

The `AdamOptimizer` class in the TensorFlow creates additional variables named "slots". The variables must be initialized before training the model. Therefore, if the developer call `initialize_all_variables()` before calling `AdamOptimizer` and does not call the initializer afterward, the variables created by `AdamOptimizer` will not be initialized and might cause an error.

### Type

API Specific

### Existing Stage

Model Training

### Effect

Error-prone

### Example

```python
### TensorFlow
import tensorflow as tf

# Violated Code
init = tf.global_variables_initializer()
train_op = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
sess = tf.Session()
sess.run(init)

# Recommended Fix
train_op = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

```

### Source:

#### Paper 
- Yuhao Zhang, Yifan Chen, Shing-Chi Cheung, Yingfei Xiong, and Lu Zhang. 2018.An empirical study on TensorFlow program bugs. InProceedings of the 27th ACMSIGSOFT International Symposium on Software Testing and Analysis. 129–140.

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/33788989/tensorflow-using-adam-optimizer

#### Documentation

