"""Checker which checks rules for preventing data leakage between training and test data."""
from typing import List

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.util.ast import AssignUtil
from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.resources import Resources


class DataLeakageChecker(BaseChecker):
    """Checker which checks rules for preventing data leakage between training and test data."""

    __implements__ = IAstroidChecker

    name = "data-leakage"
    priority = -1
    msgs = {
        "W5504": (
            "scikit-learn estimator not used in a pipeline.",
            "sk-pipeline",
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

    PREPROCESSING_CLASSES = [
        "FunctionTransformer",
        "KBinsDiscretizer",
        "KernelCenterer",
        "LabelBinarizer",
        "LabelEncoder",
        "MultiLabelBinarizer",
        "MaxAbsScaler",
        "MinMaxScaler",
        "OneHotEncoder",
        "OrdinalEncoder",
        "PolynomialFeatures",
        "PowerTransformer",
        "QuantileTransformer",
        "RobustScaler",
        "StandardScaler",
    ]

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rules in this checker.

        :param node: The node which is visited.
        """
        try:
            # If the learning function is called on an estimator, rule is violated.
            if (
                node.func is not None
                and hasattr(node.func, "attrname")
                and node.func.attrname in self.LEARNING_FUNCTIONS
                and self._expr_is_estimator(node.func.expr)
            ):
                self.add_message("sk-pipeline", node=node)
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

    @staticmethod
    def _expr_is_estimator(expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is an estimator.

        :param expr: Expression to evaluate.
        :return: True when the expression is an estimator.
        """
        if isinstance(expr, astroid.Call) and DataLeakageChecker._call_initiates_estimator(expr):
            return True

        # If expr is a Name, check whether that name is assigned to an estimator.
        if isinstance(expr, astroid.Name):
            values = AssignUtil.assignment_values(expr)
            for value in values:
                if DataLeakageChecker._expr_is_estimator(value):
                    return True
        return False

    @staticmethod
    def _call_initiates_estimator(call: astroid.Call) -> bool:
        """
        Evaluate whether a Call node is initiating an estimator.

        :param call: Call to evaluate.
        :return: True when an estimator is initiated.
        """
        return (
            call.func is not None
            and hasattr(call.func, "name")
            and call.func.name in DataLeakageChecker._get_estimator_classes()
        )

    @staticmethod
    def _get_estimator_classes() -> List[str]:
        """
        Get all estimator classes.

        The list contains all learning classes and preprocessing classes which do something in the
        fit function from sklearn.

        :return: List of estimator classes.
        """
        learning_classes = list(Resources.get_hyperparameters().keys())
        estimator_classes = learning_classes + DataLeakageChecker.PREPROCESSING_CLASSES
        assert None not in estimator_classes
        return estimator_classes
