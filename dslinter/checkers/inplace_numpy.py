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
        "W5601":(
            "The operation has not been assigned to another variable, which might result in losing the result",
            "inplace-misused-numpy",
            "The result of the operation should be assigned to another variable, or the in-place "
            "parameter should be set to True(In NumPy it is the out parameter)."
        )
    }
    options = ()

    # LIST = [
    #     # Binary operations
    #     "bitwise_and",
    #     "bitwise_or",
    #     "bitwise_xor",
    #     "invert",
    #     "left_shift",
    #     "right_shift"
    #     # logic functions
    #     "all",
    #     "any",
    #     "isfinite",
    #     "isinf",
    #     "isnan",
    #     "isnat",
    #     "isneginf",
    #     "isposinf",
    #     "logical_and",
    #     "logical_or",
    #     "logical_not",
    #     "logical_xor"
    #     "greater",
    #     "greater_equal",
    #     "less",
    #     "less_equal",
    #     "equal",
    #     "not_equal"
    #     # Mathematical
    #     "sin",
    #     "cos",
    #     "tan",
    #     "arcsin",
    #     "arccos",
    #     "arctan",
    #     "hypot",
    #     "arctan2",
    #     "degrees",
    #     "radians",
    #     "deg2rad",
    #     "rad2deg",
    #     "sinh",
    #     "cosh",
    #     "tanh",
    #     "arcsinh",
    #     "arccosh",
    #     "arctanh",
    #     "around",
    #     "round_",
    #     "rint",
    #     "fix",
    #     "floor",
    #     "ceil",
    #     "trunc",
    #     "prod",
    #     "sum",
    #     "nanprod",
    #     "nansum",
    #     "cumprod",
    #     "cumsum",
    #     "nancumprod",
    #     "nancumsum",
    #     "exp",
    #     "expm1",
    #     "exp2",
    #     "log",
    #     "log10",
    #     "log2",
    #     "log1p",
    #     "logaddexp",
    #     "logaddexp2",
    #     "signbit",
    #     "copysign",
    #     "frexp",
    #     "ldexp",
    #     "nextafter",
    #     "spacing",
    #     "lcm",
    #     "gcd",
    #     "add",
    #     "reciprocal",
    #     "positive",
    #     "negative",
    #     "multiply",
    #     "divide",
    #     "power",
    #     "subtract",
    #     "true_divide",
    #     "floor_divide",
    #     "float_power",
    #     "fmod",
    #     "mod",
    #     "modf",
    #     "remainder",
    #     "divmod",
    #     "maximum",
    #     "fmax",
    #     "amax",
    #     "nanmax",
    #     "minimum",
    #     "fmin",
    #     "amin",
    #     "nanmin",
    #     "convolve",
    #     "clip",
    #     "sqrt",
    #     "cbrt",
    #     "square",
    #     "absolute",
    #     "fabs",
    #     "sign",
    #     "heaviside",
    #     "nan_to_num"
    # ]

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, add messages if it violated the defined rules.

        :param node:
        """
        try:
            if self._result_is_lost(node):
                self.add_message("inplace-misused-numpy", node = node)
        except:
            ExceptionHandler.handle(self, node)

    def _result_is_lost(self, node: astroid.Call) -> bool:
        """
        If the inplace parameter is not set in the API, and the result of API call is
        not assigned to another variable, the result is lost.

        :param node:
        :return: True if the result is lost.
        """
        return (
            node.func.expr.name == "np" and
            not self._is_inplace_operation(node) and
            # If the parent of the Call is an Expression, it means the DataFrame is lost.
            isinstance(node.parent, astroid.Expr)
        )


    @staticmethod
    def _is_inplace_operation(node: astroid.Call) -> bool:
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
