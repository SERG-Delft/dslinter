""" In-Place Checker for NumPy which checker In-Place APIs are correctly used. """
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.inplace_helper import inplace_is_true


class InPlaceNumpyChecker(BaseChecker):
    """ In-Place Checker for NumPy which checker In-Place APIs are correctly used. """

    __implements__ = IAstroidChecker

    name = "inplace-numpy"
    priority = -1
    msgs = {
        "W9999": (
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
                self.add_message("inplace-numpy", node=node)
        except:  # pylint: disable=bare-except
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
                and node.func.expr.name in ["np", "numpy"]  # This might need to be changed to a more robust check
                and not self._function_whitelisted(node)
                and not inplace_is_true(node, "out")
                # If the parent of the Call is an Expression (not an Assignment or a Call or Return),
                # it means the result is lost.
                and isinstance(node.parent, astroid.Expr)
        )

    def _function_whitelisted(self, node) -> bool:
        """
        If the function is in the whitelist, it can be excluded from the check.
        :return:
        """
        WHITELIST = [
            "resize",
            "sort",
            "save",
            "savez",
            "savez_compressed",
            "savetxt",
            "tofile",
            "fill_diagonal",
            "testing",
            "allclose",
            "copyto",
            "set_printoptions",
            "isclose",
            "seterr",
            "scatter_add"
        ]
        return hasattr(node.func, "attrname") and (node.func.attrname in WHITELIST)
