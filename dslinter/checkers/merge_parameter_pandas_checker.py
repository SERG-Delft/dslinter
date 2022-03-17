import astroid as astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from typing import Dict

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.type_inference import TypeInference


class MergeParameterPandasChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "merge-parameter-pandas"
    priority = -1
    msgs = {
        "": (
            "merge-parameter-pandas",
            "merge-parameter-pandas",
            "merge-parameter-pandas"
        )
    }
    options = ()

    # [variable name, inferred type of object the function is called on]
    _subscript_types: Dict[str, str] = {}

    def visit_module(self, module: astroid.Module):
        """Visit module and infer which library the variables are from. """
        try:
            self._subscript_types = TypeInference.infer_dataframes(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_call(self, call_node: astroid.Call):
        # call on pandas dataframe object && name "merge" && check parameter
        if(
            hasattr(call_node.func, "attrname")
            and call_node.func.attrname == "merge"
            and hasattr(call_node.func, "expr")
            and hasattr(call_node.func.expr, "name")
            and self._subscript_types[call_node.func.expr.name] in ["pd.DataFrame", "pandas.DataFrame"]
        ):
            kws = [kw.arg for kw in call_node.keywords if hasattr(kw, "arg")]
            if(
                "how" in kws
                and "on" in kws
                and "validate" in kws
            ):
                pass
            else:
                self.add_message("merge-parameter-pandas", node=call_node)

