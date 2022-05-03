"""Checker which checks whether random seed is set in pytorch"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.randomness_control_helper import check_main_module, has_import


class RandomnessControlPytorchChecker(BaseChecker):
    """Checker which checks whether random seed is set in pytorch"""
    __implements__ = IAstroidChecker

    name = "randomness-control-pytorch"
    priority = -1
    msgs = {
        "W5511": (
            "The torch.manual_seed() is not set in PyTorch program",
            "randomness-control-pytorch",
            "The torch.manual_seed() should be set in PyTorch program for reproducible result"
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
        try:
            if self._import_pytorch is False:
                self._import_pytorch = has_import(node, "torch")
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, node)

    def visit_module(self, module: astroid.Module):
        """
        Check whether there is a rule violation.
        :param module:
        """
        try:
            _is_main_module = check_main_module(module)
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
                self.add_message("randomness-control-pytorch", node=module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

