---
title: "Memory not Freed"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "model training", "memory issue"]
weight: 9
---

### Description

ML application training is memory-consuming, and thus, it is essential to free memory in time. Some APIs are provided to alleviate the run-out-of-memory issue in deep learning libraries.  TensorFlow's documentation notes that if the model is created in a loop, it is suggested to use `clear\_session()` in the loop. Meanwhile, the GitHub repository "Pytorch best practice" recommends using `.detach()` to detach the tensor whenever possible. We suggest developers check whether they use these APIs to free the memory whenever possible in their code.  

### Type

Generic

### Existing Stage

Model Training

### Effect

Memory Issue

### Example

```diff

### TensorFlow
import tensorflow as tf

# Violated Code
for _ in range(100):
+  tf.keras.backend.clear_session()
   model = tf.keras.Sequential([tf.keras.layers.Dense(10) for _ in range(10)])

```

### Source:

#### Paper 

#### Grey Literature
- https://github.com/IgorSusmelj/pytorch-styleguide

#### GitHub Commit

#### Stack Overflow

#### Documentation
- https://www.tensorflow.org/api_docs/python/tf/keras/backend/clear_session
- https://stackoverflow.com/questions/42495930/tensorflow-oom-on-gpu

