""" In-Place Checker for NumPy which checker In-Place APIs are correctly used. """
import astroid
from pylint. checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.util.exception_handler import ExceptionHandler


class InPlaceNumpyChecker(BaseChecker):
    """ In-Place Checker for NumPy which checker In-Place APIs are correctly used. """
    __implement__ = IAstroidChecker

    name = "inplace_numpy"
    priority = -1
    msgs = {
        "W5502":(
            "The operation result has not been assigned to another variable, which might cause losing the result.",
            "inplace-numpy",
            "The result of the operation should be assigned to another variable, or the `out` parameter should be defined."
        )
    }
    options = ()

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, add messages if it violated the defined rules.

        :param node: call node
        """
        try:
            if self._result_is_lost(node):
                self.add_message("inplace-numpy", node = node)
        except: # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

    def _result_is_lost(self, node: astroid.Call) -> bool:
        """
        If the inplace parameter is not set in the API, and the result of API call is
        not assigned to another variable, the result is lost.

        :param node:
        :return: True if the result is lost.
        """
        return (
                hasattr(node, "func")
                and hasattr(node.func, "expr")
                and hasattr(node.func.expr, "name")
                and node.func.expr.name == "np"
                and not self._inplace_is_true(node)
                # If the parent of the Call is an Expression (not an Assignment), it means the result is lost.
                and isinstance(node.parent, astroid.Expr)
        )

    @staticmethod
    def _inplace_is_true(node: astroid.Call) -> bool:
        """
        Evaluate whether the call has an 'out==True' keyword argument.

        :param node: Node to check the arguments from.
        :return: True when the call has an 'inplace==True' keyword argument.
        """
        if node.keywords is None:
            return False

        for keyword in node.keywords:
            if keyword.arg == "out":
                return keyword.value.value
        return False
