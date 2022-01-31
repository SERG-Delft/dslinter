---
title: "Memory not Freed"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "model training", "memory issue"]
weight: 5
summary: "Free memory in time."
---

### Description

#### Context
Machine learning training is memory-consuming, and the machine's memory is always limited by budget.

#### Problem
If the machine runs out of memory while training the model, the training will fail.

#### Solution
Some APIs are provided to alleviate the run-out-of-memory issue in deep learning libraries. TensorFlow's documentation notes that if the model is created in a loop, it is suggested to use `clear\_session()` in the loop. Meanwhile, the GitHub repository `pytorch-styleguide` recommends using `.detach()` to free the tensor from the graph whenever possible. The `.detach()` API can prevent unnecessary operations from being recorded and therefore can save memory. Developers should check whether they use this kind of APIs to free the memory whenever possible in their code. 

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

