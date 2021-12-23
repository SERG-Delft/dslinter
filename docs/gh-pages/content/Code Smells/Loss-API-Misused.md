---
title: "Loss API Misused"
disableShare: true
# ShowReadingTime: true
tags: 
weight: 
---

### Description

Different loss APIs take different input formats, but the difference is not clarified in some documentations, so it is easy to misuse. For example, in PyTorch, the \textit{NLLLoss} takes the output of \textit{LogSoftmax} as the input. If the input given to \textit{NLLLoss} has not been processed by \textit{LogSoftmax}, it might lead to a wrong result.

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
loss = nn.NLLLoss()
# input is of size N x C = 3 x 5
input = torch.randn(3, 5, requires_grad=True)
# each element in target has to have 0 <= value < C
target = torch.tensor([1, 0, 4])
output = loss(input, target)
output.backward()


# Recommended Fix
m = nn.LogSoftmax(dim=1)
loss = nn.NLLLoss()
# input is of size N x C = 3 x 5
input = torch.randn(3, 5, requires_grad=True)
# each element in target has to have 0 <= value < C
target = torch.tensor([1, 0, 4])
output = loss(m(input), target)
output.backward()


```

### Source:

#### Paper 

#### Grey Literature
- https://medium.com/missinglink-deep-learning-platform/most-common-neural-net-pytorch-mistakes-456560ada037

#### GitHub Commit

#### Stack Overflow

#### Documentation

