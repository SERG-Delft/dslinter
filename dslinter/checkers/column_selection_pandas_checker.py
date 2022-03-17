from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

class ColumnSelectionPandasChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "column-selection-pandas"
    priority = -1
    msgs = {
        "": (
            "column-selection-pandas",
            "column-selection-pandas",
            "column-selection-pandas"
        )
    }
    options = ()

    def visit_call(self):
        pass

