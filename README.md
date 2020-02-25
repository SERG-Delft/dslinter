# dslinter
Pylint plugin for data science.

## Installation
Go to the package directory and install the plugin with
```
pip install .
```

## Usage
```
pylint --load-plugins=dslinter --disable=all --enable=non-unique-returns [..other options..] <path_to_sources>
```

## Tests
Tests can be run by using the pytest package:
```
pytest .
```
