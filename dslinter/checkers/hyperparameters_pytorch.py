# import astroid as astroid
# from pylint.interfaces import IAstroidChecker
#
# from dslinter.util.exception_handler import ExceptionHandler
#
#
# class HyperparameterPyTorchChecker():
#
#     __implements__ = IAstroidChecker
#
#     name = "hyperparameter_pytorch"
#     priority = -1
#     msgs = {
#         "": (
#             "",
#             "hyperparameter-pytorch",
#             ""
#         )
#     }
#
#     options = (
#
#     )
#
#     HYPERPARAMETERS_MAIN = {
#
#     }
#
#     def visit_call(self, node: astroid.Call):
#         try:
#             pass
#         except:
#             ExceptionHandler.handle(self, node)
#
