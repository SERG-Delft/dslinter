"""Checker which checks column is selected after the dataframe is imported."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class ColumnSelectionPandasChecker(BaseChecker):
    """Checker which checks column is selected after the dataframe is imported."""

    __implements__ = IAstroidChecker

    name = "column-selection-pandas"
    priority = -1
    msgs = {
        "R5504": (
            "There is no column selection after the dataframe is imported.",
            "column-selection-pandas",
            "Column should be selected after the dataframe is imported for better readability."
        )
    }
    options = ()

    _import_data_pandas = False
    _import_data_idx = -1
    _dataframe_name = ""

    def visit_module(self, module: astroid.Module):
        """
        Visit module and see whether the rule is violated.
        :param module:
        :return:
        """
        for idx, node in enumerate(module.body):
            if isinstance(node, astroid.Assign):
                sub_node = node.value
                if(
                    hasattr(sub_node, "func")
                    and hasattr(sub_node.func, "attrname")
                    and sub_node.func.attrname == "read_csv"
                    and hasattr(sub_node.func, "expr")
                    and hasattr(sub_node.func.expr, "name")
                    and sub_node.func.expr.name in ["pandas", "pd"]
                    and len(node.targets) > 0
                    and hasattr(node.targets[0], "name")
                ):
                    self._import_data_pandas = True
                    self._import_data_idx = idx
                    self._dataframe_name = node.targets[0].name
                if len(module.body) <= self._import_data_idx + 1:
                    self.add_message("column-selection-pandas", node=module)
                if self._import_data_idx != -1 and idx == self._import_data_idx + 1:
                    if(
                        len(node.targets) > 0
                        and hasattr(node.targets[0], "name")
                        and node.targets[0].name == self._dataframe_name
                        and hasattr(node, "value")
                        and hasattr(node.value, "slice")
                        and isinstance(node.value.slice, astroid.nodes.List)
                    ):
                        pass
                    else:
                        self.add_message("column-selection-pandas", node=module)

