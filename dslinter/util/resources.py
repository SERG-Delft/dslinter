"""Utility module for reading resources."""

import pickle
from typing import Dict, List, Union

from pkg_resources import resource_stream


class Resources:
    """Utility class for reading resources."""

    __RESOURCES_PACKAGE = "dslinter.resources"

    @staticmethod
    def get_hyperparameters(hyperparameter_resource) -> Dict[str, Dict[str, Union[int, List[str]]]]:
        """
        Get the hyperparameters resource.

        :return: Dict with every learning algorithm from scikit-learn as keys. Each value is a Dict
        containing the keys 'positional' and 'keywords' containing its amount of keywords and a list
        with the names of its keywords respectively.
        """
        return Resources.read_pickle(hyperparameter_resource)

    @staticmethod
    def read_pickle(file):
        """
        Read a pickled object from disk.

        :param file: File name of the pickle in the resource package.
        :return: Deserialized object.
        """
        return pickle.load(resource_stream(Resources.__RESOURCES_PACKAGE, file))
