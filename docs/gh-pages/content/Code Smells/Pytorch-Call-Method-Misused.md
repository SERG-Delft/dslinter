---
title: "Pytorch Call Method Misused"
disableShare: true
# ShowReadingTime: true
tags: 
weight: 21
---

### Description

In PyTorch, \textit{self.nn()} is different than \textit{self.nn.forward()}. \textit{self.nn()} also deals with all the register hooks, which would not be considered when calling the plain \textit{forward} \ref{grey:pytorch_styleguide}. Thus, it is recommended to use \textit{self.nn()} than \textit{self.nn.forward()}. 

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

