"""Checker which checks rules for excessive hyperparameter precision."""
import traceback
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.resources import Resources

import decimal

class ExcessiveHyperparameterPrecision(BaseChecker):
    """Checker which checks rules for excessive hyperparameter precision."""

    __implements__ = IAstroidChecker

    name = "excessive-hyperparameter-precision"
    priority = -1
    msgs = {
        "W5507": (
            "excessive hyperparameter precision might suggest over-tuning",
            "excessive hyperparameter precision",
            "excessive hyperparameter precision might suggest over-tuning"
        ),
    }
    options = ()

    highPrecisionParameters=["tol"]
    highPrecisionCombinations={"MLPRegressor":["alpha"]}

    precisionThreshold = 3

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rules in this checker.

        :param node: The node which is visited.
        """
        try:
            try:
                function_name = node.func.name
            except AttributeError:
                return

            hyperparams_all = Resources.get_hyperparameters()
            if function_name in hyperparams_all:
                if(node.keywords is not None):
                    for keyword in node.keywords:
                        if(
                            function_name in self.highPrecisionCombinations
                            and keyword.arg in self.highPrecisionCombinations[function_name]
                        ):
                            continue
                        if (
                                keyword.arg not in self.highPrecisionParameters
                                and hasattr(keyword, "value")
                                and hasattr(keyword.value, "value")
                                and type(keyword.value.value) == float
                                and abs(decimal.Decimal(keyword.value.as_string()).as_tuple().exponent) > self.precisionThreshold
                        ):
                            self.add_message("excessive hyperparameter precision", node=node)
        except:
            ExceptionHandler.handle(self, node)
            traceback.print_exc()