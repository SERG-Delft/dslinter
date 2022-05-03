"""Checker which checks rules for preventing data leakage between training and test data."""
from typing import List

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.utils.ast import AssignUtil
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.resources import Resources


class DataLeakageScikitLearnChecker(BaseChecker):
    """Checker which checks rules for preventing data leakage between training and test data."""

    __implements__ = IAstroidChecker

    name = "data-leakage-scikitlearn"
    priority = -1
    msgs = {
        "W5518": (
            "There are both preprocessing and estimation operations in the code, but they are not used in a pipeline.",
            "data-leakage-scikitlearn",
            "Scikit-learn preprocessors and estimators should be used inside pipelines, to prevent data leakage between training and test data.",
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
        "SelectKBest",
    ]

    def visit_call(self, call_node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rules in this checker.

        :param call_node: The node which is visited.
        """
        try:
            # If the learning function is called on an estimator, rule is violated.
            if (
                call_node.func is not None
                and hasattr(call_node.func, "attrname")
                and call_node.func.attrname in self.LEARNING_FUNCTIONS
                and hasattr(call_node.func, "expr")
                and self._expr_is_estimator(call_node.func.expr)
                and hasattr(call_node, "args")
            ):
                has_learning_function = True
                has_preprocessing_function = False
                for arg in call_node.args:
                    if isinstance(arg, astroid.Name):
                        values = AssignUtil.assignment_values(arg)
                        for value in values:
                            if (
                                isinstance(value, astroid.Call)
                                and hasattr(value, "func")
                                and hasattr(value.func, "expr")
                            ):
                                if self._expr_is_preprocessor(value.func.expr):
                                    has_preprocessing_function = True
                if has_learning_function is True and has_preprocessing_function is True:
                    self.add_message("data-leakage-scikitlearn", node=call_node)

        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, call_node)

    @staticmethod
    def _expr_is_estimator(expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is an estimator.

        :param expr: Expression to evaluate.
        :return: True when the expression is an estimator.
        """
        if isinstance(expr, astroid.Call) \
                and DataLeakageScikitLearnChecker._call_initiates_estimator(expr):
            return True

        # If expr is a Name, check whether that name is assigned to an estimator.
        if isinstance(expr, astroid.Name):
            values = AssignUtil.assignment_values(expr)
            for value in values:
                if DataLeakageScikitLearnChecker._expr_is_estimator(value):
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
                and call.func.name in DataLeakageScikitLearnChecker._get_estimator_classes()
        )

    @staticmethod
    def _get_estimator_classes() -> List[str]:
        """
        Get all estimator classes.

        The list contains all learning classes which do something in the
        fit function from sklearn.

        :return: List of estimator classes.
        """
        # pylint: disable = line-too-long
        learning_classes = list(Resources.get_hyperparameters("hyperparameters_scikitlearn_dict.pickle").keys())
        estimator_classes = learning_classes
        assert None not in estimator_classes
        return estimator_classes

    def _call_initiates_preprocessor(self, call: astroid.Call) -> bool:
        """
        Evaluate whether a Call node is initiating an scaler.

        :param call: Call to evaluate.
        :return: True when an estimator is initiated.
        """
        return (
                hasattr(call, "func")
                and hasattr(call.func, "name")
                and call.func.name in self.PREPROCESSING_CLASSES
        )

    def _expr_is_preprocessor(self, expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is an estimator.

        :param expr: Expression to evaluate.
        :return: True when the expression is an estimator.
        """
        if isinstance(expr, astroid.Call) and self._call_initiates_preprocessor(expr):
            return True

        # If expr is a Name, check whether that name is assigned to an estimator.
        if isinstance(expr, astroid.Name):
            values = AssignUtil.assignment_values(expr)
            for value in values:
                if self._expr_is_preprocessor(value):
                    return True
        return False
