"""Checker which checks whether random seed is set in pytorch"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid

from dslinter.utils.randomness_control_helper import _check_main_module


class RandomnessControlPytorchChecker(BaseChecker):
    """Checker which checks whether random seed is set in pytorch"""
    __implements__ = IAstroidChecker

    name = "randomness-control-pytorch"
    priority = -1
    msgs = {
        "W5563": (
            "torch.manual_seed() is not set in pytorch program",
            "randomness-control-pytorch",
            "torch.manual_seed() should be set in pytorch program for reproducible result"
        )
    }

    options = (
        (
            "no_main_module_check_randomness_control_pytorch",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Check every module whether torch.manual_seed() is used.",
            },
        ),
    )

    _import_pytorch = False
    _has_manual_seed = False

    def visit_import(self, node: astroid.Import):
        """
        Check whether there is a pytorch import.
        :param node: import node
        """
        for name, _ in node.names:
            if name == "torch":
                self._import_pytorch = True

    def visit_module(self, module: astroid.Module):
        """
        Check whether there is a rule violation.
        :param module:
        """

        _is_main_module = _check_main_module(module)
        if self.config.no_main_module_check_randomness_control_pytorch is False and _is_main_module is False:
            return

        for node in module.body:
            if isinstance(node, astroid.nodes.Expr) and hasattr(node, "value"):
                call_node = node.value
                if(
                    hasattr(call_node, "func")
                    and hasattr(call_node.func, "attrname")
                    and call_node.func.attrname == "manual_seed"
                ):
                    self._has_manual_seed = True

        if(
            self._import_pytorch is True
            and self._has_manual_seed is False
        ):
            self.add_message("randomness-control-pytorch", node = module)

