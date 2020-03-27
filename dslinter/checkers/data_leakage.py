"""Checker which checks rules for preventing data leakage between training and test data."""
from typing import List, Union

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.util.ast import ASTUtil


class DataLeakageChecker(BaseChecker):
    """Checker which checks rules for preventing data leakage between training and test data."""

    __implements__ = IAstroidChecker

    name = "data-leakage"
    priority = -1
    msgs = {
        "W5601": (
            "scikit-learn estimator not used in a pipeline." "sk-pipeline",
            "All scikit-learn estimators should be used inside pipelines, to prevent data leakage \
             between training and test data.",
        ),
    }
    options = ()

    LEARNING_FUNCTIONS: List[str] = [
        "fit",
        "fit_predict",
        "fit_transform",
        "predict",
        "score",
        "transform",
    ]
    LEARNING_CLASSES: List[str] = ["KMeans"]  # TODO: Read the learning classes from pickle.

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rules in this checker.

        :param node: The node which is visited.
        """
        # If the learning function is called on a learning class, rule is violated.
        if (
            node.func is not None
            and hasattr(node.func, "attrname")
            and node.func.attrname in self.LEARNING_FUNCTIONS
            and self._expr_is_learning_class(node.func.expr)
        ):
            self.add_message("sk-pipeline", node=node)

    def _expr_is_learning_class(self, expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is a learning class.

        :param expr: Expression to evaluate.
        :return: True when the expression is a learning class.
        """
        if isinstance(expr, astroid.Call) and self._call_initiates_learning_class(expr):
            return True

        # If expr is a Name, check whether the assignment can be found
        # and the name is assigned a learning class.
        if isinstance(expr, astroid.Name):
            body_block = ASTUtil.search_body(expr)
            for child in body_block:
                if (
                    isinstance(child, astroid.Assign)
                    or isinstance(child, astroid.AnnAssign)
                    and self._learning_class_assigned(child)
                ):
                    return True
        return False

    def _call_initiates_learning_class(self, call: astroid.Call) -> bool:
        """
        Evaluate whether a Call node is initiating a learning class.

        :param call: Call to evaluate.
        :return: True when a learning class is initiated.
        """
        return (
            call.func is not None
            and hasattr(call.func, "name")
            and call.func.name in self.LEARNING_CLASSES
        )

    def _learning_class_assigned(self, assign: Union[astroid.Assign, astroid.AnnAssign]) -> bool:
        """
        Evaluate whether a learning class is assigned.

        :param assign: Assign to evaluate.
        :return: True when a learning class is assigned.
        """
        if isinstance(assign, astroid.Assign):
            for target in assign.targets:
                if isinstance(target.value, astroid.Call) and self._call_initiates_learning_class(
                    target.value
                ):
                    return True
        if (
            isinstance(assign, astroid.AnnAssign)
            and isinstance(assign.target.value, astroid.Call)
            and self._call_initiates_learning_class(assign.target.value)
        ):
            return True
        return False
