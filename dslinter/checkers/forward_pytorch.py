import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class ForwardPytorchChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "forward-pytorch"
    priority = -1
    msgs = {
        "": (
            "forward-pytorch",
            "forward-pytorch",
            "forward-pytorch"
        )
    }
    options = ()

    def visit_call(self, call_node: astroid.Call):
        if(
            hasattr(call_node.func, "attrname")
            and call_node.func.attrname == "forward"
        ):
            self.add_message("forward-pytorch", node=call_node)
