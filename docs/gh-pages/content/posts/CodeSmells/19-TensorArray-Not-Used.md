---
title: "TensorArray Not Used"
disableShare: true
tags: ["api-specific", "model training", "efficiency", "error-prone"]
weight: 19
# ShowReadingTime: true	
summary: "Use `tf.TensorArray()` in TensorFlow 2 if the value of the array will change in the loop."
---

### Description

#### Context

Developers may need to change the value of the array in the loops in TensorFlow.

#### Problem

If the developer initializes an array using `tf.constant()` and tries to assign a new value to it in the loop to keep it growing, the code will run into an error. The developer can fix this error by the low-level `tf.while\_loop()` API. However, it is inefficient coding in this way. A lot of intermediate tensors are built in this process.

#### Solution

Using `tf.TensorArray()` for growing array in the loop is a better solution for this kind of problem in TensorFlow 2.

### Type

API-Specific

### Existing Stage

Model Training

### Effect

Efficiency & Error-prone

### Example

```diff
### TensorFlow
import tensorflow as tf
@tf.function
def fibonacci(n):
    a = tf.constant(1)
    b = tf.constant(1)
-    c = tf.constant([1, 1])
+    c = tf.TensorArray(tf.int32, n)
+    c = c.write(0, a)
+    c = c.write(1, b)

    for i in range(2, n):
        a, b = b, a + b
-       c = tf.concat([c, [b]], 0)
+		c = c.write(i, b)
    
-    return c
+	 return c.stack()
    
n = tf.constant(5)
d = fibonacci(n)
```

### Source:

#### Paper 

#### Grey Literature
- https://github.com/vahidk/EffectiveTensorflow

#### GitHub Commit

#### Stack Overflow

#### Documentation

