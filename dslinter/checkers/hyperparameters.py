"""Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""
from typing import Dict, List

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.resources import Resources


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

    HYPERPARAMETERS_MAIN = {
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
        "SVC": [{"positional": 4, "keywords": ["C", "kernel", "gamma"]}],
        "NuSVC": [{"positional": 4, "keywords": ["nu", "kernel", "gamma"]}],
        # There are more modules.
    }

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether all hyperparameters are set.

        :param node: Node which is visited.
        """
        try:
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
        except:
            ExceptionHandler.handle(self, node)

    def hyperparameters_to_check(self) -> Dict:
        """
        Get the hyperparameters to check against, depending on the config 'strict_hyperparameters'.

        See Resources.get_hyperparameters() for a description of the Dict.

        :return: Dict of learning classes and parameters needed.
        """
        if self.config.strict_hyperparameters:
            return Resources.get_hyperparameters()
        return self.HYPERPARAMETERS_MAIN

    @staticmethod
    def has_keywords(keywords: List[astroid.Keyword], keywords_goal: List[str]) -> bool:
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
