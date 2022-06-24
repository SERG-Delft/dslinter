"""Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.resources import Resources


class HyperparameterCountChecker(BaseChecker):
    """Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""

    __implements__ = IAstroidChecker

    name = "hyperparameters-scikitlearn-count"
    priority = -1
    msgs = {
        "R9506": (
            "Some of the important hyperparameters is not set in the program.",
            "hyperparameters-scikitlearn-count",
            "For learning algorithms, hyperparameters should be tuned and set.",
        ),
    }

    count_dict = {}
    HYPERPARAMETER_RESOURCE = "hyperparameters_scikitlearn_dict.pickle"
    MESSAGE = "hyperparameters-scikitlearn-count"
    LIBRARY = "scikitlearn"
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
        "AdaBoostClassifier": {"positional": 5, "keywords": ["learning_rate"]},
        "AdaBoostRegressor": {"positional": 5, "keywords": ["learning_rate"]},
        "GradientBoostingClassifier": {"positional": 20, "keywords": ["learning_rate"]},
        "GradientBoostingRegressor": {"positional": 21, "keywords": ["learning_rate"]},
        "HistGradientBoostingClassifier": {"positional": 18, "keywords": ["learning_rate"]},
        "HistGradientBoostingRegressor": {"positional": 18, "keywords": ["learning_rate"]},
        "RandomForestClassifier": {"positional": 18, "keywords": ["min_samples_leaf", "max_features"],},
        "RandomForestRegressor": {"positional": 17, "keywords": ["min_samples_leaf", "max_features"],},
        # sklearn.linear_model
        "ElasticNet": {"positional": 12, "keywords": ["alpha", "l1_ratio"]},
        # sklearn.neighbors
        "NearestNeighbors": {"positional": 8, "keywords": ["n_neighbors"]},
        # sklearn.svm
        "NuSVC": {"positional": 15, "keywords": ["nu", "kernel", "gamma"]},
        "NuSVR": {"positional": 11, "keywords": ["C", "kernel", "gamma"]},
        "SVC": {"positional": 15, "keywords": ["C", "kernel", "gamma"]},
        "SVR": {"positional": 11, "keywords": ["C", "kernel", "gamma"]},
        # sklearn.tree
        "DecisionTreeClassifier": {"positional": 12, "keywords": ["ccp_alpha"]},
        "DecisionTreeRegressor": {"positional": 11, "keywords": ["ccp_alpha"]},
    }
    call_types = {}
    count = 0


    def visit_importfrom(self, node: astroid.ImportFrom):
        try:
            for name, _ in node.names:
                self.call_types[name] = node.modname.split('.')[0]
        except:
            ExceptionHandler.handle(self, node)

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether hyperparameters are set.

        In strict mode, all hyperparameters should be set.
        In non-strict mode, function calls to learning functions should either contain all
        hyperparameters defined in HYPERPARAMETERS_MAIN or have at least one hyperparameter defined.

        :param node: Node which is visited.
        """
        try:
            if(
                hasattr(node, "func")
                and hasattr(node.func, "name")
            ):
                self.hyperparameter_in_class(node, node.func.name)
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

    def hyperparameter_in_class(self, node: astroid.Call, function_name: str):
        """Cheches whether the required hyperparameters are used in the class."""
        if (
            function_name in self.HYPERPARAMETERS_MAIN
            and len(node.args) == 0
        ):
            self.add_message(self.MESSAGE, node=node)
            # if function_name not in self.count_dict:
            #     self.count_dict[function_name] = {}
            # else:
            #     for kw in node.keywords:
            #         if kw not in self.count_dict:
            #             self.count_dict[function_name][kw.arg] = 1
            #         else:
            #             self.count_dict[function_name][kw.arg] += 1

    # def leave_module(self, module: astroid.Module):
    #     print(self.count_dict)
