"""Checker that checks whether datatype is set when dataframe is imported from data."""
import astroid as astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.utils.exception_handler import ExceptionHandler


class DatatypePandasChecker(BaseChecker):
    """Checker that checks whether datatype is set when a dataframe is imported from data."""

    __implements__ = IAstroidChecker

    name = "datatype-pandas"
    priority = -1
    msgs = {
        "R5503":(
            "Datatype is not set when a dataframe is imported from data.",
            "datatype-pandas",
            "Datatype should be set when a dataframe is imported from data.",
        )
    }
    options = ()

    _data_import_functions = ["read_csv", "read_table", "read_excel"]

    def visit_call(self, call_node: astroid.Call):
        """
        Vist call node and see whether datatype is set when a dataframe is imported from data.
        :param call_node:
        :return:
        """
        try:
            if(
                hasattr(call_node.func, "attrname")
                and call_node.func.attrname in self._data_import_functions
                and hasattr(call_node.func, "expr")
                and hasattr(call_node.func.expr, "name")
                and call_node.func.expr.name in ["pandas", "pd"]
            ):
                kws = [kw.arg for kw in call_node.keywords if hasattr(kw, "arg")]
                if "dtype" not in kws:
                    self.add_message(msgid="datatype-pandas", node=call_node)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, call_node)
