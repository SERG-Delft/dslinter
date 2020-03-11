"""Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""
import os
import pickle
from pathlib import Path
from typing import Dict, List

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class HyperparameterChecker(BaseChecker):
    """Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""

    __implements__ = IAstroidChecker

    name = "hyperparameters"
    priority = -1
    msgs = {
        "W5001": (
            "Hyperparameter not set.",
            "hyperparameters",
            "For learning algorithms, all hyperparameters should be tuned and set.",
        ),
        "F5001": (
            "Pickled strict hyperparameters dict not found.",
            "hyperparameters-strict-file-not-found",
            "The pickled dict with strict hyperparameters cannot be found on disk.",
        ),
    }
    options = (
        (
            "strict_hyperparameters",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Force that all parameters of learning algorithms are set.",
            },
        ),
    )

    hyperparameters_main = {
        # sklearn.manifold
        "Isomap": [{"positional": 2, "keywords": ["n_neighbors", "n_components"]}],
        "LocallyLinearEmbedding": [{"positional": 2, "keywords": ["n_neighbors", "n_components"]}],
        "SpectralEmbedding": [{"positional": 1, "keywords": ["n_components"]}],
        "MDS": [{"positional": 1, "keywords": ["n_components"]}],
        "TSNE": [{"positional": 2, "keywords": ["n_components", "perplexity"]}],
        # sklearn.cluster
        "KMeans": [{"positional": 1, "keywords": ["n_clusters"]}],
        "MiniBatchKMeans": [{"positional": 1, "keywords": ["n_clusters"]}],
        "AffinityPropagation": [{"positional": 1, "keywords": ["damping", "preference"]}],
        "MeanShift": [{"positional": 1, "keywords": ["bandwidth"]}],
        "SpectralClustering": [{"positional": 1, "keywords": ["n_clusters"]}],
        "AgglomerativeClustering": [
            {"positional": 1, "keywords": ["n_clusters"]},
            {"positional": 7, "keywords": ["linkage", "distance_threshold"]},
        ],
        "DBSCAN": [{"positional": 2, "keywords": ["eps", "min_samples"]}],
        "OPTICS": [{"positional": 1, "keywords": ["min_samples"]}],
        "Birch": [{"positional": 2, "keywords": ["threshold", "branching_factor"]}],
        # sklearn.neighbors
        "KernelDensity": [{"positional": 1, "keywords": ["bandwidth"]}],
        # klearn.neural_network
        "BernoulliRBM": [{"positional": 2, "keywords": ["n_components", "learning_rate"]}],
        # sklearn.linear_model
        "Ridge": [{"positional": 1, "keywords": ["alpha"]}],
        "Lasso": [{"positional": 1, "keywords": ["alpha"]}],
        "MultiTaskLasso": [{"positional": 1, "keywords": ["alpha"]}],
        "ElasticNet": [{"positional": 2, "keywords": ["alpha", "l1_ratio"]}],
        "MultiTaskElasticNet": [{"positional": 2, "keywords": ["alpha", "l1_ratio"]}],
        "LassoLars": [{"positional": 1, "keywords": ["alpha"]}],
        # sklearn.svm
        "SVC": [{"positional": 4, "keywords": ["C", "gamma"]}],
        "NuSVC": [{"positional": 4, "keywords": ["nu", "gamma"]}],
        # There are more modules.
    }

    def __init__(self, linter=None):
        """
        Initialize the checker.

        :param linter: Linter where the checker is added to.
        """
        super(HyperparameterChecker, self).__init__(linter)
        self._hyperparameters_strict = None
        self._strict_pickle = os.path.join(
            Path(__file__).parent.parent.parent, "resources\\hyperparameters_dict.pickle"
        )

    def visit_call(self, node: astroid.nodes.Call):
        """
        When a Call node is visited, check whether all hyperparameters are set.

        :param node: Node which is visited.
        """
        try:
            function_name = node.func.name
        except AttributeError:
            return

        hyperparameters = self.hyperparameters_to_check()
        if function_name in hyperparameters:
            correct = False
            for option in range(len(hyperparameters[function_name])):
                if len(node.args) >= hyperparameters[function_name][option][
                    "positional"
                ] or self.has_keywords(
                    node.keywords, hyperparameters[function_name][option]["keywords"],
                ):
                    correct = True

            if not correct:
                self.add_message("hyperparameters", node=node)

    def hyperparameters_to_check(self) -> Dict:
        """
        Get the hyperparameters to check against.

        :return: Dict of learning classes and parameters needed.
        """
        if self.config.strict_hyperparameters:
            if self._hyperparameters_strict is None:
                self.load_hyperparameters_pickle()
            return self._hyperparameters_strict
        return self.hyperparameters_main

    @staticmethod
    def has_keywords(keywords: List[astroid.nodes.Keyword], keywords_goal: List[str]) -> bool:
        """
        Check if a list of keywords contains certain keywords.

        :param keywords: List of keywords.
        :param keywords_goal: Name of the keywords which are checked against.
        :return: True if keywords are present, False if they are not.
        """
        if keywords is None:
            return False

        found = 0
        for keyword in keywords:
            if keyword.arg in keywords_goal:
                found += 1

        return found == len(keywords_goal)

    def load_hyperparameters_pickle(self):
        """Load the pickled strict hyperparameters dict from disk."""
        if os.path.exists(self._strict_pickle):
            with open(self._strict_pickle, "rb") as file_handler:
                self._hyperparameters_strict = pickle.load(file_handler)
        else:
            self.add_message("hyperparameters-strict-file-not-found")
            self._hyperparameters_strict = self.hyperparameters_main

    @property
    def strict_pickle(self):
        """Get the _strict_pickle property."""
        return self._strict_pickle

    @strict_pickle.setter
    def strict_pickle(self, value):
        """Set the _strict_pickle property."""
        self._strict_pickle = value
