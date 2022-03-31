"""Checker which checks whether self.net() is used to forward the input into the network in PyTorch instead of self.net.forward()."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class ForwardPytorchChecker(BaseChecker):
    """Checker which checks whether self.net() is used to forward the input into the network in PyTorch instead of self.net.forward()."""

    __implements__ = IAstroidChecker

    name = "forward-pytorch"
    priority = -1
    msgs = {
        "W5515": (
            "The self.net.forward() is used in the code rather than self.net().",
            "forward-pytorch",
            "It is recommended to use self.net() rather than self.net.forward() in PyTorch code."
        )
    }
    options = ()

    def visit_call(self, call_node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rule in this checker.
        :param call_node: The node which is visited.
        """
        if(
            hasattr(call_node.func, "attrname")
            and call_node.func.attrname == "forward"
        ):
            self.add_message("forward-pytorch", node=call_node)
