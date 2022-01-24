---
title: "TensorArray Not Used"
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

#### GitHub Commit

#### Stack Overflow

#### Documentation

