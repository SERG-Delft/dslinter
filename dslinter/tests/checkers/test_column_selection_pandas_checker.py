# import pylint.testutils
#
# import dslinter.plugin
#
#
# class TestColumnSelectionPandasChecker(pylint.testutils.CheckerTestCase):
#
#     CHECKER_CLASS = dslinter.plugin.ColumnSelectionPandasChecker
#
#     def test_column_not_selected(self):
#         script = """
#         import pandas as pd
#         df = pd.read_csv('data.csv')
#         """
#         with self.assertAddsMessages():
#             self.checker.visit_call()
#
#
#     def test_column_selected(self):
#         script = """
#         import pandas as pd
#         df = pd.read_csv('data.csv')
#         df = df[['col1', 'col2', 'col3']]
#         """
#         with self.assertNoMessages():
#             self.checker.visit_call()
