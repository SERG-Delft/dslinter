"""DataFrame checker which checks correct handling of calls on DataFrames."""
from typing import Dict

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.util.type_inference import TypeInference


class DataFrameCallChecker(BaseChecker):
    """DataFrame checker which checks correct handling of calls on DataFrames."""

    __implements__ = IAstroidChecker

    name = "dataframe-call"
    priority = -1
    msgs = {
        "W5501": (
            "Result of operation on a DataFrame is not assigned.",
            "dataframe-lost",
            "Most operations on a DataFrame return a new DataFrame. These should be assigned to \
            a variable.",
        ),
    }
    options = ()

    _call_types: Dict[
        astroid.nodes.Call, str
    ] = {}  # [node, inferred type of object the function is called on]

    def visit_module(self, node: astroid.nodes.Module):
        """
        When an Module node is visited, scan for Call nodes and get type the function is called on.

        :param node: Node which is visited.
        """
        # noinspection PyTypeChecker
        self._call_types = TypeInference.infer_types(
            node, astroid.nodes.Call, lambda x: x.func.expr.name
        )

    def visit_call(self, node: astroid.nodes.Call):  # noqa: D205, D400
        """
        When a 'simple' Call node is visited and the type of object the function is called on is a
            DataFrame, check if the Call node is part of an expression.

        A 'simple' Call node is a single function call. E.g., 'f()' and not 'f().g()'.
        This means that 'DataFrame([]).abs().abs()' is a known false negative.

        :param node: Node which is visited.
        """
        if self._is_simple_call_node(node) and self._dataframe_is_lost(node):
            self.add_message("dataframe-lost", node=node)

    @staticmethod
    def _is_simple_call_node(node: astroid.nodes.Call) -> bool:
        """
        Evaluate whether the node is a 'simple' call node.

        A 'simple' Call node is a single function call made on an expression.
        E.g., 'a.f()' and not 'f()' or 'a.f().g()' or 'a.f(g())'.

        :param node: Call node to evaluate.
        :return: True when the Call node is considered simple.
        """
        return (
            hasattr(node.func, "expr")  # The call is made on an expression.
            and hasattr(node.func.expr, "name")  # The expr the func is called on is a named thing.
            and not isinstance(node.parent, astroid.nodes.Attribute)  # Call is not an attribute.
            and not isinstance(node.parent, astroid.nodes.Call)  # Call is not part of another call.
        )

    def _dataframe_is_lost(self, node: astroid.nodes.Call) -> bool:
        """
        Check whether the call is done on a DataFrame and the result is lost.

        A result is seen as lost if it is not assigned to a variable and the operation is not done
        inplace.

        :param node: Node which is visited.
        :return: True when the call results in a DataFrame which is lost.
        """
        return (
            node in self._call_types  # Check if the type is inferred of this call.
            and self._call_types[node] == "pandas.core.frame.DataFrame"
            and not self._is_inplace_operation(node)
            and not (  # Check if the call is part of an assign operation.
                isinstance(node.parent, astroid.nodes.Assign)
                or isinstance(node.parent, astroid.nodes.AssignAttr)
                or isinstance(node.parent, astroid.nodes.AnnAssign)
            )
        )

    @staticmethod
    def _is_inplace_operation(node: astroid.nodes.Call) -> bool:
        """
        Evaluate whether the call has an 'inplace==True' keyword argument.

        :param node: Node to check the arguments from.
        :return: True when the call has an 'inplace==True' keyword argument.
        """
        if node.keywords is None:
            return False

        for keyword in node.keywords:
            if keyword.arg == "inplace":
                return keyword.value.value
        return False
