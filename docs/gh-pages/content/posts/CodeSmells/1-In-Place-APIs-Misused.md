---
title: "In-Place APIs Misused"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "data cleaning", "error-prone"]
weight: 1
summary: "Remember to assign the result of an operation to a variable or set the in-place parameter in the API."
# date: "2019-03-05"
---

### Description

#### Context
Data structures can be manipulated in mainly two different approaches: 1) by applying the changes to a copy of the data structure and leaving the original object intact, or 2) by changing the existing data structure (also known as in-place).

#### Problem
Some methods can adopt in-place by default, while others return a copy. If the developer assumes an in-place approach, he will not assign the returned value to any variable. Hence, the operation will be executed, but it will not affect the final outcome. For example, when using the Pandas library, the developer may not assign the result of `df.dropna()` to a variable. He may assume that this API will make changes on the original `DataFrame` and not set the in-place parameter to be `True` either. The original `DataFrame` will not be updated in this way. In the `"TensorFlow Bugs" replication package`, we also found an example where the developer thought `np.clip()` is an in-place operation and used it without assigning it to a new variable.

#### Solution
We suggest developers check whether the result of the operation is assigned to a variable or the in-place parameter is set in the API. Some developers hold the view that the in-place operation will save memory. However, this is a misconception in the Pandas library because the copy of the data is still created. In PyTorch, the in-place operation does save GPU memory, but it risks overwriting the values needed to compute the gradient.


### Type

Generic

### Existing Stage

Data Cleaning

### Effect

Error-prone

### Example

```diff
### NumPy
import numpy as np
zhats = [2, 3, 1, 0]
- np.clip(zhats, -1, 1)
+ zhats = np.clip(zhats, -1, 1)

### Pandas
import pandas as pd
df = pd.DataFrame([-1])
- df.abs()
+ df = df.abs()
```

### Source:

#### Paper 
- MPA Haakman. 2020. Studying the Machine Learning Lifecycle and ImprovingCode Quality of Machine Learning Applications. 

#### Grey Literature
- https://towardsdatascience.com/in-place-operations-in-pytorch-f91d493e970e
- https://github.com/bamos/dcgan-completion.tensorflow/commit/e8b930501dffe01db423b6ca1c65d3ac54f27223

#### GitHub Commit

#### Stack Overflow

#### Documentation

