"""DataFrame checker which checks correct handling of calls on DataFrames."""
from typing import Dict, List

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.util.ast import AssignUtil
from dslinter.util.type_inference import TypeInference


class DataFrameChecker(BaseChecker):
    """DataFrame checker which checks correct handling of calls on DataFrames."""

    __implements__ = IAstroidChecker

    name = "dataframe"
    priority = -1
    msgs = {
        "W5501": (
            "Result of operation on a DataFrame is not assigned.",
            "unassigned-dataframe",
            "Most operations on a DataFrame return a new DataFrame. These should be assigned to \
            a variable.",
        ),
        "W5502": (
            "Iterating through a DataFrame.",
            "dataframe-iteration",
            "Iteration through pandas objects is generally slow and should be avoided.",
        ),
        "W5503": (
            "Iterated object is modified.",
            "dataframe-iteration-modification",
            "An object where is iterated over should not be modified.",
        ),
    }
    options = ()

    _call_types: Dict[
        astroid.Call, str
    ] = {}  # [node, inferred type of object the function is called on]

    def visit_module(self, node: astroid.Module):
        """
        When an Module node is visited, scan for Call nodes and get type the function is called on.

        :param node: Node which is visited.
        """
        # noinspection PyTypeChecker
        self._call_types = TypeInference.infer_types(node, astroid.Call, lambda x: x.func.expr.name)

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, add messages if it violated the defined rules.

        :param node: Node which is visited.
        """
        if self._is_simple_call_node(node) and self._dataframe_is_lost(node):
            self.add_message("unassigned-dataframe", node=node)
        if self._iterating_through_dataframe(node):
            self.add_message("dataframe-iteration", node=node)

    @staticmethod
    def _is_simple_call_node(node: astroid.Call) -> bool:
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
            and not isinstance(node.parent, astroid.Attribute)  # Call is not an attribute.
            and not isinstance(node.parent, astroid.Call)  # Call is not part of another call.
        )

    def _dataframe_is_lost(self, node: astroid.Call) -> bool:
        """
        Check whether the call is done on a DataFrame and the result is lost.

        A result is seen as lost if its parent is an Expression and the operation is not done
        inplace.

        :param node: Node which is visited.
        :return: True when the call results in a DataFrame which is lost.
        """
        # TODO: Whitelist the functions head, tail, sample, boxplot, describe, hist, info, memory_usage, plot, and to_*** (all functions starting with "to_").
        return (
            node in self._call_types  # Check if the type is inferred of this call.
            and self._call_types[node] == "pandas.core.frame.DataFrame"
            and not self._is_inplace_operation(node)
            # If the parent of the Call is an Expression, it means the DataFrame is lost.
            and isinstance(node.parent, astroid.Expr)
        )

    @staticmethod
    def _is_inplace_operation(node: astroid.Call) -> bool:
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

    def _iterating_through_dataframe(self, node: astroid.Call) -> bool:
        """
        Evaluate whether there is iterated through a DataFrame.

        :param node: Node which is visited.
        :return: True when there is iterated through a DataFrame.
        """
        return (
            isinstance(node.parent, astroid.For)
            and node not in node.parent.body
            and node in self._call_types
            and self._call_types[node] == "pandas.core.frame.DataFrame"
        )

    def visit_for(self, node: astroid.For):
        """
        When a For node is visited, check for dataframe-iteration-modification violations.

        :param node: Node which is visited.
        """
        if not (
            isinstance(node.iter, astroid.Call)
            and node.iter in self._call_types
            and self._call_types[node.iter] == "pandas.core.frame.DataFrame"
        ):
            return

        for_targets = DataFrameChecker._get_for_targets(node)
        assigned = AssignUtil.get_assigned_target_names(node)
        modified_iterated_targets = any(target in for_targets for target in assigned)

        if modified_iterated_targets:
            self.add_message("dataframe-iteration-modification", node=node)

    @staticmethod
    def _get_for_targets(node: astroid.For) -> List[str]:
        """
        Get the target names of the for-loop definition.

        :param node: For node to get the target names from.
        :return: Target names.
        """
        target_names = []
        if isinstance(node.target, astroid.Tuple):
            for element in node.target.elts:
                if isinstance(element, astroid.AssignName):
                    target_names.append(element.name)
        elif isinstance(node.target, astroid.AssignName):
            target_names.append(node.target.name)
        return target_names
