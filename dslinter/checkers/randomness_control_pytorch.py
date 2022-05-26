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

    def visit_module(self, module: astroid.Module):
        """
        Check whether there is a rule violation.
        :param module:
        """
        try:
            _import_pytorch = False
            _has_pytorch_manual_seed = False

            # if the user wants to only check main module, but the current file is not main module, just return
            _is_main_module = check_main_module(module)
            if self.config.no_main_module_check_randomness_control_pytorch is False and _is_main_module is False:
                return

            # traverse over the node in the module
            for node in module.body:
                if isinstance(node, astroid.Import):
                    if _import_pytorch is False:
                        _import_pytorch = has_import(node, "torch")

                if isinstance(node, astroid.nodes.Expr):
                    if _has_pytorch_manual_seed is False:
                        _has_pytorch_manual_seed = self._check_pytorch_manual_seed_in_expr_node(node)

                if isinstance(node, astroid.nodes.FunctionDef):
                    for nod in node.body:
                        if isinstance(nod, astroid.nodes.Expr):
                            if _has_pytorch_manual_seed is False:
                                _has_pytorch_manual_seed = self._check_pytorch_manual_seed_in_expr_node(nod)

            # check if the rules are violated
            if(
                _import_pytorch is True
                and _has_pytorch_manual_seed is False
            ):
                self.add_message("randomness-control-pytorch", node=module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    @staticmethod
    def _check_pytorch_manual_seed_in_expr_node(expr_node: astroid.Expr):
        if hasattr(expr_node, "value"):
            call_node = expr_node.value
            return RandomnessControlPytorchChecker._check_pytorch_manual_seed_in_call_node(call_node)

    @staticmethod
    def _check_pytorch_manual_seed_in_call_node(call_node: astroid.Call):
        if(
            hasattr(call_node, "func")
            and hasattr(call_node.func, "attrname")
            and call_node.func.attrname == "manual_seed"
        ):
            return True
        return False
