"""Checker which checks whether values are compared with np.nan."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class NanChecker(BaseChecker):
    """Checker which checks whether values are compared with np.nan."""

    __implements__ = IAstroidChecker

    name = "nan"
    priority = -1
    msgs = {
        "E5001": (
            "Value compared with np.nan.",
            "nan-equality",
            "Values cannot be compared with np.nan, as np.nan != np.nan.",
        ),
    }
    options = ()

    def visit_compare(self, node: astroid.Compare):
        """
        When a compare node is visited, check whether a comparison is done with np.nan.

        :param node: Node which is visited.
        """
        for side in (node.left, node.ops[0][1]):
            if (
                isinstance(side, astroid.Attribute)
                and side.attrname == "nan"
                and side.expr.name == "np"
            ):
                self.add_message("nan-equality", node=node)
                return
