"""Checker which checks rules for controlling randomness."""
from typing import List
import traceback
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.resources import Resources


class ControllingRandomness(BaseChecker):
    """Checker which checks rules for controlling randomness."""

    __implements__ = IAstroidChecker

    name = "controlling-randomness"
    priority = -1
    msgs = {
        "W5506": (
            "'random_state=None' shouldn't be used in estimators or cross-validation splitters, it indicates improper randomness control",
            "controlling randomness",
            "For reproducible results across executions, remove any use of random_state=None."
        ),
    }
    options = ()

    SPLITTER_FUNCTIONS: List[str] = [
        "make_classification",
        "check_cv",
        "train_test_split",
    ]

    SPLITTER_CLASSES = [
        "GroupKFold",
        "GroupShuffleSplit",
        "KFold",
        "LeaveOneGroupOut",
        "LeavePGroupsOut",
        "LeaveOneOut",
        "LeavePOut",
        "PredefinedSplit",
        "RepeatedKFold",
        "RepeatedStratifiedKFold",
        "ShuffleSplit",
        "StratifiedKFold",
        "StratifiedShuffleSplit",
        "TimeSeriesSplit"
    ]

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rules in this checker.

        :param node: The node which is visited.
        """

        estimators_all = Resources.get_hyperparameters()
        try:
            if (
                hasattr(node, "func")
                and hasattr(node.func, "name")
                and hasattr(node, "keywords")
                and (node.func.name in self.SPLITTER_FUNCTIONS or node.func.name in self.SPLITTER_CLASSES or node.func.name in estimators_all)
                and node.keywords is not None
            ):
                for keyword in node.keywords:
                    if (keyword.arg == "random_state" and keyword.value.as_string() == "None"):
                        self.add_message("controlling randomness", node=node)
        except:
            ExceptionHandler.handle(self, node)
            traceback.print_exc()
