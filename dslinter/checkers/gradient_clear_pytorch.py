"""Checker which checks optimizer.zero_grad() is used when loss_fn.backward() and optimizer.step() are used."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.utils.exception_handler import ExceptionHandler


class GradientClearPytorchChecker(BaseChecker):
    """Checker which checks optimizer.zero_grad() is used when loss_fn.backward() and optimizer.step() are used."""

    __implements__ = IAstroidChecker

    name = "gradient-clear-pytorch"
    priority = -1
    msgs = {
        "W5517": (
            "The optimizer.zero_grad() is not used in pytorch code when loss_fn.backward() and optimizer.step() are used.",
            "gradient-clear-pytorch",
            "The loss_fn.backward() and optimizer.step() should be used together with optimizer.zero_grad() to clear gradients."
        )
    }
    options = ()

    def visit_for(self, for_node: astroid.For):
        """
        When a For node is visited, check whether it violated the rule in this checker.
        :param for_node: The node which is visited.
        """
        try:
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
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, for_node)

