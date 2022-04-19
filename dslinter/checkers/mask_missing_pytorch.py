"""Checker which checks whether there are possible invalid value unmasked."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class MaskMissingPytorchChecker(BaseChecker):
    """Checker which checks whether there are possible invalid value unmasked."""

    __implements__ = IAstroidChecker

    name = "missing-mask-pytorch"
    priority = -1
    msgs = {
        "W5511": (
            "The variable in torch.log() isn't wrapped with torch.clip() or torch.clamp().",
            "missing-mask-pytorch",
            "Add a mask for possible invalid values. For example, developers should wrap the argument for torch.log() with torch.clip() to avoid the argument turning to zero."
        )
    }

    options = ()

    def visit_call(self, node: astroid.Call):
        """
        Visit call node to see whether there are rules violations.
        :param node:
        :return:
        """
        # if log is call but no mask outside of it, it violate the rule
        _has_log = False
        _has_mask = False
        if (
            hasattr(node.func, "attrname")
            and node.func.attrname == "log"
            and hasattr(node.func, "expr")
            and hasattr(node.func.expr, "name")
            and node.func.expr.name == "torch"
        ):
            _has_log = True
        if(
            hasattr(node, "args")
            and len(node.args) > 0
            and hasattr(node.args[0], "func")
            and hasattr(node.args[0].func, "attrname")
            and node.args[0].func.attrname in ["clip", "clamp"]
        ):
            _has_mask = True

        if _has_log is True and _has_mask is False:
            self.add_message(msgid="missing-mask-pytorch", node=node)
