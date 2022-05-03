"""Checker which checks rules for controlling randomness."""
from typing import List
import traceback
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.resources import Resources


class RandomnessControlScikitLLearnChecker(BaseChecker):
    """Checker which checks rules for controlling randomness."""

    __implements__ = IAstroidChecker

    name = "randomness-control-scikitlearn"
    priority = -1
    msgs = {
        "W5509": (
            "The 'random_state' should be set in estimators or cross-validation splitters.",
            "randomness-control-scikitlearn",
            "For reproducible results across executions, set 'random_state'."
        ),
    }
    options = ()

    SPLITTER_FUNCTIONS: List[str] = [
        "make_classification",
        # "check_cv", # no random_state
        "train_test_split",
    ]

    SPLITTER_CLASSES = [
        # "GroupKFold",
        "GroupShuffleSplit",
        "KFold",
        # "LeaveOneGroupOut",
        # "LeavePGroupsOut",
        # "LeaveOneOut",
        # "LeavePOut",
        # "PredefinedSplit",
        "RepeatedKFold",
        "RepeatedStratifiedKFold",
        "ShuffleSplit",
        "StratifiedKFold",
        "StratifiedShuffleSplit",
        # "TimeSeriesSplit"
    ]

    _HYPERPARAMETER_RESOURCE = "hyperparameters_scikitlearn_dict.pickle"
    _estimators_all = Resources.get_hyperparameters(_HYPERPARAMETER_RESOURCE)

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rules in this checker.

        :param node: The node which is visited.
        """

        try:
            if (
                # pylint: disable = R0916
                hasattr(node, "func")
                and hasattr(node, "keywords")
                and hasattr(node.func, "name")
                and (node.func.name in self.SPLITTER_FUNCTIONS
                     or node.func.name in self.SPLITTER_CLASSES)
                     #or node.func.name in self.estimators_all)
            ):
                if node.keywords is not None:
                    _has_random_state_keyword = False
                    for keyword in node.keywords:
                        if keyword.arg == "random_state":
                            _has_random_state_keyword = True
                            if keyword.value.as_string() == "None":
                                self.add_message("randomness-control-scikitlearn", node=node)
                    if _has_random_state_keyword is False:
                        self.add_message("randomness-control-scikitlearn", node=node)

        # pylint: disable = W0702
        except:
            ExceptionHandler.handle(self, node)
            traceback.print_exc()
