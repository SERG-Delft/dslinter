# dslinter
[![build dslinter](https://github.com/Hynn01/dslinter/actions/workflows/build.yml/badge.svg)](https://github.com/Hynn01/dslinter/actions/workflows/build.yml)
[![codecov.io](https://codecov.io/github/Hynn01/dslinter/coverage.svg?branch=main)](https://codecov.io/github/Hynn01/dslinter?branch=main)

`dslinter` is a pylint plugin for linting data science and machine learning code. We plan to support the following Python libraries: TensorFlow, PyTorch, Scikit-Learn, Pandas, NumPy and SciPy.

## Implemented Checkers:

- **[C5501 - C5506] Import Checker**: Check whether data science modules are imported using the correct naming conventions.

- **W5501 InPlace Checker(Pandas)**: Operations on DataFrames return new DataFrames, and they should be assigned to a variable. If the result of a operation on a DataFrame is not assigned to a variable, the result will be lost, so the rule is violated. Operations from the whitelist and with `in_place` parameter set are excluded.

- **W5502 InPlace Checker(NumPy)**: The result of the NumPy operations should be assign to a variable. If the operation is not assigned to a variable, the result will be lost, so the rule is violated. Operations from whitelist and with `out` parameter (can act as in-place) set are excluded. 

- **W5511 Unnecessary Iteration Checker(Pandas)**: Vectorized solutions are preferred over iterators for DataFrames. If iterations are used while there are better solutions, the rule is violated.

- **W5512 Unnecessary Iteration Checker(Pandas)**: A dataframe where is iterated over should not be modified. If the dataframe is modified during iteration, the rule is violated.

- **W5513 Unnecessary Iteration Checker(TensorFlow)**: If there is any augment assignment operation in the loop, the rule is violated. Augment assignment in the loop can be replace with vectorized solution in TensorFlow API.

- **W5521 Scaler Missing Checker(ScikitLearn)**: Check scaler is used before scaling-sensitive operations in a scikit-learn pipeline. Scaling-sensitive operations includes Principal Component Analysis (PCA), Support Vector Machine (SVM), Stochastic Gradient Descent (SGD), Multi-layer Perceptron classifier and L1 and L2 regularization

- **W5531 Hyperparameter Checker(ScikitLearn)**: For scikit-learn learning algorithms, some important hyperparameters should be set.

- **W5532 Hyperparameter Checker(PyTorch)**: For neural network learning algorithm, some imporatnt hyperparameters should be set, such as learning rate, batch size, momentum and weight decay.

- **W5533 Hyperparameter Checker(TensorFlow)**: For neural network learning algorithm, some imporatnt hyperparameters should be set, such as learning rate, batch size, momentum and weight decay.

- **W5541 Memory Release Checker(TensorFlow)**: If a neural network is created in the loop, and no memory clear operation is used, the rule is violated.

- **W5551 Deterministic Algorithm Usage Checker(PyTorch)**: If use_deterministic algorithm is not used in a pytorch program, the rule is violated.

- **W5561 Randomness Control Checker(ScikitLearn)**: For reproducible results across executions, remove any use of random_state=None in scikit-learn estimators.

- **W5562 Randomness Control Checker(TensorFlow)**: The tf.random.set_seed() should be used to preserve reproducibility in a Tensorflow program.

- **W5563 Randomness Control Checker(PyTorch)**: The torch.manual_seed() should be used to preserve reproducibility in a Tensorflow program.

- **W5564 Randomness Control Checker(NumPy)**: The np.seed() should be used to preserve reproducibility in a machine learning program.

- **W5565 Randomness Control Checker(PyTorch-Dataloader)**: The worker_init_fn() and generator should be set in dataloader to preserve reproducibility. If they're not set, the rule is violated.

- **W5571 Mask Missing Checker(TensorFlow)**: If log function is used in the code, check whether the argument value is valid. 

- **W5572 Mask Missing Checker(PyTorch)**: If log function is used in the code, check whether the argument value is valid. 

- **W5581 Data Leakage Checker(ScikitLearn)**: All scikit-learn estimators should be used inside Pipelines, to prevent data leakage between training and test data.

- **W5591 Dependent Threshold Checker(TensorFlow)**: If threshold-dependent evaluation(e.g., f-score) is used in the code, check whether threshold-indenpendent evaluation(e.g., auc) metrics is also used in the code.

- **W5592 Dependent Threshold Checker(PyTorch)**: If threshold-dependent evaluation(e.g., f-score) is used in the code, check whether threshold-indenpendent evaluation(e.g., auc) metrics is also used in the code.

- **W5593 Dependent Threshold Checker(ScikitLearn)**: If threshold-dependent evaluation(e.g., f-score) is used in the code, check whether threshold-indenpendent evaluation(e.g., auc) metrics is also used in the code.


- **W5601 Nan Equality Checker (NumPy)**: Values cannot be compared with np.nan, as `np.nan != np.nan`.


## Installation
To install from the Python Package Index:
```
pip install dslinter
```

## Usage
To only use the checkers implemented in this plugin, run:
```
pylint --load-plugins=dslinter --disable=all --enable=import,data-leakage <other_options> <path_to_sources>
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

