"""Checker which checks rules for controlling randomness."""
from typing import List
import traceback
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.util.exception_handler import ExceptionHandler


class ControllingRandomness(BaseChecker):
    """Checker which checks rules for controlling randomness."""

    __implements__ = IAstroidChecker

    name = "controlling-randomness"
    priority = -1
    msgs = {
        "W5506": (
            "'random_state=None' shouldn't be used in estimators or cross-validation splitters",
            "controlling randomness",
            "For reproducible results across executions, remove any use of random_state=None."
        ),
    }
    options = ()

    FUNCTIONS: List[str] = [
        "make_classification",
        "train_test_split",
    ]

    CLASSES = [
        "KFold",
        "SGDClassifier",
        "RandomForestClassifier",
    ]

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rules in this checker.

        :param node: The node which is visited.
        """
        try:
            if (
                hasattr(node, "func")
                and hasattr(node.func, "name")
                and hasattr(node, "keywords")
                and (node.func.name in self.FUNCTIONS or node.func.name in self.CLASSES)
                and node.keywords is not None
            ):
                for keyword in node.keywords:
                    if (keyword.arg == "random_state" and keyword.value.as_string() == "None"):
                        self.add_message("controlling randomness", node=node)
        except:
            ExceptionHandler.handle(self, node)
            traceback.print_exc()


