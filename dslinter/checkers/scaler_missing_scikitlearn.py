"""Checker checks whether scaler is added before scaling-sensitive operations."""
import traceback
from typing import List
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.ast import AssignUtil


class ScalerMissingScikitLearnChecker(BaseChecker):
    """Checker checks whether scaler is added before scaling-sensitive operations."""

    __implements__ = IAstroidChecker

    name = "scaler-missing-scikitlearn"
    priority = -1
    msgs = {
        "W5505": (
            "Scaler is not used before scaling-sensitive operation",
            "scaler-missing-scikitlearn",
            "To ensure a good result, use feature scaling before scaling-sensitive operation."
        ),
    }
    options = ()

    PIPELINE = [
        "make_pipeline",
        "Pipeline",
    ]

    SCALING_SENSITIVE_OPERATIONS = [
        "PCA",
        "KernelPCA",
        "SparsePCA",
        "IncrementalPCA",
        "LinearSVC",
        "LinearSVR",
        "NuSVC",
        "NuSVR",
        "OneClassSVM",
        "SVC",
        "SVR",
        "SGDClassifier",
        "SGDOneClassSVM",
        "SGDRegressor",
        "MLPClassifier",
        "MLPRegressor"
    ]

    SCALER = ["RobustScaler", "StandardScaler", "MaxAbsScaler", "MinMaxScaler",]

    LEARNING_FUNCTIONS: List[str] = [
        "fit",
        "fit_transform",
        "transform",
    ]

    Variables = []

    def visit_call(self, node: astroid.Call):
        """
        When a node is visited, add a message if the rule is violated.
        :param node:
        :return:
        """
        try:
            # If there is no scaler before a scaling-sensitive operarion, the rule is violated.
            # If pipeline is used
            if (
                hasattr(node, "func")
                and hasattr(node.func, "name")
                and node.func.name in self.PIPELINE
                and hasattr(node, "args")
            ):
                has_scaling_sensitive_operation = False
                has_scaler = False
                for arg in node.args:
                    if isinstance(arg, astroid.Call):
                        if self._call_initiates_scaler(arg):
                            has_scaler = True
                        if self._call_initiates_scaling_sensitive_operations(arg):
                            has_scaling_sensitive_operation = True
                            break
                if has_scaling_sensitive_operation is True and has_scaler is False:
                    self.add_message("scaler-missing-scikitlearn", node=node)

            # If pipeline is not used and a scaling-sensitive operation is called
            if (
                    hasattr(node, "func")
                    and hasattr(node.func, "attrname")
                    and node.func.attrname in self.LEARNING_FUNCTIONS
                    and hasattr(node.func, "expr")
                    and self._expr_is_scaling_sensitive_operation(node.func.expr)
                    and hasattr(node, "args")
            ):
                has_scaling_sensitive_operation = True
                has_scaler = False
                for arg in node.args:
                    if isinstance(arg, astroid.Name):
                        values = AssignUtil.assignment_values(arg)
                        for value in values:
                            if (
                                isinstance(value, astroid.Call)
                                and hasattr(value, "func")
                                and hasattr(value.func, "expr")
                            ):
                                if self._expr_is_scaler(value.func.expr):
                                    has_scaler = True
                if has_scaling_sensitive_operation is True and has_scaler is False:
                    self.add_message("scaler-missing-scikitlearn", node=node)

        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)
            traceback.print_exc()

    def _call_initiates_scaling_sensitive_operations(self, call: astroid.Call) -> bool:
        """
        Evaluate whether a Call node is initiating an pca.

        :param call: Call to evaluate.
        :return: True when an estimator is initiated.
        """
        return (
                hasattr(call, "func")
                and hasattr(call.func, "name")
                and call.func.name in self.SCALING_SENSITIVE_OPERATIONS
        )

    def _call_initiates_scaler(self, call: astroid.Call) -> bool:
        """
        Evaluate whether a Call node is initiating an scaler.

        :param call: Call to evaluate.
        :return: True when an estimator is initiated.
        """
        return (
                hasattr(call, "func")
                and hasattr(call.func, "name")
                and call.func.name in self.SCALER
        )

    def _expr_is_scaling_sensitive_operation(self, expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is an estimator.

        :param expr: Expression to evaluate.
        :return: True when the expression is an estimator.
        """
        # pylint: disable = line-too-long
        if isinstance(expr, astroid.Call) and self._call_initiates_scaling_sensitive_operations(expr):
            return True

        # If expr is a Name, check whether that name is assigned to an estimator.
        if isinstance(expr, astroid.Name):
            values = AssignUtil.assignment_values(expr)
            for value in values:
                if self._expr_is_scaling_sensitive_operation(value):
                    return True
        return False

    def _expr_is_scaler(self, expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is an estimator.

        :param expr: Expression to evaluate.
        :return: True when the expression is an estimator.
        """
        if isinstance(expr, astroid.Call) and self._call_initiates_scaler(expr):
            return True

        # If expr is a Name, check whether that name is assigned to an estimator.
        if isinstance(expr, astroid.Name):
            values = AssignUtil.assignment_values(expr)
            for value in values:
                if self._expr_is_scaler(value):
                    return True
        return False
