[![build dslinter](https://github.com/Hynn01/dslinter/actions/workflows/build.yml/badge.svg)](https://github.com/Hynn01/dslinter/actions/workflows/build.yml)
[![codecov.io](https://codecov.io/github/Hynn01/dslinter/coverage.svg?branch=main)](https://codecov.io/github/Hynn01/dslinter?branch=main)
# dslinter
Pylint plugin for linting data science and machine learning code, focussed on the libraries pandas and scikit-learn.

Implemented checkers:

- **Unassigned DataFrame Checker**: Operations on DataFrames return new DataFrames. These DataFrames should be
    assigned to a variable.
- **DataFrame Iteration Checker**: Vectorized solutions are preferred over iterators for DataFrames.
- **Nan Equality Checker**: Values cannot be compared with np.nan, as `np.nan != np.nan`.
- **Hyperparameter Checker**: For (scikit-learn) learning algorithms, all hyperparameters should be set.
- **Import Checker**: Check whether data science modules are imported using the correct naming conventions.
- **Data Leakage Checker**: All scikit-learn estimators should be used inside Pipelines, to prevent data leakage between
    training and test data.
- **Controlling Randomness Checker**: For reproducible results across executions, remove any use of random_state=None in scikit-learn estimators.
- **Excessive Hyperparameter Precision Checker**: Check hyperparameter in scikit-learn estimators. excessive hyperparameter precision might suggest over-tuning.
- **Scaler before PCA Checker**: Check scaler is used before Principle Component Analysis (PCA) in a scikit-learn pipeline. Feature scaling is important for PCA.


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

```

## How to contribute
1. clone the repository:
```
git clone https://github.com/Hynn01/dslinter.git
cd dslinter
```
2. dslinter uses poetry to manage dependencies. To install from source for development purposes: clone this repo and install the plugin with:
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

