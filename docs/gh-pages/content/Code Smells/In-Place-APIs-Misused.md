---
title: "In Place APIs Misused"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "data preparation", "error-prone"]
weight: 2
---

### Description

“In-place operation is an operation that directly changes the content of a given linear algebra, vector, matrices (Tensor) without making a copy.” Due to the nature of the in-place operation, the in-place APIs are easily misused. Developers sometimes forget to set the in-place parameter in APIs to true while not assigning the new result to a variable, causing potential silent bugs. The data is not updated in this way, but the developer thinks it is and might not be able to find where the bug is. For example, when using Pandas library, sometimes the developers do not assign the new result to a DataFrame without setting the in-place parameter to be true, causing the DataFrame not to be updated. In the TensorFlow dataset, we also found an example that the developer thought `np.clip()` is an in-place operation and used it without assigning it to a new variable.

Some developers hold the view that in-place operation will save memory. However, in Pandas library, this is a misconception because the copy of the data is still created. In PyTorch, the in-place operation does save GPU memory, but it can potentially overwrite values required to compute gradients. Therefore, we suggest developers be careful with the in-place operation.

### Type

Generic

### Existing Stage

Data Preparation

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

