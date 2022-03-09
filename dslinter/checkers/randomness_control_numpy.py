"""Checker which checks whether random seed is set in numpy"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid

from dslinter.utils.randomness_control_helper import _check_main_module


class RandomnessControlNumpyChecker(BaseChecker):
    """Checker which checks whether random seed is set in numpy"""
    __implements__ = IAstroidChecker

    name = "randomness-control-numpy"
    priority = -1
    msgs = {
        "W5564": (
            "np.seed() is not set in numpy program",
            "randomness-control-numpy",
            "np.seed() should be set in numpy program for reproducible result"
        )
    }
    options = ()

    _import_numpy = False
    _has_manual_seed = False

    options = (
        (
            "no_main_module_check_randomness_control_numpy",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Check every module whether tf.random.set_seed() is used.",
            },
        ),
    )

    def visit_import(self, node: astroid.Import):
        """
        Check whether there is a numpy import.
        :param node: import node
        """
        for name, _ in node.names:
            if name == "numpy":
                self._import_numpy = True

    def visit_module(self, module: astroid.Module):
        """
        Check whether there is a rule violation.
        :param module:
        """
        _is_main_module = _check_main_module(module)
        if self.config.no_main_module_check_randomness_control_numpy is False and _is_main_module is False:
            return

        for node in module.body:
            if isinstance(node, astroid.nodes.Expr) and hasattr(node, "value"):
                call_node = node.value
                if(
                    hasattr(call_node, "func")
                    and hasattr(call_node.func, "attrname")
                    and call_node.func.attrname == "seed"
                    and hasattr(call_node.func.expr, "attrname")
                    and call_node.func.expr.attrname == "random"
                    and hasattr(call_node.func.expr, "expr")
                    and hasattr(call_node.func.expr.expr, "name")
                    and call_node.func.expr.expr.name in ["np", "numpy"]
                ):
                    self._has_manual_seed = True

        if(
            self._import_numpy is True
            and self._has_manual_seed is False
        ):
            self.add_message("randomness-control-numpy", node = module)
