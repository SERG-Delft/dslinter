---
title: "Deterministic Algorithm Option Not Used"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "model training", "reproducibility"]
weight: 6
summary: "Set deterministic algorithm option to `True` during the development process, and use the option that provides better performance in the production."
---

### Description

#### Context
Using deterministic algorithms can improve reproducibility.

#### Problem
The non-deterministic algorithm cannot produce repeatable results, which is inconvenient for debugging.

#### Solution
Some libraries provide APIs for developers to use the deterministic algorithm. In PyTorch, it is suggested to set `torch.use_deterministic_algorithms(True)` when debugging. However, the application will perform slower if this option is set, so it is suggested not to use it in the deployment stage. 

### Type
Generic

### Existing Stage
Model Training

### Effect
Reproducibility

### Example

```diff
### PyTorch
import torch
+ torch.use_deterministic_algorithms(True)
```

### Source:

#### Paper 
#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation
- https://pytorch.org/docs/stable/notes/randomness.html

