import traceback
from typing import List

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.ast import AssignUtil


class PCAScalerChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "pca-scaler"
    priority = -1
    msgs = {
        "W5508": (
            "Scaler is not used before PCA",
            "pca scaler checker",
            "To ensure a good result, use feature scaling before Principle Component Analysis."
        ),
    }
    options = ()

    PIPELINE = [
        "make_pipeline",
        "Pipeline",
    ]

    PCA = ["PCA","KernelPCA","SparsePCA","IncrementalPCA",]

    SCALER = ["RobustScaler", "StandardScaler", "MaxAbsScaler", "MinMaxScaler",]

    LEARNING_FUNCTIONS: List[str] = [
        "fit",
        "fit_transform",
        "transform",
    ]

    Variables = []


    def visit_call(self, node: astroid.Call):
        try:
            # If there is no scaler before a pca, rule is violated.
            if (
                node.func is not None
                and hasattr(node.func, "name")
                and node.func.name in self.PIPELINE
                and node.args is not None
            ):
                hasPCA = False
                hasScaler = False
                for arg in node.args:
                    if isinstance(arg, astroid.Call):
                        if PCAScalerChecker._call_initiates_scaler(arg):
                            hasScaler = True
                        if PCAScalerChecker._call_initiates_pca(arg):
                            hasPCA = True
                            break
                    if isinstance(arg, astroid.node_classes.List):
                        for kid in arg.get_children():
                            for item in kid.get_children():
                                if isinstance(item, astroid.Call):
                                    if PCAScalerChecker._call_initiates_scaler(item):
                                        hasScaler=True
                                    if PCAScalerChecker._call_initiates_pca(item):
                                        hasPCA=True
                            if hasPCA == True:
                                    break
                if hasPCA == True and hasScaler==False:
                    self.add_message("pca scaler checker", node=node)

            if (
                    node.func is not None
                    and hasattr(node.func, "attrname")
                    and node.func.attrname in self.LEARNING_FUNCTIONS
                    and self._expr_is_pca(node.func.expr)
                    and node.args is not None
            ):
                hasPCA = True
                for arg in node.args:
                    # print(arg)
                    if isinstance(arg, astroid.Name):
                        values = AssignUtil.assignment_values(arg)
                        for value in values:
                            if (
                                    value.func is not None
                                    and hasattr(node.func, "attrname")
                                    and node.func.attrname in self.LEARNING_FUNCTIONS
                                    and self._expr_is_scaler(value.func.expr)
                            ):
                                hasScaler=True
                if hasPCA == True and hasScaler==False:
                    self.add_message("pca scaler checker", node=node)


        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)
            traceback.print_exc()

    @staticmethod
    def _call_initiates_pca(call: astroid.Call) -> bool:
        """
        Evaluate whether a Call node is initiating an pca.

        :param call: Call to evaluate.
        :return: True when an estimator is initiated.
        """
        return (
            call.func is not None
            and hasattr(call.func, "name")
            and call.func.name in PCAScalerChecker.PCA
        )

    @staticmethod
    def _call_initiates_scaler(call: astroid.Call) -> bool:
        """
        Evaluate whether a Call node is initiating an scaler.

        :param call: Call to evaluate.
        :return: True when an estimator is initiated.
        """
        return (
            call.func is not None
            and hasattr(call.func, "name")
            and call.func.name in PCAScalerChecker.SCALER
        )

    @staticmethod
    def _expr_is_pca(expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is an estimator.

        :param expr: Expression to evaluate.
        :return: True when the expression is an estimator.
        """
        if isinstance(expr, astroid.Call) and PCAScalerChecker._call_initiates_pca(expr):
            return True

        # If expr is a Name, check whether that name is assigned to an estimator.
        if isinstance(expr, astroid.Name):
            values = AssignUtil.assignment_values(expr)
            for value in values:
                if PCAScalerChecker._expr_is_pca(value):
                    return True
        return False

    @staticmethod
    def _expr_is_scaler(expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is an estimator.

        :param expr: Expression to evaluate.
        :return: True when the expression is an estimator.
        """
        if isinstance(expr, astroid.Call) and PCAScalerChecker._call_initiates_scaler(expr):
            return True

        # If expr is a Name, check whether that name is assigned to an estimator.
        if isinstance(expr, astroid.Name):
            values = AssignUtil.assignment_values(expr)
            for value in values:
                if PCAScalerChecker._expr_is_scaler(value):
                    return True
        return False