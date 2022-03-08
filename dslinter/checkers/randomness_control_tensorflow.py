"""Checker which checks whether random seed is set in tensorflow"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid


class RandomnessControlTensorflowChecker(BaseChecker):
    """Checker which checks whether random seed is set in tensorflow"""
    __implements__ = IAstroidChecker

    name = "randomness-control-tensorflow"
    priority = -1
    msgs = {
        "W5572": (
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

    def visit_module(self, module: astroid.Module):
        """
        Check whether there is a rule violation.
        :param node:
        """
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
            self.add_message("randomness-control-tensorflow", node = module)
