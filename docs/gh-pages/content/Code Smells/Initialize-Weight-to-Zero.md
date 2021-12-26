---
title: "Initialize Weight to a Constant"
disableShare: true
# ShowReadingTime: true
tags: ["added","generic","model training","error-prone"]
weight: 25
---

### Description

In neural network, if all the weights are initialized to a constant, i.e., all the neurons starts with the same weight, all the neurons will follow the same gradient during the backward propagation update. As a result, neurons will learn same features in each iterations. In this way, the nueral netwok will provide a poor result.

### Type

Generic



### Existing Stage

Model Training



### Effect

Error-prone




### Example

```python
# Violated Code
# Use PyTorch's defaault init or initialize to 0
def conv(ni, nf, ks=3, stride=1, padding=1, **kwargs):
    _conv = nn.Conv2d(ni, nf, kernel_size=ks,stride=stride,padding=padding, **kwargs)
    # no initialization
    return _conv
  
# Recommended Fix
def conv(ni, nf, ks=3, stride=1, padding=1, **kwargs):
    _conv = nn.Conv2d(ni, nf, kernel_size=ks,stride=stride,padding=padding, **kwargs)
    nn.init.kaiming_normal_(_conv.weight)
    return _conv
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

