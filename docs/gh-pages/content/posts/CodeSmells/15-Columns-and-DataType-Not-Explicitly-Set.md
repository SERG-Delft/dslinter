---
title: "Columns and DataType Not Explicitly Set"
disableShare: true
tags: ["api-specific", "data cleaning", "readability"]
weight: 15
# ShowReadingTime: true	
summary: "Explicitly select columns and set `DataType` in Pandas."
---

### Description

#### Context

All columns are selected by default when a `DataFrame` is imported from a file or other sources. The data type for each column is defined based on the default `dtype` conversion.

#### Problem

If the columns are not selected explicitly, it is not easy for developers to know what to expect in the downstream data schema. If the datatype is not set explicitly, it may silently continue the next step even though the input is unexpected, which may cause errors later.

#### Solution
It is recommended to set their columns and `DataType` explicitly.


### Type

API-Specific

### Existing Stage

Data Cleaning

### Effect

Readability

### Example

```diff
import pandas as pd
df = pd.read_csv('data.csv')
+ df = df[['col1', 'col2', 'col3']]
```

### Source:

#### Paper 

#### Grey Literature
- https://github.com/joshlk/pandas_style_guide

#### GitHub Commit

#### Stack Overflow

#### Documentation

