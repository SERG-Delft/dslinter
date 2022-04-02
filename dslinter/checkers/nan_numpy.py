"""Checker which checks whether values are compared with np.nan."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.utils.exception_handler import ExceptionHandler


class NanNumpyChecker(BaseChecker):
    """Checker which checks whether values are compared with np.nan."""

    __implements__ = IAstroidChecker

    name = "nan-numpy"
    priority = -1
    msgs = {
        "E5501": (
            "Value compared with np.nan.",
            "nan-numpy",
            "Values cannot be compared with np.nan, as np.nan != np.nan.",
        ),
    }
    options = ()

    def visit_compare(self, node: astroid.Compare):
        """
        When a compare node is visited, check whether a comparison is done with np.nan.

        :param node: Node which is visited.
        """
        try:
            for side in (node.left, node.ops[0][1]):
                if isinstance(side, astroid.Attribute) \
                        and side.attrname == "nan" \
                        and side.expr.name == "np":
                    self.add_message("nan-numpy", node=node)
                    return
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)
