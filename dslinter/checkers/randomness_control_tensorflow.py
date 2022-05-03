"""Checker which checks whether random seed is set in tensorflow"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.randomness_control_helper import check_main_module, has_import


class RandomnessControlTensorflowChecker(BaseChecker):
    """Checker which checks whether random seed is set in tensorflow"""
    __implements__ = IAstroidChecker

    name = "randomness-control-tensorflow"
    priority = -1
    msgs = {
        "W5510": (
            "The tf.random.set_seed() is not set in TensorFlow program",
            "randomness-control-tensorflow",
            "The tf.random.set_seed() should be set in TensorFlow program for reproducible result"
        )
    }
    options = (
        (
            "no_main_module_check_randomness_control_tensorflow",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Check every module whether tf.random.set_seed() is used.",
            },
        ),
    )

    _import_tensorflow = False
    _has_manual_seed = False

    def visit_import(self, node: astroid.Import):
        """
        Check whether there is a tensorflow import.
        :param node: import node
        """
        try:
            if self._import_tensorflow is False:
                self._import_tensorflow = has_import(node, "tensorflow")
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, node)

    def visit_module(self, module: astroid.Module):
        """
        Check whether there is a rule violation.
        :param module:
        """
        try:
            _is_main_module = check_main_module(module)
            if self.config.no_main_module_check_randomness_control_tensorflow is False and _is_main_module is False:
                return

            for node in module.body:
                if isinstance(node, astroid.nodes.Expr) and hasattr(node, "value"):
                    call_node = node.value
                    if(
                        hasattr(call_node, "func")
                        and hasattr(call_node.func, "attrname")
                        and call_node.func.attrname == "set_seed"
                        and hasattr(call_node.func.expr, "attrname")
                        and call_node.func.expr.attrname == "random"
                        and hasattr(call_node.func.expr, "expr")
                        and hasattr(call_node.func.expr.expr, "name")
                        and call_node.func.expr.expr.name in ["tf", "tensorflow"]
                    ):
                        self._has_manual_seed = True

            if(
                self._import_tensorflow is True
                and self._has_manual_seed is False
            ):
                self.add_message("randomness-control-tensorflow", node=module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)
