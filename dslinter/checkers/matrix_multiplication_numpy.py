import astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker

class MatrixMultiplicationNumpyChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "matrix-multiplication-numpy"
    priority = -1
    msgs = {
        "": (
            "matrix-multiplication-numpy",
            "matrix-multiplication-numpy",
            "matrix-multiplication-numpy"
        )
    }
    options = ()

    def visit_call(self, call_node: astroid.Call):
        pass

