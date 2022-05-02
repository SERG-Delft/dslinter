"""DataFrame checker which checks correct handling of calls on DataFrames."""
from typing import Dict
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.inplace_helper import inplace_is_true
from dslinter.utils.type_inference import TypeInference


class InPlacePandasChecker(BaseChecker):
    """DataFrame checker which checks correct handling of calls on DataFrames."""

    __implements__ = IAstroidChecker

    name = "inplace-pandas"
    priority = -1
    msgs = {
        "W5503": (
            "Result of operation on a DataFrame is not assigned.",
            "inplace-pandas",
            "Most operations on a DataFrame return a new DataFrame. These should be assigned to a variable.",
        ),
    }
    options = ()

    # [node, inferred type of object the function is called on]
    _call_types: Dict[astroid.Call, str] = {}

    # Whitelisted functions for which a DataFrame does not have to be assigned.
    WHITELISTED = [
        "all",
        "any",
        "bool",
        "boxplot",
        "corr",
        "corrwith",
        "count",
        "cov",
        "describe",
        "duplicated",
        "equals",
        "first_valid_index",
        "head",
        "hist",
        "idxmax",
        "idxmin",
        "info",
        "insert",
        "items",
        "iteritems",
        "iterrows",
        "itertuples",
        "keys",
        "last_valid_index",
        "mad",
        "max",
        "mean",
        "median",
        "memory_usage",
        "min",
        "mode",
        "nlargest",
        "nsmallest",
        "nunique",
        "plot",
        "profile_report",  # Jupyter notebook specific
        "sample",
        "sem",
        "skew",
        "sum",
        "tail",
        "update",
        "var",
        "to_***",
    ]

    def visit_module(self, module: astroid.Module):
        """
        When an Module node is visited, scan for Call nodes and get type the function is called on.

        :param module: Node which is visited.
        """
        try:
            # noinspection PyTypeChecker
            # pylint: disable = line-too-long
            self._call_types = TypeInference.infer_types(module, astroid.Call, lambda x: x.func.expr.name)
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, module)

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, add messages if it violated the defined rules.

        :param node: Node which is visited.
        """
        try:
            if (
                self._is_simple_call_node(node)
                and not self._function_whitelisted(node)
                and self._dataframe_is_lost(node)
            ):
                self.add_message("inplace-pandas", node=node)
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

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

    @staticmethod
    def _function_whitelisted(node: astroid.Call) -> bool:
        """
        Evaluate whether the a Call node is whitelisted for the unassigned-dataframe rule.

        All whitelisted functions do not have to assigned to a variable. Whitelisted functions
        are listed in the WHITELISTED variable and also include all functions starting with "to_".

        :param node: Call node to evaluate.
        :return: True when the function of the call is whitelisted.
        """
        return hasattr(node.func, "attrname") and (
                node.func.attrname in InPlacePandasChecker.WHITELISTED
                or node.func.attrname[:3] == "to_"
        )

    def _dataframe_is_lost(self, node: astroid.Call) -> bool:
        """
        Check whether the call is done on a DataFrame and the result is lost.

        A result is seen as lost if its parent is an Expression and the operation is not done
        inplace.

        :param node: Node which is visited.
        :return: True when the call results in a DataFrame which is lost.
        """
        return (
            node in self._call_types  # Check if the type is inferred of this call.
            and (
                self._call_types[node] == '"pandas.core.frame.DataFrame"'
                or self._call_types[node] == '"pyspark.sql.dataframe.DataFrame"'
            )
            and not inplace_is_true(node, "inplace")
            # If the parent of the Call is an Expression (not an Assignment),
            # it means the DataFrame is lost.
            and isinstance(node.parent, astroid.Expr)
        )
