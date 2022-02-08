---
title: "Randomness Uncontrolled"
disableShare: true
# ShowReadingTime: true
tags: ["generic","model training","model evaluation","reproducibility"]
weight: 8
summary: "Set random seed explicitly during the development process whenever a possible random procedure is involved in the application."
---

### Description

#### Context
There are several scenarios involving random seeds. In some algorithms, randomness is inherently involved in the training process. For the cross-validation process in the model evaluation stage, the dataset split by some library APIs can vary depending on random seeds.

#### Problem
If the random seed is not set, the result will be irreproducible, which increases the debugging effort. In addition, it will be difficult to replicate the study based on the previous one. For example, in Scikit-Learn, if the random seed is not set, the random forest algorithm may provide a different result every time it runs, and the dataset split by cross-validation splitter will also be different in the next run. 

#### Solution
It is recommended to set global random seed first for reproducible results in Scikit-Learn, Pytorch, Numpy and other libraries where a random seed is involved. Specifically, `DataLoader` in PyTorch needs to be set with a random seed to ensure the data is split and loaded in the same way every time running the code. 

### Type

Generic

### Existing Stage

Model Training & Model Evaluation

### Effect

Reproducibility

### Example

```diff
### python in general
import random
+ random.seed(0)

### Tensorflow
import tensoflow as tf
+ tf.random.set_seed(0)

### PyTorch
import torch
+ torch.manual_seed(0)

### Scikit-Learn
from sklearn.model_selection 
import KFold
+ rng = 0
- kf = KFold(random_state=None)
+ kf = KFold(random_state=rng)

### NumPy
import numpy as np
+ np.random.seed(0)
```

### Source:

#### Paper 

#### Grey Literature
- https://towardsdatascience.com/my-machine-learning-model-is-perfect-9a7928e0f604
- https://github.com/IgorSusmelj/pytorch-styleguide

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/57416925/best-practices-for-generating-a-random-seeds-to-seed-pytorch

#### Documentation
- https://pytorch.org/docs/stable/notes/randomness.html

