---
title: "Broadcasting Feature Not Used"
disableShare: true
summary:
tags: 
weight: 
# ShowReadingTime: true	
---

### Description

#### Context

#### Problem

#### Solution


### Type


### Existing Stage


### Effect


### Example

```diff
### TensorFlow example 1
import tensorflow as tf
a = tf.constant([[1., 2.], [3., 4.]])
b = tf.constant([[1.], [2.]])
- c = a + tf.tile(b, [1, 2])
+ c = a + b

### TensorFlow example 2
import tensorflow as tf
a = tf.random.uniform([5, 3, 5])
b = tf.random.uniform([5, 1, 6])
- tiled_b = tf.tile(b, [1, 3, 1])
- c = tf.concat([a, tiled_b], 2)
- d = tf.keras.layers.Dense(10, activation=tf.nn.relu).apply(c)
+ pa = tf.keras.layers.Dense(10).apply(a)
+ pb = tf.keras.layers.Dense(10).apply(b)
+ d = tf.nn.relu(pa + pb)
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

