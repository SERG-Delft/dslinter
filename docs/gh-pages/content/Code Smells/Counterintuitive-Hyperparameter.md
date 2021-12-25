---
title: "Counterintuitive Hyperparameter"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "model training", "error-prone"]
weight: 8
---

### Description

Counterintuitive hyperparameters will also cause bugs. There are four posts on StackOverflow discussing where the bug in the program is, and it turns out that a large learning rate causes bugs. This implies that the developer should check whether the hyperparameters stay in the normal range when developing ML applications.  


### Type

Generic

### Existing Stage

Model Training

### Effect

Error-prone

### Example

```python

# TensorFlow
import tensorflow as tf

# Violated Code
optimizer = tf.train.GradientDescentOptimizer(0.01)

# Recommended Fix
optimizer = tf.train.GradientDescentOptimizer(0.001)

```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/33641799/why-does-tensorflow-example-fail-when-increasing-batch-size
- https://stackoverflow.com/questions/43636736/tensorflow-weights-diverge-or-nan
- https://stackoverflow.com/questions/43948571/tensorflow-loss-becomes-nan
- https://stackoverflow.com/questions/46577203/tensorflow-issues

#### Documentation

