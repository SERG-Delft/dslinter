# """Checker which checks whether np.dot() is used for matrix multiplication in the numpy code."""
# import astroid
# from pylint.interfaces import IAstroidChecker
# from pylint.checkers import BaseChecker
#
#
# class MatrixMultiplicationNumpyChecker(BaseChecker):
#     """Checker which checks whether np.dot() is used for matrix multiplication in the numpy code."""
#
#     __implements__ = IAstroidChecker
#
#     name = "matrix-multiplication-numpy"
#     priority = -1
#     msgs = {
#         "": (
#             "np.dot() is used for matrix multiplication in the code.",
#             "matrix-multiplication-numpy",
#             "np.dot() shouldn't be used for matrix multiplication in the code."
#         )
#     }
#     options = ()
#
#     def visit_call(self, call_node: astroid.Call):
#         """Visit call node and check whether the rule is violated."""
#         if(
#             hasattr(call_node.func, "attrname")
#             and call_node.func.attrname == "dot"
#             and hasattr(call_node.func, "expr")
#             and hasattr(call_node.func.expr, "name")
#             and call_node.func.expr.name in ["numpy", "np"]
#         ):
#             self.add_message("matrix-multiplication-numpy", node=call_node)
