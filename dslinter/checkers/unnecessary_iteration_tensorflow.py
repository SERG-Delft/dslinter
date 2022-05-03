"""Check whether there is an unnecessary iteration in Tensorflow code."""
from typing import Dict
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
import astroid
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.type_inference import TypeInference


class UnnecessaryIterationTensorflowChecker(BaseChecker):
    """Check whether there is an unnecessary iteration in Tensorflow code."""
    __implements__ = IAstroidChecker

    name = "unnecessary-iteration-tensorflow"
    priority = -1
    msgs = {
        "R5502": {
            "There is an unnecessary iteration in the tensorflow code.",
            "unnecessary-iteration-tensorflow",
            "There is a efficient solution(Vectorization or Reduction) to replace the iteration.",
        }
    }
    options = ()

    # [variable name, inferred type of object the function is called on]
    _variable_types: Dict[str, str] = {}

    def visit_module(self, module: astroid.Module):
        """Visit module and infer which library the variables are from. """
        try:
            self._variable_types = TypeInference.infer_native_variable_most_recent_types(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_for(self, node: astroid.For):
        """Evaluate whether there is an augmented assign in the loop, it can be replaced
            by a reduction operation, which is faster."""
        try:
            if (
                hasattr(node, "body")
                # there is augmented assign with tf variable in the body
                and self._augmented_assign_with_tf_variable(node.body)
            ):
                self.add_message("iteration-tensorflow", node=node)
        except:  # pylint: disable=W0702
            ExceptionHandler.handle(self, node)

    def _augmented_assign_with_tf_variable(self, body: list) -> bool:
        """
        Check whether there are augmented assigns in the body,
        and whether the augmented assign is applied on a tensorflow variable.
        :param body: body in the for node
        :return: True when meeting the requirements
        """
        for node in body:
            # there is augmented assign in the body
            if isinstance(node, astroid.AugAssign):
                # # the augmented assign is apply on a const
                # if hasattr(node, "value") and isinstance(node.value, astroid.nodes.Const):
                #     return True
                while hasattr(node, "value"):
                    node = node.value
                # the augmented assign is apply on a tf variable node
                if hasattr(node, "name") and self._is_tf_variable(node.name):
                    return True
        return False

    def _is_tf_variable(self, name) -> bool:
        """
        Check whether the variable with the name is a tensorflow variable
        :param name: name of the variable
        :return: True when meeting the requirements
        """
        return name in self._variable_types and self._variable_types[name] in ["tf", "tensorflow"]
