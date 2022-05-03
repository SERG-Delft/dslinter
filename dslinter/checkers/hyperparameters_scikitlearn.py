"""Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""
# pylint: disable = line-too-long
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter
from dslinter.checkers.hyperparameters import HyperparameterChecker


class HyperparameterScikitLearnChecker(HyperparameterChecker):
    """Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""

    __implements__ = IAstroidChecker

    name = "hyperparameters-scikitlearn"
    priority = -1
    msgs = {
        "R5506": (
            "Some of the important hyperparameters is not set in the program.",
            "hyperparameters-scikitlearn",
            "For learning algorithms, hyperparameters should be tuned and set.",
        ),
    }

    options = (
        (
            "strict_hyperparameters_scikitlearn",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Force that all parameters of learning algorithms are set.",
            },
        ),
    )

    def __init__(self, linter: PyLinter = HyperparameterChecker):
        super().__init__(linter)
        self.HYPERPARAMETER_RESOURCE = "hyperparameters_scikitlearn_dict.pickle"
        self.MESSAGE = "hyperparameters-scikitlearn"
        self.LIBRARY = "scikitlearn"
        # Main hyperparameters of learning algorithms, as defined in research.
        # Sources:
        # 1. Probst, P., Boulesteix, A. L., & Bischl, B. (2019). Tunability: Importance of
        #   Hyperparameters of Machine Learning Algorithms. Journal of Machine Learning Research,
        #   20(53), 1-32.
        # 2. van Rijn, J. N., & Hutter, F. (2018, July). Hyperparameter importance across datasets.
        #   In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery &
        #   Data Mining (pp. 2367-2376).
        self.HYPERPARAMETERS_MAIN = {
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
