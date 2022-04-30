"""Class which tests the DataFrameChecker."""
import astroid
import pylint.testutils
import dslinter


class TestUnnecessaryIterationPandasChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the DataFrameChecker."""

    CHECKER_CLASS = dslinter.plugin.UnnecessaryIterationPandasChecker

    def test_iterating_through_dataframe(self):
        """Test whether a message is added when there is iterated through a DataFrame."""
        script = """
        import pandas as pd
        df = pd.DataFrame()
        for _, row in df.iterrows(): 
            pass
        """
        module_tree = astroid.parse(script)
        call = module_tree.body[-1].iter
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="dataframe-iteration-modification-pandas", node=call),):
            self.checker.visit_module(module_tree)
            self.checker.visit_call(call)

    def test_iterating_and_modifying(self):
        """Test whether a dataframe-iteration-modification violation is correctly found."""
        script = """
        import pandas as pd
        df = pd.DataFrame()
        for _, row in df.iterrows():
            row['a'] = 10
        """
        module_tree = astroid.parse(script)
        for_node = module_tree.body[-1]
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(msg_id="dataframe-iteration-modification-pandas", node=for_node),
        ):
            self.checker.visit_module(module_tree)
            self.checker.visit_for(for_node)

    def test_iterating_and_modifying_nested(self):
        """Test whether a nested dataframe-iteration-modification violation is correctly found."""
        script = """
        import pandas as pd
        df = pd.DataFrame()
        for _, row in df.iterrows():
            if True: row['a'] = 10
        """
        module_tree = astroid.parse(script)
        for_node = module_tree.body[-1]
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(msg_id="dataframe-iteration-modification-pandas", node=for_node),
        ):
            self.checker.visit_module(module_tree)
            self.checker.visit_for(for_node)
