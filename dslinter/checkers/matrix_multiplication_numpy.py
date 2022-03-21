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
        if(
            hasattr(call_node.func, "attrname")
            and call_node.func.attrname == "dot"
            and hasattr(call_node.func, "expr")
            and hasattr(call_node.func.expr, "name")
            and call_node.func.expr.name in ["numpy", "np"]
        ):
            self.add_message("matrix-multiplication-numpy", node=call_node)

