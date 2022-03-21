# """Class which tests MatrixMultiplicationNumpyChecker."""
# import dslinter
# import pylint.testutils
# import astroid
#
#
# class TestMatrixMultiplicationNumpyChecker(pylint.testutils.CheckerTestCase):
#     """Class which tests MatrixMultiplicationNumpyChecker."""
#
#     CHECKER_CLASS = dslinter.plugin.MatrixMultiplicationNumpyChecker
#
#     def test_matrix_multiplication_incorrectly_used(self):
#         """Message should be added when np.dot() is used in the code."""
#         script = """
#         import numpy as np
#         a = [[1, 0], [0, 1]]
#         b = [[4, 1], [2, 2]]
#         np.dot(a, b)  #@
#         """
#         call_node = astroid.extract_node(script)
#         with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="matrix-multiplication-numpy", node=call_node)):
#             self.checker.visit_call(call_node)
#
#     def test_matrix_multiplication_correctly_used(self):
#         """No message should be added when np.matmul() is used for matrix multiplication."""
#         script = """
#         import numpy as np
#         a = [[1, 0], [0, 1]]
#         b = [[4, 1], [2, 2]]
#         np.matmul(a, b)   #@
#         """
#         call_node = astroid.extract_node(script)
#         with self.assertNoMessages():
#             self.checker.visit_call(call_node)
