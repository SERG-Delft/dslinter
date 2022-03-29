import pdb

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class GradientClearPytorchChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "gradient-clear-pytorch"
    priority = -1
    msgs = {
        "": (
            "gradient-clear-pytorch",
            "gradient-clear-pytorch",
            "gradient-clear-pytorch"
        )
    }
    options = ()

    def visit_for(self, for_node: astroid.For):
        _has_zero_grad = False
        _has_backward = False
        _has_step = False
        for n in for_node.body:
            if(
                isinstance(n, astroid.Expr)
                and hasattr(n.value, "func")
                and hasattr(n.value.func, "attrname")
            ):
                if n.value.func.attrname == "zero_grad":
                    _has_zero_grad = True
                if n.value.func.attrname == "backward":
                    _has_backward = True
                if n.value.func.attrname == "step":
                    _has_step = True
        if _has_backward is True and _has_step is True and _has_zero_grad is False:
            self.add_message("gradient-clear-pytorch", node=for_node)

