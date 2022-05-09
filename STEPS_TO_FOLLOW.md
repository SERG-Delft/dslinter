### Here are the steps to follow for the evaluation :)

## For Python Project:
### STEP 1
Install `dslinter` from the Python Package Index:
```
pip install dslinter
```
### STEP 2
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
forward-pytorch,gradient-clear-pytorch,data-leakage-scikitlearn,\
dependent-threshold-scikitlearn,dependent-threshold-tensorflow,dependent-threshold-pytorch \
--output-format=json:report.json,text:report.txt,colorized \
--reports=y \
<path_to_the_project>
```
[For Windows Users]:
```
pylint --load-plugins=dslinter --disable=all --enable=import,unnecessary-iteration-pandas,unnecessary-iteration-tensorflow,nan-numpy,chain-indexing-pandas,datatype-pandas,column-selection-pandas,merge-parameter-pandas,inplace-pandas,dataframe-conversion-pandas,scaler-missing-scikitlearn,hyperparameters-scikitlearn,hyperparameters-tensorflow,hyperparameters-pytorch,memory-release-tensorflow,deterministic-pytorch,randomness-control-numpy,randomness-control-scikitlearn,randomness-control-tensorflow,randomness-control-pytorch,randomness-control-dataloader-pytorch,missing-mask-tensorflow,missing-mask-pytorch,tensor-array-tensorflow,forward-pytorch,gradient-clear-pytorch,data-leakage-scikitlearn,dependent-threshold-scikitlearn,dependent-threshold-tensorflow,dependent-threshold-pytorch --output-format=json:report.json,text:report.txt,colorized --reports=y <path_to_sources>
```

## For Notebook:
For notebook, we need to convert it to Python file first and run `dslinter` on the Python file.
To convert the notebook to Python file, run:
```
jupyter nbconvert --to script <path_to_the_notebook>
```
Then following the two steps mentioned above for Python project.
