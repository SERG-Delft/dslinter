""""""

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.type_inference import TypeInference
from typing import Dict


class TensorArrayTensorflowChecker(BaseChecker):
    """"""

    __implements__ = IAstroidChecker

    name = "tensor-array-tensorflow"
    priority = -1
    msgs = {
        "": (
            "tensor-array-tensorflow",
            "tensor-array-tensorflow",
            "tensor-array-tensorflow",
        )
    }
    options = ()

     # [variable name, inferred type of object the function is called on]
    _variable_types: Dict[str, str] = {}

    def visit_module(self, module: astroid.Module):
        """Visit module and infer which libraries the variables are from. """
        try:
            self._variable_types = TypeInference.infer_library_variable_first_types(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_for(self, for_node: astroid.For):
        for node in for_node.body:
            if(
                isinstance(node, astroid.Assign)
                and len(node.targets) > 0
                and hasattr(node.targets[0], "name")
                and node.targets[0].name in self._variable_types
                and self._variable_types[node.targets[0].name] in ["tf.constant", "tensorflow.constant"]
                and self.infer_call_expression(node.value) in ["tf.concat"]
            ):
                self.add_message("tensor-array-tensorflow", node=for_node)

    def infer_call_expression(self, call_node: astroid.Call):
        call_expression = ""
        call = call_node.func
        if hasattr(call, "attrname"):
            call_expression = "." + call.attrname + call_expression
        while hasattr(call, "expr"):
            call = call.expr
            if hasattr(call, "attrname"):
                call_expression = "." + call.attrname + call_expression
        if hasattr(call, "name"):
            call_expression = call.name + call_expression
        return call_expression
