"""Checker which checks whether chain indexing is used in pandas code."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from typing import Dict

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.type_inference import TypeInference


class ChainIndexingPandasChecker(BaseChecker):
    """Checker which checks whether chain indexing is used in pandas code."""

    __implements__ = IAstroidChecker

    name = "chain-indexing-pandas"
    priority = -1
    msgs = {
        "W5502": (
            "Chain indexing is used in pandas code.",
            "chain-indexing-pandas",
            "Chain indexing is considered bad practice in pandas code and should be avoided."
        )
    }
    options = ()

    # [subscript node name, inferred type of object the function is called on]
    _subscript_types: Dict[str, str] = {}

    def visit_module(self, module: astroid.Module):
        """Visit module and infer which libraries the variables are from. """
        try:
            self._subscript_types = TypeInference.infer_library_variable_most_recent_types(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_subscript(self, subscript_node: astroid.Subscript):
        """Visit subscript node and check whether there is chain indexing."""
        try:
            indexing_num = 0
            node = subscript_node
            # count indexing number
            while hasattr(node, "value"):
                indexing_num += 1
                node = node.value
            # if chain indexing is used in the code, and the indexing number is no less than two, the rule is violated.
            if(
                hasattr(node, "name")
                and node.name in self._subscript_types
                and self._subscript_types[node.name] == "pd.DataFrame"
                and indexing_num >= 2
            ):
                self.add_message("chain-indexing-pandas", node=subscript_node)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, subscript_node)
