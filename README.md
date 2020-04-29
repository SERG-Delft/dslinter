# dslinter
Pylint plugin for linting data science and machine learning code, focussed on the libraries pandas and scikit-learn.

Implemented checkers:

- **Unassigned DataFrame Checker**: Operations on a pandas DataFrame return a new DataFrame. This DataFrame should be
    assigned to a variable.
- **DataFrame Iteration Checker**: Vectorized solutions are preferred over iterators for pandas DataFrames.
- **Nan Equality Checker**: Values cannot be compared with np.nan, as `np.nan != np.nan`.
- **Hyperparameter Checker**: For (scikit-learn) learning algorithms, all hyperparameters should be set.
- **Import Checker**: Check whether data science modules are imported using the correct naming conventions.
- **Data Leakage Checker**: All scikit-learn estimators should be used inside Pipelines, to prevent data leakage between
    training and test data.

## Installation
To install from source for development purposes: clone this repo and install the plugin with:
```
pip install -e .
```
To install from the Python Package Index:
```
pip install dslinter
```

## Usage
To only use the checkers implemented in this plugin, run:
```
pylint --load-plugins=dslinter --disable=all --enable=dataframe,nan,hyperparameters,import,data-leakage <other_options> <path_to_sources>
```
To expand a current pylint configuration with the checkers from this plugin, run:
```
pylint --load-plugins=dslinter <other_options> <path_to_sources>
``` 

## Tests
Tests can be run by using the pytest package:
```
pytest .
```
