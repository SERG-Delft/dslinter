"""Checker which check whether df.values is used for dataframe conversion."""
from typing import Dict
import astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker

from dslinter.utils.exception_handler import ExceptionHandler


class DataframeConversionPandasChecker(BaseChecker):
    """Checker which check whether df.values is used for dataframe conversion."""

    __implements__ = IAstroidChecker

    name = "dataframe-conversion-pandas"
    priority = -1
    msgs = {
        "W5504": (
            "df.values is used in pandas code for dataframe conversion.",
            "dataframe-conversion-pandas",
            "For dataframe conversion in pandas code, use .to_numpy() instead of .values."
        )
    }
    options = ()

    # [variable name, inferred type of object the function is called on]
    _call_types: Dict[str, str] = {}
    _imported_pandas = False

    def visit_import(self, import_node: astroid.Import):
        """Visit import node to see whether pandas is imported."""
        try:
            for name, _ in import_node.names:
                if name == "pandas":
                    self._imported_pandas = True
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, import_node)

    def visit_call(self, call_node: astroid.Call):
        """Visit call node to see whether there is rule violation."""
        try:
            if hasattr(call_node, "attrname") and call_node.attrname == "values":
                self.add_message("dataframe-conversion-pandas", node=call_node)
                return
            if(
                hasattr(call_node, "func")
                and hasattr(call_node.func, "expr")
                and hasattr(call_node.func.expr, "attrname")
                and call_node.func.expr.attrname == "values"
            ):
                    self.add_message("dataframe-conversion-pandas", node=call_node)
                    return
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, call_node)
