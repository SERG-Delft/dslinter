# dslinter
[![build dslinter](https://github.com/Hynn01/dslinter/actions/workflows/build.yml/badge.svg)](https://github.com/Hynn01/dslinter/actions/workflows/build.yml)
[![codecov.io](https://codecov.io/github/Hynn01/dslinter/coverage.svg?branch=main)](https://codecov.io/github/Hynn01/dslinter?branch=main)

`dslinter` is a pylint plugin for linting data science and machine learning code. We plan to support the following Python libraries: TensorFlow, PyTorch, Scikit-Learn, Pandas, NumPy and SciPy.

Implemented checkers:

- **Import Checker**: Check whether data science modules are imported using the correct naming conventions.
- **Unassigned DataFrame Checker**: Operations on DataFrames return new DataFrames. These DataFrames should be
    assigned to a variable.
- **DataFrame Iteration Checker**: Vectorized solutions are preferred over iterators for DataFrames.
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
pylint --load-plugins=dslinter --disable=all --enable=import,data-leakage <other_options> <path_to_sources>
```
To expand a current pylint configuration with the checkers from this plugin, run:
```
pylint --load-plugins=dslinter <other_options> <path_to_sources>
```

## How to contribute
Contributions are welcome! If you want to contribute, please see the following steps:
1. fork the repository and clone the repository you forked
2. `dslinter` uses `poetry` to manage dependencies, so you will need to install `poetry` first and then install the dependencies. 
```
pip install poerty
poetry install
```
To install `dslinter` from source for development purposes, install it with:
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

