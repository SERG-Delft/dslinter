---
title: "Zero_grad Not Used Before Backward"
disableShare: true
# ShowReadingTime: true
tags: 
weight: 23
---

### Description

Developers should use \textit{optimizer.zero\_grad()}, \textit{loss\_fn.backward()}, \textit{optimizer.step()} together and should be forget to use \textit{optimizer.zero\_grad()} before \textit{loss\_fn.backward()}. \textit{optimizer.zero\_grad()} clears the old gradients from last step. If this API is not used, the gradients will be accumulated from all \textit{loss.backward()} calls and it will lead to the gradient explosion, which fails the training.

### Type

API Specific

### Existing Stage

Model Training

### Effect

Error-prone

### Example

```python

### PyTorch

# Violated Code
output = model(input) # forward-pass
loss_fn.backward()    # backward-pass
optimizer.step()      # update weights by an ever growing gradient 


# Recommended Fix

output = model(input) # forward-pass
optimizer.zero_grad() # reset gradient 
loss_fn.backward()    # backward-pass
optimizer.step()      # weight updates using reasonable gradients 


```

### Source:

#### Paper 

#### Grey Literature
- https://medium.com/missinglink-deep-learning-platform/most-common-neural-net-pytorch-mistakes-456560ada037

#### GitHub Commit

#### Stack Overflow

#### Documentation

