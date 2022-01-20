---
title: "Missing Regularization"
disableShare: true
# ShowReadingTime: true
tags: ["added","generic", "model training", "efficiency"]
weight: 25
---

### Description

In deep learning, regularization can help control overfitting, speed up the training process by dealing with noise and outliers. Developers should check whether they are able to make use of regularization to improve performance.

### Type

Generic



### Existing Stage

Model Training



### Effect

Efficiency




### Example

```python
### TensorFlow
# Violated Code
layer = tf.keras.layers.Dense(
    5, input_dim=5,
    kernel_initializer='ones',
    kernel_regularizer=tf.keras.regularizers.L1(0.01),
    activity_regularizer=tf.keras.regularizers.L2(0.01))

# Recommended Fix
layer = tf.keras.layers.Dense(
    5, input_dim=5,
    kernel_initializer='ones')

### PyTorch
# Violated Code
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

# Recommended Fix
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-5)
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

