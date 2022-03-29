"""Checker which checks whether training mode and evaluation mode is toggling properly in pytorch code."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class ModeTogglingPytorchChecker(BaseChecker):
    """Checker which checks whether training mode and evaluation mode is toggling properly in pytorch code."""

    __implements__ = IAstroidChecker

    name = "mode-toggling-pytorch"
    priority = -1
    msgs = {
        "": (
            "The training mode did not toggle back in time in the pytorch code.",
            "mode-toggling-pytorch",
            "Developers should call the training mode in the right place to avoid forgetting to switch back to the training mode after the inference step."
        )
    }
    options = ()

    def visit_for(self, for_node: astroid.For):
        """
        When a For node is visited, check whether it violated the rule in this checker.
        :param for_node: The node which is visited.
        """
        _has_train = False
        _has_eval = False
        for node in for_node.body:
            if isinstance(node, astroid.Expr):
                if(
                    isinstance(node.value, astroid.Call)
                    and hasattr(node.value.func, "attrname")
                    and node.value.func.attrname == "train"
                ):
                    _has_train = True
                if(
                    isinstance(node.value, astroid.Call)
                    and hasattr(node.value.func, "attrname")
                    and node.value.func.attrname == "eval"
                ):
                    _has_eval = True
            if isinstance(node, astroid.If):
                for if_node in node.body:
                    if(
                        isinstance(if_node, astroid.Expr)
                        and isinstance(if_node.value, astroid.Call)
                        and hasattr(if_node.value.func, "attrname")
                        and if_node.value.func.attrname == "eval"
                    ):
                        _has_eval = True

        if _has_eval != _has_train:
            self.add_message("mode-toggling-pytorch", node=for_node)
