"""Checker which checks whether deterministic algorithm is used."""
import astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker


class DeterministicAlgorithmChecker(BaseChecker):
    """Checker which checks whether deterministic algorithm is used."""

    __implements__ = IAstroidChecker

    name = "deterministic-pytorch"
    priority = -1
    msgs = {
        "W5551":(
            "torch.use_deterministic_algorithm()  is not set to True",
            "deterministic-pytorch",
            "torch.use_deterministic_algorithm()  should be set to True during development process for reproducible result."
        )
    }
    options = ()

    _import_pytorch = False
    _has_deterministic_algorithm_option = False

    def visit_import(self, node: astroid.Import):
        """
        Check whether there is a pytorch import
        :param node: import node
        """
        for name, alias in node.names:
            if name == "torch":
                self._import_pytorch = True

    def visit_call(self, node: astroid.Call):
        """
        Check whether use_deterministic_algorithms option is used.
        :param node: call node
        """
        # if torch.use_deterministic_algorithm() is call and the argument is True, set _has_deterministic_algorithm_option to True
        if(
            hasattr(node, "func")
            and hasattr(node.func, "attrname")
            and node.func.attrname == "use_deterministic_algorithms"
            and hasattr(node, "args")
            and len(node.args) > 0
            and hasattr(node.args[0], "value")
            and node.args[0].value == True
        ):
            self._has_deterministic_algorithm_option = True

        if(
            self._import_pytorch is True
            and self._has_deterministic_algorithm_option is False
        ):
            self.add_message("deterministic-pytorch", node = node)
