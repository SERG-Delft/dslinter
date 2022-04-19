"""Class which tests ColumnSelectionPandasChecker."""
import pylint.testutils
import astroid
import dslinter.plugin


class TestColumnSelectionPandasChecker(pylint.testutils.CheckerTestCase):
    """Class which tests ColumnSelectionPandasChecker."""

    CHECKER_CLASS = dslinter.plugin.ColumnSelectionPandasChecker

    def test_column_not_selected(self):
        """A message should be added if there is no column selection after the dataframe is imported."""
        script = """
        import pandas as pd
        df = pd.read_csv('data.csv')
        """
        module = astroid.parse(script)
        assign_node = module.body[-1]
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="column-selection-pandas", node=assign_node)):
            self.checker.visit_module(module)

    def test_column_selected1(self):
        """No message should be added if there is column selection after the dataframe is imported."""
        script = """
        import pandas as pd
        df = pd.read_csv('data.csv')
        df = df[['col1', 'col2', 'col3']]
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_column_selected2(self):
        """No message should be added if there is column selection after the dataframe is imported."""
        script = """
        import pandas as pd
        df = pd.read_csv('data.csv')
        print(df)
        df = df[['col1', 'col2', 'col3']]
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_a_column_not_selected(self):
        """A message should be added if some imported dataframe are not selected by columns."""
        script = """
        import pandas as pd
        df1 = pd.read_csv('data1.csv')
        df2 = pd.read_csv('data2.csv')
        df1 = df1[['col1', 'col2', 'col3']]
        """
        module = astroid.parse(script)
        assign_node = module.body[-2]
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="column-selection-pandas", node=assign_node)):
            self.checker.visit_module(module)

    def test_all_columns_selected(self):
        """No message should be added if every imported dataframe is selected by columns."""
        script = """
        import pandas as pd
        df1 = pd.read_csv('data1.csv')
        df2 = pd.read_csv('data2.csv')
        df1 = df1[['col1', 'col2', 'col3']]
        df3 = df2[['col1', 'col2']]
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)
