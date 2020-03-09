"""Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""
from typing import List

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class HyperparameterChecker(BaseChecker):
    """Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""

    __implements__ = IAstroidChecker

    name = "hyperparameters"
    priority = -1
    msgs = {
        "W0001": (
            "Hyperparameter not set.",
            "hyperparameters",
            "For learning algorithms, all hyperparamters should be tuned and set.",
        ),
    }
    options = ()

    hyperparameters = {
        # sklearn.cluster
        "KMeans": [{"positional": 1, "keywords": ["n_clusters"]}],
        "MiniBatchKMeans": [{"positional": 1, "keywords": ["n_clusters"]}],
        "AffinityPropagation": [{"positional": 1, "keywords": ["damping", "preference"]}],
        "MeanShift": [{"positional": 1, "keywords": ["bandwidth"]}],
        "SpectralClustering": [{"positional": 1, "keywords": ["n_clusters"]}],
        "AgglomerativeClustering": [
            {"positional": 1, "keywords": ["n_clusters"]},
            {"positional": 99, "keywords": ["linkage", "distance_threshold"]},
        ],
        "DBSCAN": [{"positional": 2, "keywords": ["eps", "min_samples"]}],
        "OPTICS": [{"positional": 1, "keywords": ["min_samples"]}],
        "Birch": [{"positional": 2, "keywords": ["threshold", "branching_factor"]}],
    }

    def visit_call(self, node: astroid.nodes.Call):
        """
        When a Call node is visited, check if all hyperparameters are set.

        :param node: Node which is visited.
        """
        function_name = node.func.name
        if function_name in self.hyperparameters:
            correct = False
            for option in range(len(self.hyperparameters[function_name])):
                if len(node.args) >= self.hyperparameters[function_name][option][
                    "positional"
                ] or self.has_keywords(
                    node.keywords, self.hyperparameters[function_name][option]["keywords"],
                ):
                    correct = True

            if not correct:
                self.add_message("hyperparameters", node=node)

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
