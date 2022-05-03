"""Checker which checks whether deterministic algorithm is used."""
import astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.randomness_control_helper import check_main_module, has_import


class DeterministicAlgorithmChecker(BaseChecker):
    """Checker which checks whether deterministic algorithm is used."""

    __implements__ = IAstroidChecker

    name = "deterministic-pytorch"
    priority = -1
    msgs = {
        "W5507": (
            "The torch.use_deterministic_algorithm()  is not used or not set to True",
            "deterministic-pytorch",
            "The torch.use_deterministic_algorithm()  should be used and set to True during development process for reproducible result."
        )
    }

    options = (
        (
            "no_main_module_check_deterministic_pytorch",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Check every module whether torch.use_deterministic_algorithm() is used or set.",
            },
        ),
    )

    _import_pytorch = False
    _has_deterministic_algorithm_option = False

    def visit_import(self, node: astroid.Import):
        """
        Check whether there is a pytorch import
        :param node: import node
        """
        try:
            if self._import_pytorch is False:
                self._import_pytorch = has_import(node, "torch")
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, node)

    def visit_module(self, module: astroid.Module):
        """
        Check whether use_deterministic_algorithms option is used.
        :param module: call node
        """
        try:
            _is_main_module = check_main_module(module)
            if self.config.no_main_module_check_deterministic_pytorch is False and _is_main_module is False:
                return

            # if torch.use_deterministic_algorithm() is call and the argument is True,
            # set _has_deterministic_algorithm_option to True
            for node in module.body:
                if isinstance(node, astroid.nodes.Expr) and hasattr(node, "value"):
                    call_node = node.value
                    if(
                        hasattr(call_node, "func")
                        and hasattr(call_node.func, "attrname")
                        and call_node.func.attrname == "use_deterministic_algorithms"
                        and hasattr(call_node, "args")
                        and len(call_node.args) > 0
                        and hasattr(call_node.args[0], "value")
                        and call_node.args[0].value is True
                    ):
                        self._has_deterministic_algorithm_option = True

            if(
                self._import_pytorch is True
                and self._has_deterministic_algorithm_option is False
            ):
                self.add_message("deterministic-pytorch", node=module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)
