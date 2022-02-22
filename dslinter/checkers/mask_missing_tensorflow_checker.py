"""Checker which checks whether there are possible invalid value unmasked."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class MaskMissingTensorflowChecker(BaseChecker):
    """Checker which checks whether there are possible invalid value unmasked."""

    __implements__ = IAstroidChecker

    name = "missing-mask-tensorflow"
    priority = -1
    msgs = {
        "W5561": (
            "missing-mask-tensorflow",
            "missing-mask-tensorflow",
            "missing-mask-tensorflow"
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
        # pdb.set_trace()
        __has_log = False
        __has_mask = False
        if node.func.attrname == "log":
            __has_log = True
        if(
            hasattr(node, "args")
            and len(node.args) > 0
            and hasattr(node.args[0], "func")
            and hasattr(node.args[0].func, "attrname")
            and node.args[0].func.attrname == "clip_by_value"
        ):
            __has_mask = True

        if(__has_log is True and __has_mask is False):
            self.add_message(msgid= "missing-mask-tensorflow", node = node)
