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
        "W5512": (
            "The variable in tf.log() isn't wrapped with tf.clip().",
            "missing-mask-tensorflow",
            "Add a mask for possible invalid values. For example, developers should wrap the argument for tf.log() with tf.clip() to avoid the argument turning to zero."
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
        if(
            hasattr(node.func, "attrname")
            and node.func.attrname == "log"
            and hasattr(node.func, "expr")
            and hasattr(node.func.expr, "name")
            and node.func.expr.name in ["tf", "tensorflow"]
        ):
            _has_log = True
        if(
            hasattr(node, "args")
            and len(node.args) > 0
            and hasattr(node.args[0], "func")
            and hasattr(node.args[0].func, "attrname")
            and node.args[0].func.attrname == "clip_by_value"
        ):
            _has_mask = True

        if _has_log is True and _has_mask is False:
            self.add_message(msgid="missing-mask-tensorflow", node=node)
