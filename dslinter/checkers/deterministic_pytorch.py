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

    def visit_module(self, module: astroid.Module):
        """
        Check whether there is a rule violation.
        :param module:
        """
        try:
            _import_pytorch = False
            _has_deterministic_algorithm_option = False

            # if the user wants to only check main module, but the current file is not main module, just return
            _is_main_module = check_main_module(module)
            if self.config.no_main_module_check_deterministic_pytorch is False and _is_main_module is False:
                return

            # traverse over the node in the module
            for node in module.body:
                if isinstance(node, astroid.Import):
                    if _import_pytorch is False:
                        _import_pytorch = has_import(node, "torch")

                if isinstance(node, astroid.nodes.Expr):
                    if _has_deterministic_algorithm_option is False:
                        _has_deterministic_algorithm_option = self._check_deterministic_algorithm_option_in_expr_node(node)

                if isinstance(node, astroid.nodes.FunctionDef):
                    for nod in node.body:
                        if isinstance(nod, astroid.nodes.Expr):
                            if _has_deterministic_algorithm_option is False:
                                _has_deterministic_algorithm_option = self._check_deterministic_algorithm_option_in_expr_node(nod)

            # check if the rules are violated
            if(
                _import_pytorch is True
                and _has_deterministic_algorithm_option is False
            ):
                self.add_message("deterministic-pytorch", node=module)

        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    @staticmethod
    def _check_deterministic_algorithm_option_in_expr_node(expr_node: astroid.Expr):
        if hasattr(expr_node, "value"):
            call_node = expr_node.value
            return DeterministicAlgorithmChecker._check_deterministic_algorithm_option_in_call_node(call_node)

    @staticmethod
    def _check_deterministic_algorithm_option_in_call_node(call_node: astroid.Call):
        # if torch.use_deterministic_algorithm() is call and the argument is True,
        # set _has_deterministic_algorithm_option to True
        if(
            hasattr(call_node, "func")
            and hasattr(call_node.func, "attrname")
            and call_node.func.attrname == "use_deterministic_algorithms"
            and hasattr(call_node, "args")
            and len(call_node.args) > 0
            and hasattr(call_node.args[0], "value")
            and call_node.args[0].value is True
        ):
            return True
        return False
