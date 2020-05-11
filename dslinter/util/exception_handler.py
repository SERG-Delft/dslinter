"""Utility module for handling exceptions thrown in checkers."""
import astroid
from pylint.checkers import BaseChecker

from dslinter.util.ast import ASTUtil


class ExceptionHandler:
    """Utility class for handling exceptions thrown in checkers."""

    @staticmethod
    def handle(checker: BaseChecker, node: astroid.node_classes.NodeNG):
        """
        Handle an exception thrown in a checker.

        Print an error message to the console.

        :param checker: Checker where the exception is thrown from.
        :param node: Node which is visited while the exception is thrown.
        """
        module = ASTUtil.search_module(node)
        print(
            "ERROR: Could not finish processing the checker {} on module {}. Continuing.".format(
                checker.name, module.name
            )
        )
