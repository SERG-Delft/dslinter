# dslinter
[![build](https://github.com/SERG-Delft/dslinter/actions/workflows/build.yml/badge.svg)](https://github.com/SERG-Delft/dslinter/actions/workflows/build.yml)
[![codecov.io](https://codecov.io/github/SERG-Delft/dslinter/coverage.svg?branch=main)](https://codecov.io/github/SERG-Delft/dslinter?branch=main)
[![PyPI version](https://badge.fury.io/py/dslinter.svg)](https://badge.fury.io/py/dslinter)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI - Downloads - Monthly](https://img.shields.io/pypi/dm/dslinter)](https://pypi.org/project/dslinter/) 
[![Code Grade](https://api.codiga.io/project/33224/status/svg)](https://api.codiga.io/project/33224/status/svg)

`dslinter` is a PyLint plugin for linting data science and machine learning code. It aims to help developers ensure the machine learning code quality and supports the following Python libraries: TensorFlow, PyTorch, Scikit-Learn, Pandas, NumPy and SciPy. 

`dslinter` implements the detection rules for smells identified by [our previous work](https://arxiv.org/pdf/2203.13746.pdf). The smells are collected from papers, grey literature, GitHub commits, and Stack Overflow posts. The smells are also elaborated at a [website](https://hynn01.github.io/ml-smells/) :)


https://user-images.githubusercontent.com/26082974/166459816-758b2cfc-303d-47d8-ab55-9525e3717c9d.mov

> The example project in the demo video can be found [here](https://github.com/Hynn01/dslinter-example-projects/tree/main/llexnlp).

## Installation
To install from the Python Package Index:
```
pip install dslinter
```

## Usage
To only use the checkers implemented in this plugin, run:
```
pylint \
--load-plugins=dslinter \
--disable=all \
--enable=import,unnecessary-iteration-pandas,unnecessary-iteration-tensorflow,\
nan-numpy,chain-indexing-pandas,datatype-pandas,\
column-selection-pandas,merge-parameter-pandas,inplace-pandas,\
dataframe-conversion-pandas,scaler-missing-scikitlearn,hyperparameters-scikitlearn,\
hyperparameter-tensorflow,hyperparameter-pytorch,memory-release-tensorflow,\
deterministic-pytorch,randomness-control-numpy,randomness-control-scikitlearn,\
randomness-control-tensorflow,randomness-control-pytorch,randomness-control-dataloader-pytorch,\
missing-mask-tensorflow,missing-mask-pytorch,tensor-array-tensorflow,\
forward-pytorch,gradient-clear-pytorch,data-leakage-scikitlearn,\
dependent-threshold-scikitlearn,dependent-threshold-tensorflow,dependent-threshold-pytorch \
--output-format=json:report.json,text:report.txt,colorized \
--reports=y \
<path_to_sources>
```
Or place a [`.pylintrc` configuration file](https://github.com/Hynn01/dslinter/blob/main/docs/pylint-configuration-examples/pylintrc-with-only-dslinter-settings/.pylintrc) which contains above settings in the folder where you run your command on, and run:
```
pylint <path_to_sources>
```
To expand a current pylint configuration with the checkers from this plugin, run:
```
pylint --load-plugins=dslinter <other_options> <path_to_sources>
```

## How to contribute
Contributions are welcome! If you want to contribute, please see the following steps:
1. fork the repository and clone the repository you forked.
```
git clone https://github.com/your-github-account/dslinter.git
git submodule update --init --recursive
```
2. `dslinter` uses `poetry` to manage dependencies, so you will need to install `poetry` first and then install the dependencies. 
```
pip install poerty
poetry install
```
- To install `dslinter` from source for development purposes, install it with:
```
poetry build
pip install ./dist/dslinter-version.tar.gz
```
3. Assign yourself to the issue you want to solve. If you identify a new issue that needs to be solved, feel free to open a new issue.
4. Make changes to the repository and run the tests.
To run the tests using pytest:
```
poetry run pytest .
```
5. Make a pull request. The pull request is expected to pass the tests. :)


## Implemented Checkers:

- **C5501 - C5506 | import | Import Checker**: Check whether data science modules are imported using the correct naming conventions.

- **R5501 | unnecessary-iteration-pandas | Unnecessary Iteration Checker(Pandas)**: Vectorized solutions are preferred over iterators for DataFrames. If iterations are used while there are vectorized APIs can be used, the rule is violated.

- **W5501 | dataframe-iteration-modification-pandas | Unnecessary Iteration Checker(Pandas)**: A dataframe where is iterated over should not be modified. If the dataframe is modified during iteration, the rule is violated.

- **R5502 | unnecessary-iteration-tensorflow | Unnecessary Iteration Checker(TensorFlow)**: If there is any augment assignment operation in the loop, the rule is violated. Augment assignment in the loop can be replaced with vectorized solution in TensorFlow APIs.

- **E5501 | nan-numpy | Nan Equality Checker(NumPy)**: Values cannot be compared with np.nan, as `np.nan != np.nan`.

- **W5502 | chain-indexing-pandas | Chain Indexing Checker(Pandas)**: Chain indexing is considered bad practice in pandas code and should be avoided. If chain indexing is used on a pandas dataframe, the rule is violated.

- **R5503 | datatype-pandas | Datatype Checker(Pandas)**: Datatype should be set when a dataframe is imported from data to ensure the data formats are imported as expected. If the datatype is not set when importing, the rule is violated.

- **R5504 | column-selection-pandas | Column Selection Checker(Pandas)**: Column should be selected after the dataframe is imported for better elaborating what to be expected in the downstream. 

- **R5505 | merge-parameter-pandas | Merge Parameter Checker(Pandas)**: Parameters 'how', 'on' and 'validate' should be set for merge operations to ensure the correct usage of merging.

- **W5503 | inplace-pandas | InPlace Checker(Pandas)**: Operations on DataFrames return new DataFrames, and they should be assigned to a variable. Otherwise the result will be lost, and the rule is violated. Operations from the whitelist and with `in_place` parameter set are excluded.

- **W5504 | dataframe-conversion-pandas | Dataframe Conversion Checker(Pandas)**: For dataframe conversion in pandas code, use .to_numpy() instead of .values. If .values is used in pandas code, the rule is violated.

- **W5505 | scaler-missing-scikitlearn | Scaler Missing Checker(ScikitLearn)**: Check whether the scaler is used before every scaling-sensitive operation in scikit-learn codes. Scaling-sensitive operations includes Principal Component Analysis (PCA), Support Vector Machine (SVM), Stochastic Gradient Descent (SGD), Multi-layer Perceptron classifier and L1 and L2 regularization.

- **R5506 | hyperparameters-scikitlearn | Hyperparameter Checker(ScikitLearn)**: For scikit-learn learning algorithms, some important hyperparameters should be set.

- **R5507 | hyperparameter-tensorflow | Hyperparameter Checker(TensorFlow)**: For neural network learning algorithm, some imporatnt hyperparameters should be set, such as learning rate, batch size, momentum and weight decay.

- **R5508 | hyperparameter-pytorch | Hyperparameter Checker(PyTorch)**: For neural network learning algorithm, some imporatnt hyperparameters should be set, such as learning rate, batch size, momentum and weight decay.

- **W5506 | memory-release-tensorflow | Memory Release Checker(TensorFlow)**: If a neural network is created in the loop, and no memory clear operation is used, the rule is violated.

- **W5507 | deterministic-pytorch | Deterministic Algorithm Usage Checker(PyTorch)**: If use_deterministic algorithm is not used in a pytorch program, the rule is violated.

- **W5508 | randomness-control-numpy | Randomness Control Checker(NumPy)**: The np.seed() should be used to preserve reproducibility in a machine learning program.

- **W5509 | randomness-control-scikitlearn | Randomness Control Checker(ScikitLearn)**: For reproducible results across executions, remove any use of random_state=None in scikit-learn estimators.

- **W5510 | randomness-control-tensorflow | Randomness Control Checker(TensorFlow)**: The tf.random.set_seed() should be used to preserve reproducibility in a Tensorflow program.

- **W5511 | randomness-control-pytorch | Randomness Control Checker(PyTorch)**: The torch.manual_seed() should be used to preserve reproducibility in a Tensorflow program.

- **W5512 | randomness-control-dataloader-pytorch | Randomness Control Checker(PyTorch-Dataloader)**: The worker_init_fn() and generator should be set in dataloader to preserve reproducibility. If they're not set, the rule is violated.

- **W5513 | missing-mask-tensorflow | Mask Missing Checker(TensorFlow)**: If log function is used in the code, check whether the argument value is valid. 

- **W5514 | missing-mask-pytorch | Mask Missing Checker(PyTorch)**: If log function is used in the code, check whether the argument value is valid. 

- **W5515 | tensor-array-tensorflow | Tensor Array Checker(Tensorflow)**: Use tf.TensorArray() for growing array in the loop.

- **W5516 | forward-pytorch | Net Forward Checker(PyTorch)**: It is recommended to use self.net() rather than self.net.forward() in PyTorch code. If self.net.forward() is used in the code, the rule is violated.

- **W5517 | gradient-clear-pytorch | Gradient Clear Checker(PyTorch)**: The loss_fn.backward() and optimizer.step() should be used together with optimizer.zero_grad(). If the ".backward()" is missing in the code, the rule is violated.

- **W5518 | data-leakage-scikitlearn | Data Leakage Checker(ScikitLearn)**: All scikit-learn estimators should be used inside Pipelines, to prevent data leakage between training and test data.

- **W5519 | dependent-threshold-scikitlearn | Dependent Threshold Checker(TensorFlow)**: If threshold-dependent evaluation(e.g., f-score) is used in the code, check whether threshold-indenpendent evaluation(e.g., auc) metrics is also used in the code.

- **W5520 | dependent-threshold-tensorflow | Dependent Threshold Checker(PyTorch)**: If threshold-dependent evaluation(e.g., f-score) is used in the code, check whether threshold-indenpendent evaluation(e.g., auc) metrics is also used in the code.

- **W5521 | dependent-threshold-pytorch | Dependent Threshold Checker(ScikitLearn)**: If threshold-dependent evaluation(e.g., f-score) is used in the code, check whether threshold-indenpendent evaluation(e.g., auc) metrics is also used in the code.
