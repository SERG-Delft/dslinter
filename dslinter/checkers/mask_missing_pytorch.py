"""Checker which checks whether there are possible invalid value unmasked."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.utils.type_inference import TypeInference


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

    _variables_with_processing_operation = {}

    def visit_module(self, module: astroid.Module):
        self._variables_with_processing_operation = TypeInference.infer_variable_full_types(module)

    def visit_call(self, call_node: astroid.Call):
        """
        Visit call node to see whether there are rules violations.
        :param call_node:
        :return:
        """
        # if log is call but no mask outside of it, it violate the rule
        _has_log = False
        _has_mask = False
        if (
            hasattr(call_node.func, "attrname")
            and call_node.func.attrname == "log"
            and hasattr(call_node.func, "expr")
            and hasattr(call_node.func.expr, "name")
            and call_node.func.expr.name == "torch"
        ):
            _has_log = True
        if(
            hasattr(call_node, "args")
            and len(call_node.args) > 0
            and hasattr(call_node.args[0], "func")
            and hasattr(call_node.args[0].func, "attrname")
            and call_node.args[0].func.attrname in ["clip", "clamp"]
        ):
            _has_mask = True
        if(
            hasattr(call_node, "args")
            and len(call_node.args) > 0
            and hasattr(call_node.args[0], "name")
            and call_node.args[0].name in self._variables_with_processing_operation
        ):
            _variable_name = call_node.args[0].name
            _variable_index = self._variables_with_processing_operation[_variable_name].index("torch.log")
            if _variable_index >= 1 and self._variables_with_processing_operation[_variable_name][_variable_index - 1] in ["torch.clip", "torch.clamp"]:
                _has_mask = True

        if _has_log is True and _has_mask is False:
            self.add_message(msgid="missing-mask-pytorch", node=call_node)
