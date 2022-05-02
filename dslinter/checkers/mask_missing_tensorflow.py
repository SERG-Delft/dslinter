"""Checker which checks whether there are possible invalid value unmasked."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.type_inference import TypeInference


class MaskMissingTensorflowChecker(BaseChecker):
    """Checker which checks whether there are possible invalid value unmasked."""

    __implements__ = IAstroidChecker

    name = "missing-mask-tensorflow"
    priority = -1
    msgs = {
        "W5513": (
            "The variable in tf.log() isn't wrapped with tf.clip_by_value().",
            "missing-mask-tensorflow",
            "Add a mask for possible invalid values. For example, developers should wrap the argument for tf.log() with tf.clip() to avoid the argument turning to zero."
        )
    }

    options = ()

    _variables_with_processing_operation = {}

    def visit_module(self, module: astroid.Module):
        try:
            self._variables_with_processing_operation = TypeInference.infer_variable_full_types(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_call(self, call_node: astroid.Call):
        """
        Visit call node to see whether there are rules violations.
        :param call_node:
        :return:
        """
        # if log is call but no mask outside of it, it violate the rule
        try:
            _has_log = False
            _has_mask = False
            if(
                hasattr(call_node.func, "attrname")
                and call_node.func.attrname == "log"
                and hasattr(call_node.func, "expr")
                and hasattr(call_node.func.expr, "name")
                and call_node.func.expr.name in ["tf", "tensorflow"]
            ):
                _has_log = True
            if(
                hasattr(call_node, "args")
                and len(call_node.args) > 0
                and hasattr(call_node.args[0], "func")
                and hasattr(call_node.args[0].func, "attrname")
                and call_node.args[0].func.attrname == "clip_by_value"
            ):
                _has_mask = True
            if(
                hasattr(call_node, "args")
                and len(call_node.args) > 0
                and hasattr(call_node.args[0], "name")
                and call_node.args[0].name in self._variables_with_processing_operation
                and "tf.clip_by_value" in self._variables_with_processing_operation[call_node.args[0].name]
            ):
                _has_mask = True

            if _has_log is True and _has_mask is False:
                self.add_message(msgid="missing-mask-tensorflow", node=call_node)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, call_node)
