---
title: "Hyperparameter not Explicitly Set"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "data preparation", "error-prone","reproducibility"]
weight: 6
---

### Description

Hyperparameters are ML algorithm parameters used to control the learning process and are usually determined before the actual process starts. Hyperparameters should be set and tuned because they improve prediction quality
and reproducibility. Tuning hyperparameters can lead to higher prediction quality because the default
parameters of the learning algorithm may not be optimal for a given data or problem, and may lead to local optima.  These parameters directly control the behavior of the training algorithm and therefore have a significant impact on the performance of the model.

The second reason for defining hyperparameters for learning algorithms is that it improves reproducibility. While the default parameters of a machine learning library may be perfect for some time, these default parameters of the library may change in new versions of the library. In addition, setting all hyperparameters explicitly allows replicating the model in a different programming language. Therefore, it is easier to reproduce the results if hyperparameters are set.

### Type

Generic

### Existing Stage

Data Preparation

### Effect

Error-prone & Reproducibility

### Example

```diff
### Scikit-Learn
from sklearn.cluster import KMeans

- kmeans = KMeans()
+ kmeans = KMeans(n_clusters=8, random_state=0)
+ # Or, ideally:
+ kmeans = KMeans(n_clusters=8,
+ init='k-means++', n_init=10,
+ max_iter=300, tol=0.0001,
+ precompute_distances='auto',
+ verbose=0, random_state=0,
+ copy_x=True, n_jobs=1,
+ algorithm='auto')

### PyTorch
import torch
import numpy as np
from kmeans_pytorch import kmeans

# data
data_size, dims, num_clusters = 1000, 2, 3
x = np.random.randn(data_size, dims) / 6
x = torch.from_numpy(x)

# kmeans
- cluster_ids_x, cluster_centers = kmeans(X=x, num_clusters=num_clusters)
+ cluster_ids_x, cluster_centers = kmeans(
+     X=x, num_clusters=num_clusters, distance='euclidean', device=torch.device('cpu')
+ )
```

### Source:

#### Paper 
- MPA Haakman. 2020. Studying the Machine Learning Lifecycle and ImprovingCode Quality of Machine Learning Applications. (2020).
- Eric Breck, Shanqing Cai, Eric Nielsen, Michael Salib, and D Sculley. 2017. TheML test score: A rubric for ML production readiness and technical debt reduction.In2017 IEEE International Conference on Big Data (Big Data). IEEE, 1123–1132.
- Gopi Krishnan Rajbahadur, Gustavo Ansaldi Oliva, Ahmed E Hassan, and Juer-gen Dingel. 2019.   Pitfalls Analyzer: Quality Control for Model-Driven DataScience Pipelines. In2019 ACM/IEEE 22nd International Conference on ModelDriven Engineering Languages and Systems (MODELS). IEEE, 12–22.
- Nargiz Humbatova, Gunel Jahangirova, Gabriele Bavota, Vincenzo Riccio, AndreaStocco, and Paolo Tonella. 2020. Taxonomy of real faults in deep learning sys-tems. InProceedings of the ACM/IEEE 42nd International Conference on SoftwareEngineering. 1110–1121.

#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation

