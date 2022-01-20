---
title: "Regular Expression Solution Not Optimal"
disableShare: true
# ShowReadingTime: true
tags: ["not sure", "api-specific", "data preparation", "efficiency"]
weight: 15
---

### Description

A post provides a better coding solution for the regular expression, which might be able to apply to the Nature Language Processing (NLP) preprocessing process. NLP tasks are data-intensive and often take a long time to clean the data, so it would be good to save some time when preprocessing the data. The post noted that `regex.sub()` and `str.translate()` work faster than `str.replace()` in practice in Pandas library. The more efficient solution is worth considering.

### Type

API Specific

### Existing Stage

Data Preparation

### Effect

Efficiency

### Example

```python

### Pandas
import Pandas as pd
df = pd.DataFrame({'text':['a..b?!??', '%hgh&12','abc123!!!', '$$$1234']})

# Violated Code
df['text'] = df['text'].str.replace(r'[^\w\s]+', '')


# Recommended Fix
punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{}~'   # `|` is not present here
transtab = str.maketrans(dict.fromkeys(punct, ''))
df['text'] = '|'.join(df['text'].tolist()).translate(transtab).split('|')


```

### Source:

#### Paper 
#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/50444346/fast-punctuation-removal-with-pandas/50444347#50444347

#### Documentation

