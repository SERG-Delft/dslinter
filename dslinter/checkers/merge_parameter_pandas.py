"""Checker which checks whether the parameters for merge operations are set."""
import astroid as astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from typing import Dict

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.type_inference import TypeInference


class MergeParameterPandasChecker(BaseChecker):
    """Checker which checks whether the parameters for merge operations are set."""

    __implements__ = IAstroidChecker

    name = "merge-parameter-pandas"
    priority = -1
    msgs = {
        "R5505": (
            "Parameters for merge operations are not set.",
            "merge-parameter-pandas",
            "Parameters 'how', 'on' and 'validate' should be set for merge operations to ensure the correct usage of merging."
        )
    }
    options = ()

    # [variable name, inferred type of object the function is called on]
    _subscript_types: Dict[str, str] = {}

    def visit_module(self, module: astroid.Module):
        """Visit module and infer which library the variables are from. """
        try:
            self._subscript_types = TypeInference.infer_library_variable_most_recent_types(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_call(self, call_node: astroid.Call):
        """Visit call node and check whether the parameters are set."""
        # call on pandas dataframe object && name "merge" && check parameter
        try:
            if(
                hasattr(call_node.func, "attrname")
                and call_node.func.attrname == "merge"
                and hasattr(call_node.func, "expr")
                and hasattr(call_node.func.expr, "name")
                and call_node.func.expr.name in self._subscript_types
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
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, call_node)
