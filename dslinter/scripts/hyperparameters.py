"""Functions for getting the signatures of Classes."""
# pylint: disable = line-too-long
import inspect
import pickle
from typing import List


def save_hyperparameter(classes: List, path: str):
    """Functions for getting the signatures of Classes."""
    # Collect all signatures of the learning classes.
    signatures = []
    for c in classes:
        try:
            signatures.append((c.__name__, inspect.signature(c)))
        except ValueError as ex:
            print(ex)

    # Construct the dict with hyperparameters from the signatures.
    hyperparameters = {}
    for class_name, signature in signatures:
        keywords_amount = len(signature.parameters)
        keywords = list(signature.parameters.keys())
        hyperparameters[class_name] = {"positional": keywords_amount, "keywords": keywords}

    print(hyperparameters)

    # Write the pickled hyperparameters dict to disk and verify it.
    with open(path, "wb") as file_handler:
        pickle.dump(hyperparameters, file_handler)
        print("The pickle with all hyperparameters is written to disk.")
    with open(path, "rb") as file_handler:
        hyperparameters_loaded = pickle.load(file_handler)
        assert hyperparameters == hyperparameters_loaded

    print("Done!")
