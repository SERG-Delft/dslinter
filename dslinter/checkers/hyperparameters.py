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
        "W5505": (
            "Hyperparameter not set.",
            "hyperparameters",
            "For learning algorithms, hyperparameters should be tuned and set.",
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

    # Main hyperparameters of learning algorithms, as defined in research.
    # Sources:
    # 1. Probst, P., Boulesteix, A. L., & Bischl, B. (2019). Tunability: Importance of
    #   Hyperparameters of Machine Learning Algorithms. Journal of Machine Learning Research,
    #   20(53), 1-32.
    # 2. van Rijn, J. N., & Hutter, F. (2018, July). Hyperparameter importance across datasets.
    #   In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery &
    #   Data Mining (pp. 2367-2376).
    HYPERPARAMETERS_MAIN = {
        # sklearn.ensemble
        "AdaBoostClassifier": {"positional": 3, "keywords": ["learning_rate"]},
        "AdaBoostRegressor": {"positional": 3, "keywords": ["learning_rate"]},
        "GradientBoostingClassifier": {"positional": 2, "keywords": ["learning_rate"]},
        "GradientBoostingRegressor": {"positional": 2, "keywords": ["learning_rate"]},
        "HistGradientBoostingClassifier": {"positional": 2, "keywords": ["learning_rate"]},
        "HistGradientBoostingRegressor": {"positional": 2, "keywords": ["learning_rate"]},
        "RandomForestClassifier": {"positional": 7, "keywords": ["min_samples_leaf", "max_features"],},
        "RandomForestRegressor": {"positional": 7, "keywords": ["min_samples_leaf", "max_features"],},
        # sklearn.linear_model
        "ElasticNet": {"positional": 2, "keywords": ["alpha", "l1_ratio"]},
        # sklearn.neighbors
        "NearestNeighbors": {"positional": 1, "keywords": ["n_neighbors"]},
        # sklearn.svm
        "NuSVC": {"positional": 4, "keywords": ["nu", "kernel", "gamma"]},
        "NuSVR": {"positional": 4, "keywords": ["C", "kernel", "gamma"]},
        "SVC": {"positional": 4, "keywords": ["C", "kernel", "gamma"]},
        "SVR": {"positional": 4, "keywords": ["C", "kernel", "gamma"]},
        # sklearn.tree
        "DecisionTreeClassifier": {"positional": 14, "keywords": ["ccp_alpha"]},
        "DecisionTreeRegressor": {"positional": 14, "keywords": ["ccp_alpha"]},
    }

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether hyperparameters are set.

        In strict mode, all hyperparameters should be set.
        In non-strict mode, function calls to learning functions should either contain all
        hyperparameters defined in HYPERPARAMETERS_MAIN or have at least one hyperparameter defined.

        :param node: Node which is visited.
        """
        try:
            try:
                function_name = node.func.name
            except AttributeError:
                return

            hyperparams_all = Resources.get_hyperparameters()

            if function_name in hyperparams_all:  # pylint: disable=unsupported-membership-test
                if self.config.strict_hyperparameters:
                    if not HyperparameterChecker._has_required_hyperparameters(node, hyperparams_all):
                        self.add_message("hyperparameters", node=node)
                else:  # non-strict
                    if (
                        function_name in self.HYPERPARAMETERS_MAIN
                        and not HyperparameterChecker._has_required_hyperparameters(node, self.HYPERPARAMETERS_MAIN)
                    ):
                        self.add_message("hyperparameters", node=node)
                    elif len(node.args) == 0 and node.keywords is None:
                        self.add_message("hyperparameters", node=node)
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

    @staticmethod
    def _has_required_hyperparameters(node: astroid.Call, hyperparameters: Dict):
        """
        Evaluate whether a function call has all required hyperparameters defined.

        :param node: Node which is visited.
        :param hyperparameters: Dict of functions with their required hyperparameters.
        :return: True when all required hyperparameters are defined.
        """
        return len(node.args) >= hyperparameters[node.func.name]["positional"] or HyperparameterChecker._has_keywords(
            node.keywords, hyperparameters[node.func.name]["keywords"]
        )

    @staticmethod
    def _has_keywords(keywords: List[astroid.Keyword], keywords_goal: List[str]) -> bool:
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
