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
            "Chain indexing is used in pandas code",
            "chain-indexing-pandas",
            "Chain indexing is considered bad practice in pandas and should be avoided in pandas code."
        )
    }
    options = ()

    # [variable name, inferred type of object the function is called on]
    _subscript_types: Dict[str, str] = {}

    def visit_module(self, module: astroid.Module):
        """Visit module and infer which libraries the variables are from. """
        try:
            self._subscript_types = TypeInference.infer_library_variable_most_recent_types(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_subscript(self, subscript_node: astroid.Subscript):
        """Visit subscript node and check whether there is chain indexing."""
        if(
            hasattr(subscript_node, "value")
            and hasattr(subscript_node.value, "value")
            and hasattr(subscript_node.value.value, "name")
            and subscript_node.value.value.name in self._subscript_types
            and self._subscript_types[subscript_node.value.value.name] == "pd.DataFrame"
        ):
            self.add_message("chain-indexing-pandas", node=subscript_node)

