"""DataFrame checker which checks correct handling of DataFrames."""
from typing import Dict

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.util.type_inference import TypeInference


class DataFrameChecker(BaseChecker):
    """DataFrame checker which checks correct handling of DataFrames."""

    __implements__ = IAstroidChecker

    name = "dataframe"
    priority = -1
    msgs = {
        "W5501": (
            "Result of operation on a DataFrame is not saved.",
            "dataframe-lost",
            "An operation on a DataFrame returns a new DataFrame, which should be assigned to \
            a variable",
        ),
    }
    options = ()

    _call_nodes: Dict[
        astroid.nodes.Call, str
    ] = {}  # [node, inferred type of object the function is called on]

    def visit_module(self, node: astroid.nodes.Module):
        """
        When an Module node is visited, scan for Call nodes and get the type of the func expr.

        :param node: Node which is visited.
        """
        # noinspection PyTypeChecker
        self._call_nodes = TypeInference.infer_types(
            node, astroid.nodes.Call, lambda x: x.func.expr.name
        )
