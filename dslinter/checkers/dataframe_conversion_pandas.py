import pdb

import astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.type_inference import TypeInference
from typing import Dict


class DataframeConversionPandasChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "dataframe-conversion-pandas"
    priority = -1
    msgs = {
        "": (
            "dataframe-conversion-pandas",
            "dataframe-conversion-pandas",
            "dataframe-conversion-pandas"
        )
    }
    options = ()

    # [variable name, inferred type of object the function is called on]
    _call_types: Dict[str, str] = {}

    def visit_module(self, module: astroid.Module):
        """Visit module and infer which libraries the variables are from. """
        try:
            self._call_types = TypeInference.infer_dataframes(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_call(self, call_node: astroid.Call):
        if(
            hasattr(call_node, "attrname")
            and call_node.attrname == "values"
            and hasattr(call_node, "expr")
            and hasattr(call_node.expr, "name")
            and call_node.expr.name in self._call_types
            # and self._call_types[call_node.expr.name] in ["pandas.DataFrame", "pd.DataFrame"]
        ):
            self.add_message("dataframe-conversion-pandas", node=call_node)


