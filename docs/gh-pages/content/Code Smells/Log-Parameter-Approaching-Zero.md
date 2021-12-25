---
title: "Log Parameter Approaching Zero"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "model training", "error-prone"]
weight: 11
---

### Description

Several posts on Stack Overflow talk about the bugs that are not easy to discover caused by the log parameter approaching zero. In this kind of program, the log function variable turns to zero and raises an error during the training process. However, the error's stack trace did not directly point to the line of code that the bug exist. This kind of problem is not easy to debug and might take a long training time to find. Therefore, the developer should check the log parameter and may add a very small number to the log parameter in the code before running it. It will save time and effort if the developer could identify this smell before the code run into errors.

### Type

Generic

### Existing Stage

Model Training

### Effect

Error-prone

### Example

```python

### TensorFlow
import Tensorflow as tf

# Violated Code
cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))

# Recommended Fix
cross_entropy = -tf.reduce_sum(y_*tf.log(tf.clip_by_value(y_conv,1e-10,1.0)))

```

### Source:

#### Paper 
- Nargiz Humbatova, Gunel Jahangirova, Gabriele Bavota, Vincenzo Riccio, AndreaStocco, and Paolo Tonella. 2020. Taxonomy of real faults in deep learning sys-tems. InProceedings of the ACM/IEEE 42nd International Conference on SoftwareEngineering. 1110–1121.
- Yuhao Zhang, Yifan Chen, Shing-Chi Cheung, Yingfei Xiong, and Lu Zhang. 2018.An empirical study on TensorFlow program bugs. InProceedings of the 27th ACMSIGSOFT International Symposium on Software Testing and Analysis. 129–140.

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/33712178/tensorflow-nan-bug
- https://stackoverflow.com/questions/33699174/tensorflows-relugrad-claims-input-is-not-finite
- https://stackoverflow.com/questions/39487825/tensorflow-convolutionary-net-grayscale-vs-black-white-training
- https://stackoverflow.com/questions/35078027/implement-mlp-in-tensorflow

#### Documentation

