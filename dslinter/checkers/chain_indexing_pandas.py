import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from typing import Dict

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.type_inference import TypeInference


class ChainIndexingPandasChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "chain-indexing-pandas"
    priority = -1
    msgs = {
        "": (
            "chain-indexing-pandas",
            "chain-indexing-pandas",
            "chain-indexing-pandas"
        )
    }
    options = ()

    # [variable name, inferred type of object the function is called on]
    _variable_types: Dict[str, str] = {}

    def visit_module(self, module: astroid.Module):
        """Visit module and infer which library the variables are from. """
        try:
            self._variable_types = TypeInference.infer_variable_types(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_subscript(self, subscript_node: astroid.Subscript):
        # is chainindexing && is dataframe
        if(
            hasattr(subscript_node, "value")
            and hasattr(subscript_node.value, "value")
            and hasattr(subscript_node.value.value, "name")
            and subscript_node.value.value.name in self._variable_types
            and self._variable_types[subscript_node.value.value.name] == "pd"
        ):
            self.add_message("chain-indexing-pandas", node=subscript_node)





