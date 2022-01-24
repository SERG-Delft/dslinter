---
title: "Columns and DataType Not Explicitly Set"
disableShare: true
summary:
tags: 
weight: 
# ShowReadingTime: true	
---

### Description

#### Context

#### Problem

#### Solution


### Type


### Existing Stage


### Effect


### Example

```diff
import pandas as pd
df = pd.read_csv('data.csv')
+ df = df[['col1', 'col2', 'col3']]
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

