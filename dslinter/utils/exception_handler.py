"""Utility module for handling exceptions thrown in checkers."""
import astroid
from pylint.checkers import BaseChecker

from dslinter.utils.ast import ASTUtil


class ExceptionHandler:
    """Utility class for handling exceptions thrown in checkers."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def handle(checker: BaseChecker, node: astroid.node_classes.NodeNG):
        """
        Handle a generic exception thrown in a checker by printing an error message.

        :param checker: Checker where the exception is thrown from.
        :param node: Node which is visited while the exception is thrown.
        """
        module = ASTUtil.search_module(node)
        print(
            "ERROR: Could not finish processing the checker {} on module {} at line {}. Continuing.".format(
                checker.name, module.name, node.lineno
            )
        )
