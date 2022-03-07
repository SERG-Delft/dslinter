# dslinter
[![build dslinter](https://github.com/Hynn01/dslinter/actions/workflows/build.yml/badge.svg)](https://github.com/Hynn01/dslinter/actions/workflows/build.yml)
[![codecov.io](https://codecov.io/github/Hynn01/dslinter/coverage.svg?branch=main)](https://codecov.io/github/Hynn01/dslinter?branch=main)

`dslinter` is a pylint plugin for linting data science and machine learning code. We plan to support the following Python libraries: TensorFlow, PyTorch, Scikit-Learn, Pandas, NumPy and SciPy.

Implemented checkers:

- **[C5501 - C5506] Import Checker**: Check whether data science modules are imported using the correct naming conventions.

- **W5501 InPlace Checker(Pandas)**: Operations on DataFrames return new DataFrames, and they should be assigned to a variable. If the result of a operation on a DataFrame is not assigned to a variable, the result will be lost, so the rule is violated. Operations from the whitelist and with `in_place` parameter set are excluded.

- **W5502 InPlace Checker(NumPy)**: The result of the NumPy operations should be assign to a variable. If the operation is not assigned to a variable, the result will be lost, so the rule is violated. Operations from whitelist and with `out` parameter (can act as in-place) set are excluded. 

- **W5511 Unnecessary Iteration Checker(Pandas)**: Vectorized solutions are preferred over iterators for DataFrames. If iterations are used while there are better solutions, the rule is violated.

- **W5512 Unnecessary Iteration Checker(Pandas)**: A dataframe where is iterated over should not be modified. If the dataframe is modified during iteration, the rule is violated.

- **W5513 Unnecessary Iteration Checker(TensoFlow)**: If there is any augment assignment operation in the loop, the rule is violated. Augment assignment in the loop can be replace with vectorized solution in TensorFlow API.

- **Hyperparameter Checker**: For (scikit-learn) learning algorithms, all hyperparameters should be set.
- **Data Leakage Checker**: All scikit-learn estimators should be used inside Pipelines, to prevent data leakage between
    training and test data.
- **Controlling Randomness Checker**: For reproducible results across executions, remove any use of random_state=None in scikit-learn estimators.
- **Scaler before PCA Checker**: Check scaler is used before Principle Component Analysis (PCA) in a scikit-learn pipeline. Feature scaling is important for PCA.

- **Nan Equality Checker**: Values cannot be compared with np.nan, as `np.nan != np.nan`.


## Installation
To install from the Python Package Index:
```
pip install dslinter
```

## Usage
To only use the checkers implemented in this plugin, run:
```
pylint --load-plugins=dslinter --disable=all --enable=dataframe,nan,hyperparameters,import,data-leakage,controlling-randomness,excessive-hyperparameter-precision,pca-scaler <other_options> <path_to_sources>
```
To expand a current pylint configuration with the checkers from this plugin, run:
```
pylint --load-plugins=dslinter <other_options> <path_to_sources>
```

## How to contribute
1. fork the repository
2. dslinter uses poetry to manage dependencies. To install from source for development purposes, clone this repo and install the plugin with:
```
pip install poerty
poetry install
poetry build
pip install ./dist/dslinter-version.tar.gz
```
3. Assign yourself to the issue you want to solve. If you identify a new issue that needs to be solved, feel free to open a new issue.
4. Make changes to the repository and run the tests.
To run the tests using pytest:
```
poetry run pytest .
```
5. Make a pull request. The pull request is expected to pass the tests.

