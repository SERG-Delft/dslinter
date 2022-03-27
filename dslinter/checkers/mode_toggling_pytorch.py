import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class ModeTogglingPytorchChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "mode-toggling-pytorch"
    priority = -1
    msgs = {
        "": (
            "mode-toggling-pytorch",
            "mode-toggling-pytorch",
            "mode-toggling-pytorch"
        )
    }
    options = ()

    def visit_for(self, for_node: astroid.For):
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
