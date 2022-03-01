"""Checker which checkes whether random seed is set in tensorflow"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid


class RandomnessControllingTensorflowChecker(BaseChecker):
    """Checker which checks whether random seed is set in tensorflow"""
    __implements__ = IAstroidChecker

    name = "randomness-control-tensorflow"
    priority = -1
    msgs = {
        "W5572" : (
            "tf.random.set_seed() is not set in tensorflow program",
            "randomness-control-tensorflow",
            "tf.random.set_seed() should be set in tensorflow program for reproducible result"
        )
    }
    options = ()

    _import_tensorflow = False
    _has_manual_seed = False

    def visit_import(self, node: astroid.Import):
        """
        Check whether there is a tensorflow import.
        :param node: import node
        """
        for name, _ in node.names:
            if name == "tensorflow":
                self._import_tensorflow = True

    def visit_call(self, node: astroid.Call):
        """
        Check whether there is a rule violation.
        :param node:
        """
        if(
            hasattr(node, "func")
            and hasattr(node.func, "attrname")
            and node.func.attrname == "set_seed"
            and hasattr(node.func.expr, "attrname")
            and node.func.expr.attrname == "random"
            and hasattr(node.func.expr, "expr")
            and hasattr(node.func.expr.expr, "name")
            and node.func.expr.expr.name in ["tf", "tensorflow"]
        ):
            self._has_manual_seed = True

        if(
            self._import_tensorflow is True
            and self._has_manual_seed is False
        ):
            self.add_message("randomness-control-tensorflow", node = node)
