"""Checker which checkes whether random seed is set in numpy"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid


class RandomnessControllingNumpyChecker(BaseChecker):
    """Checker which checks whether random seed is set in numpy"""
    __implements__ = IAstroidChecker

    name = "randomness-control-numpy"
    priority = -1
    msgs = {
        "W5574" : (
            "tf.random.set_seed() is not set in numpy program",
            "randomness-control-numpy",
            "tf.random.set_seed() should be set in numpy program for reproducible result"
        )
    }
    options = ()

    _import_numpy = False
    _has_manual_seed = False

    def visit_import(self, node: astroid.Import):
        """
        Check whether there is a numpy import.
        :param node: import node
        """
        for name, _ in node.names:
            if name == "numpy":
                self._import_numpy = True

    def visit_call(self, node: astroid.Call):
        """
        Check whether there is a rule violation.
        :param node:
        """
        if(
            hasattr(node, "func")
            and hasattr(node.func, "attrname")
            and node.func.attrname == "seed"
            and hasattr(node.func.expr, "attrname")
            and node.func.expr.attrname == "random"
            and hasattr(node.func.expr, "expr")
            and hasattr(node.func.expr.expr, "name")
            and node.func.expr.expr.name in ["np", "numpy"]
        ):
            self._has_manual_seed = True

        if(
            self._import_numpy is True
            and self._has_manual_seed is False
        ):
            self.add_message("randomness-control-numpy", node = node)

