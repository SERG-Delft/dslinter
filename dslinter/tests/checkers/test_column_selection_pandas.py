"""Class which tests ColumnSelectionPandasChecker."""
import pylint.testutils
import astroid
import dslinter.plugin


class TestColumnSelectionPandasChecker(pylint.testutils.CheckerTestCase):
    """Class which tests ColumnSelectionPandasChecker."""

    CHECKER_CLASS = dslinter.plugin.ColumnSelectionPandasChecker

    def test_column_not_selected(self):
        """Message should be added if there is no column selection after the dataframe is imported."""
        script = """
        import pandas as pd
        df = pd.read_csv('data.csv')
        """
        module = astroid.parse(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="column-selection-pandas", node=module)):
            self.checker.visit_module(module)

    def test_column_selected(self):
        """No Message should be added if there is column selection after the dataframe is imported."""
        script = """
        import pandas as pd
        df = pd.read_csv('data.csv')
        df = df[['col1', 'col2', 'col3']]
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)
