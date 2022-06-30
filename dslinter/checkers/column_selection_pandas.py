"""Checker which checks column is selected after the dataframe is imported."""
from collections import defaultdict

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.utils.exception_handler import ExceptionHandler


class ColumnSelectionPandasChecker(BaseChecker):
    """Checker which checks column is selected after the dataframe is imported."""

    __implements__ = IAstroidChecker

    name = "column-selection-pandas-correct"
    priority = -1
    msgs = {
        "R5504": (
            "There is no column selection after the dataframe is imported.",
            "column-selection-pandas-correct",
            "Column should be selected after the dataframe is imported for better elaborating what to be expected in the downstream."
        )
    }
    options = ()

    _data_import_functions = ["read_csv", "read_table", "read_fwf", "read_excel", "read_xml"]

    def visit_module(self, module: astroid.Module):
        """
        Visit module and see whether the rule is violated.
        :param module:
        :return: None
        """
        try:
            self._traverse_content(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_functiondef(self, functiondef_node: astroid.FunctionDef):
        """
        Visit functiondef node and see whether the rule is violated.
        :param function_def_node:
        :return: None
        """
        try:
            self._traverse_content(functiondef_node)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, functiondef_node)

    def _traverse_content(self, block):
        """Traverse through the block and see whether the rule is violated"""
        _dataframe_selected_dict = defaultdict(bool)
        _name_node_dict = defaultdict()
        for _, node in enumerate(block.body):
            if isinstance(node, astroid.Assign):
                self._process_assign_node(node, _dataframe_selected_dict, _name_node_dict)

        # check which dataframe is imported but not selected by columns
        for k, v in _dataframe_selected_dict.items():
            if v is True:
                self.add_message("column-selection-pandas-correct", node=_name_node_dict[k])

    def _process_assign_node(self, node: astroid.Assign, _dataframe_selected_dict, _name_node_dict):
        """Check assign node to see if there is a imported dataframe or whether the datdframe columns are selected."""
        # check if there is a imported dataframe
        if(
            hasattr(node.value, "func")
            and hasattr(node.value.func, "attrname")
            and node.value.func.attrname in self._data_import_functions
            and hasattr(node.value.func, "expr")
            and hasattr(node.value.func.expr, "name")
            and node.value.func.expr.name in ["pandas", "pd"]
            and len(node.targets) > 0
            and hasattr(node.targets[0], "name")
        ):
            _imported_dataframe_name = node.targets[0].name
            _dataframe_selected_dict[_imported_dataframe_name] = False
            _name_node_dict[_imported_dataframe_name] = node
        # check if dataframe columns are selected
        if(
            hasattr(node, "value")
            and isinstance(node.value, astroid.Subscript)
            and hasattr(node.value, "value")
            and hasattr(node.value.value, "name")
            and node.value.value.name in _dataframe_selected_dict
            and hasattr(node.value, "slice")
            and isinstance(node.value.slice, astroid.nodes.List)
        ):
            _selected_dataframe_name = node.value.value.name
            _dataframe_selected_dict[_selected_dataframe_name] = True
