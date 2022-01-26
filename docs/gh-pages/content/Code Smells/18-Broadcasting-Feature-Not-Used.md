---
title: "Broadcasting Feature Not Used"
disableShare: true
tags: ["api-specific", "model training", "efficiency"]
weight: 18
# ShowReadingTime: true	
summary: "Use the broadcasting feature in TensorFlow 2 to be more memory efficient. "
---

### Description

#### Context

Use the broadcasting feature in TensorFlow 2 to be more memory efficient. 

#### Problem

Without broadcasting, tiling a tensor first to match another tensor consumes more memory due to the creation and storage of a middle tiling operation result.  

#### Solution

With broadcasting, it is more memory efficient. However, there is a trade-off in debugging since the tiling process is not explicitly stated. Therefore, it is suggested to be as explicit as possible in operation to alleviate the debugging problem. For example, specify the dimension in reduction operations and when using `tf.squeeze()`.

### Type

API-Specific

### Existing Stage

Model Training

### Effect

Efficiency

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
- https://github.com/vahidk/EffectiveTensorflow

#### GitHub Commit

#### Stack Overflow

#### Documentation

