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

    def visit_call(self, node: astroid.nodes.Call):
        """
        When a Call node is visited, ...

        :param node: Node which is visited.
        """
        if node.func.name == "KMeans":
            self.check_hyperparameters_kmeans(node)

    def check_hyperparameters_kmeans(self, node: astroid.nodes.Call):
        """
        Check if the hyperparameters of a KMeans call are all set.

        Hyperparameter(s):
        - n_clusters keyword (or the first positional one).

        :param node: Node which is visited.
        """
        if not len(node.args) >= 1 and not self.has_keyword(
            node.keywords, "n_clusters"
        ):
            self.add_message("hyperparameters", node=node)

    @staticmethod
    def has_keyword(keywords: List[astroid.nodes.Keyword], keyword_goal: str) -> bool:
        """
        Check if a list of keywords contain a certain keyword.

        :param keywords: List of keywords.
        :param keyword_goal: Name of the keyword which is checked against.
        :return: True if the keyword is present, False if it is not.
        """
        if keywords is None:
            return False

        for keyword in keywords:
            if keyword.arg == keyword_goal:
                return True
        return False
