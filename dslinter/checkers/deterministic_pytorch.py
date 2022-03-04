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
            "torch.use_deterministic_algorithm()  should be set to True \
            during development process for reproducible result."
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
        for name, _ in node.names:
            if name == "torch":
                self._import_pytorch = True

    def visit_module(self, module: astroid.Module):
        """
        Check whether use_deterministic_algorithms option is used.
        :param node: call node
        """
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
            self.add_message("deterministic-pytorch", node = module)
