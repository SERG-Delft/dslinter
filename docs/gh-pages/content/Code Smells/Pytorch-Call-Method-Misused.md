---
title: "Pytorch Call Method Misused"
disableShare: true
# ShowReadingTime: true
tags: ["api-specific", "modeling training", "robustness"]
weight: 21
---

### Description

In PyTorch, `self.nn()` is different than `self.nn.forward()`. `self.nn()` also deals with all the register hooks, which would not be considered when calling the plain `forward`. Thus, it is recommended to use `self.nn()` than `self.nn.forward()`. 

### Type

API Specific

### Existing Stage

Model Training

### Effect

Robustness

### Example

```python

### PyTorch

# Violated Code
output = self.net.forward(input)

# Recommended Fix
output = self.net(input)

```

### Source:

#### Paper 

#### Grey Literature
- https://github.com/IgorSusmelj/pytorch-styleguide

#### GitHub Commit

#### Stack Overflow

#### Documentation

