---
title: "DataLoader Unused"
disableShare: true
# ShowReadingTime: true
tags: 
weight: 18
---

### Description

Some new developers are not aware of using the existing function and writing the function by themselves. However, it is recommended to use the APIs because the APIs provided by the library often consider more things. For instance, in \ref{grey:so_dataloader}, the developer does not use the DataLoader and feeds the data directly to the network. The answerer noted that using DataLoader has several benefits: 1) It allows the developers to sample the data randomly. 2) It does not preload data into memory, which is particularly useful for huge datasets. 3) It operates in the background of code, so it fetches data parallel to train thus saving time. 4) It is very efficient at batching the data. Therefore, it is better to use the DataLoader API than manually splitting the data and directly feeding the data into the network.

### Type

API Specific

### Existing Stage

Data Segregation

### Effect

Robustness

### Example

```python

### Pandas
import pandas as pd

# Violated Code
pd.eval('df.A.str.contains("ab")', engine='python')

# Recommended Fix
pd.eval('df.A.str.contains("ab")')
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/67066452/is-this-a-right-way-to-train-and-test-the-model-using-pytorch/67067242#67067242

#### Documentation

