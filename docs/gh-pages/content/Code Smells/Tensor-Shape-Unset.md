---
title: "Tensor Shape Unset"
disableShare: true
# ShowReadingTime: true
tags: ["not sure", "api-specific", "data preparation", "error-prone"]
weight: 16
---

### Description
Several bugs can be caused by tensor unaligned. Usually, the unaligned tensor problems cannot be identified at the code level, but we can explicitly control one. It is recommended to explicitly set the shape of the input for `tf.Variable()` to make the tensor aligned. In this way, we can alleviate the unaligned tensor problem.

### Type
API Specific

### Existing Stage
Data Preparation

### Effect
Error-prone

### Example

```python

### TensorFlow
import Tensorflow as tf

# Violated Code
normal_dist = tf.truncated_normal()
w = tf.Variable(nonrmal_dist, name = 'weights')

# Recommended Fix
normal_dist = tf.truncated_normal()
normal_dist.set_shape(32,32)
w = tf.Variable(nonrmal_dist, name = 'weights')

```

### Source:

#### Paper 
- Yuhao Zhang, Yifan Chen, Shing-Chi Cheung, Yingfei Xiong, and Lu Zhang. 2018.An empirical study on TensorFlow program bugs. InProceedings of the 27th ACMSIGSOFT International Symposium on Software Testing and Analysis. 129–140.
- Md Johirul Islam, Giang Nguyen, Rangeet Pan, and Hridesh Rajan. 2019.   Acomprehensive study on deep learning bug characteristics. InProceedings of the2019 27th ACM Joint Meeting on European Software Engineering Conference andSymposium on the Foundations of Software Engineering. 510–520.

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/34079787/tensor-with-unspecified-dimension-in-tensorflow

#### Documentation

