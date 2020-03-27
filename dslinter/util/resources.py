"""Utility class for reading resources."""

import os
import pickle
from pathlib import Path
from typing import Dict, List, Union


class Resources:
    """Utility class for reading resources."""

    __RESOURCES_PATH = os.path.join(Path(__file__).parent.parent.parent, "resources")
    __HYPERPARAMETER_PATH = os.path.join(__RESOURCES_PATH, "hyperparameters_dict.pickle")

    __HYPERPARAMETERS = None

    @staticmethod
    def get_hyperparameters() -> Dict[str, List[Dict[str, Union[int, List[str]]]]]:
        """
        Get the hyperparameters resource.

        :return: Dict with every learning algorithm from scikit-learn as keys. Each value is a list
        of length one, with a Dict containing the keys 'positional' and 'keywords' containing its
        amount of keywords and a list with the names of its keywords respectively.
        """
        if Resources.__HYPERPARAMETERS is None:
            Resources.__HYPERPARAMETERS = Resources.read_pickle(Resources.__HYPERPARAMETER_PATH)
        return Resources.__HYPERPARAMETERS

    @staticmethod
    def read_pickle(path: str):
        """
        Read a pickled object from disk.

        :param path: Path of the pickle.
        :return: Deserialized object.
        """
        with open(path, "rb") as file_handler:
            return pickle.load(file_handler)
