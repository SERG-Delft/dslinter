"""Checker which checks rules for excessive hyperparameter precision."""
import traceback
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.resources import Resources

class ExcessiveHyperparameterPrecision(BaseChecker):
    """Checker which checks rules for excessive hyperparameter precision."""

    __implements__ = IAstroidChecker

    name = "excessive-hyperparameter-precision"
    priority = -1
    msgs = {
        "W5507": (
            "excessive hyperparameter precision shouldn't be used in the project",
            "excessive hyperparameter precision",
            "excessive hyperparameter precision might suggest over-tuning"
        ),
    }
    options = ()

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
                        if type(keyword.value.value) == float and len(keyword.value.as_string().split(".")[1]) > 2 :
                            self.add_message("excessive hyperparameter precision", node=node)
        except:
            ExceptionHandler.handle(self, node)
            traceback.print_exc()
