### Here are the steps to follow for the evaluation :)

We recommend you wrap your project (or jupyter notebook) in a parent folder and run the following command on that folder. The output **txt** file, by default, will be generated at the folder where you run your command on.

## For Python Project:

### STEP 1
Install `dslinter` from the Python Package Index:
```
pip install dslinter
```
### STEP 2
A `__init__.py` file (can be empty) is expected at the <path_to_the_project> folder.

Copy the following command in your terminal, type in the path to your project, and press `enter` to run:

[For Linux/Mac OS Users]:
```
pylint \
--load-plugins=dslinter \
--disable=all \
--enable=import,unnecessary-iteration-pandas,unnecessary-iteration-tensorflow,\
nan-numpy,chain-indexing-pandas,datatype-pandas,\
column-selection-pandas,merge-parameter-pandas,inplace-pandas,\
dataframe-conversion-pandas,scaler-missing-scikitlearn,hyperparameters-scikitlearn,\
hyperparameters-tensorflow,hyperparameters-pytorch,memory-release-tensorflow,\
deterministic-pytorch,randomness-control-numpy,randomness-control-scikitlearn,\
randomness-control-tensorflow,randomness-control-pytorch,randomness-control-dataloader-pytorch,\
missing-mask-tensorflow,missing-mask-pytorch,tensor-array-tensorflow,\
forward-pytorch,gradient-clear-pytorch,pipeline-not-used-scikitlearn,\
dependent-threshold-scikitlearn,dependent-threshold-tensorflow,dependent-threshold-pytorch \
--output-format=text:report.txt,colorized \
--reports=y \
<path_to_the_project>
```
[For Windows Users]:
```
pylint --load-plugins=dslinter --disable=all --enable=import,unnecessary-iteration-pandas,unnecessary-iteration-tensorflow,nan-numpy,chain-indexing-pandas,datatype-pandas,column-selection-pandas,merge-parameter-pandas,inplace-pandas,dataframe-conversion-pandas,scaler-missing-scikitlearn,hyperparameters-scikitlearn,hyperparameters-tensorflow,hyperparameters-pytorch,memory-release-tensorflow,deterministic-pytorch,randomness-control-numpy,randomness-control-scikitlearn,randomness-control-tensorflow,randomness-control-pytorch,randomness-control-dataloader-pytorch,missing-mask-tensorflow,missing-mask-pytorch,tensor-array-tensorflow,forward-pytorch,gradient-clear-pytorch,pipeline-not-used-scikitlearn,dependent-threshold-scikitlearn,dependent-threshold-tensorflow,dependent-threshold-pytorch --output-format=text:report.txt,colorized --reports=y <path_to_sources>
```

## For Notebook:

### STEP 1
For notebook, we need to convert it to Python file first and run `dslinter` on the Python file.
To convert the notebook to Python file, run:
```
jupyter nbconvert --to script <path_to_the_notebook>
```
### STEP 2
Install `dslinter` from the Python Package Index:
```
pip install dslinter
```
### STEP 3
Copy the following command in your terminal, type in the path to your project, and press `enter` to run:

[For Linux/Mac OS Users]:
```
pylint \
--load-plugins=dslinter \
--disable=all \
--enable=import,unnecessary-iteration-pandas,unnecessary-iteration-tensorflow,\
nan-numpy,chain-indexing-pandas,datatype-pandas,\
column-selection-pandas,merge-parameter-pandas,inplace-pandas,\
dataframe-conversion-pandas,scaler-missing-scikitlearn,hyperparameters-scikitlearn,\
hyperparameters-tensorflow,hyperparameters-pytorch,memory-release-tensorflow,\
deterministic-pytorch,randomness-control-numpy,randomness-control-scikitlearn,\
randomness-control-tensorflow,randomness-control-pytorch,randomness-control-dataloader-pytorch,\
missing-mask-tensorflow,missing-mask-pytorch,tensor-array-tensorflow,\
forward-pytorch,gradient-clear-pytorch,pipeline-not-used-scikitlearn,\
dependent-threshold-scikitlearn,dependent-threshold-tensorflow,dependent-threshold-pytorch \
--output-format=text:report.txt,colorized \
--reports=y \
<path_to_the_python_file>
```
[For Windows Users]:
```
pylint --load-plugins=dslinter --disable=all --enable=import,unnecessary-iteration-pandas,unnecessary-iteration-tensorflow,nan-numpy,chain-indexing-pandas,datatype-pandas,column-selection-pandas,merge-parameter-pandas,inplace-pandas,dataframe-conversion-pandas,scaler-missing-scikitlearn,hyperparameters-scikitlearn,hyperparameters-tensorflow,hyperparameters-pytorch,memory-release-tensorflow,deterministic-pytorch,randomness-control-numpy,randomness-control-scikitlearn,randomness-control-tensorflow,randomness-control-pytorch,randomness-control-dataloader-pytorch,missing-mask-tensorflow,missing-mask-pytorch,tensor-array-tensorflow,forward-pytorch,gradient-clear-pytorch,pipeline-not-used-scikitlearn,dependent-threshold-scikitlearn,dependent-threshold-tensorflow,dependent-threshold-pytorch --output-format=text:report.txt,colorized --reports=y <path_to_the_python_file>
```
