"""Class which tests the DataFrameChecker."""
import astroid
import pylint.testutils
import dslinter


class TestUnnecessaryIterationPandasChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the DataFrameChecker."""

    CHECKER_CLASS = dslinter.plugin.UnnecessaryIterationPandasChecker

    DF_INIT = "import pandas as pd\ndf = pd.DataFrame()\n"

    # def test_iterating_through_dataframe(self):
    #     """Test whether a message is added when there is iterated through a DataFrame."""
    #     module_tree = astroid.parse(self.DF_INIT + "for _, row in df.iterrows(): pass")
    #     call = module_tree.body[-1].iter
    #     with self.assertAddsMessages(pylint.testutils.Message(msg_id="dataframe-iteration", node=call),):
    #         self.checker.visit_module(module_tree)
    #         self.checker.visit_call(call)

    # def test_iterating_and_modifying(self):
    #     """Test whether a dataframe-iteration-modification violation is correctly found."""
    #     module_tree = astroid.parse(self.DF_INIT + "for _, row in df.iterrows(): row['a'] = 10")
    #     for_node = module_tree.body[-1]
    #     with self.assertAddsMessages(
    #         pylint.testutils.Message(msg_id="dataframe-iteration-modification", node=for_node),
    #     ):
    #         self.checker.visit_module(module_tree)
    #         self.checker.visit_for(for_node)

    # def test_iterating_and_modifying_nested(self):
    #     """Test whether a nested dataframe-iteration-modification violation is correctly found."""
    #     module_tree = astroid.parse(self.DF_INIT + "for _, row in df.iterrows():\n\tif True: row['a'] = 10")
    #     for_node = module_tree.body[-1]
    #     with self.assertAddsMessages(
    #         pylint.testutils.Message(msg_id="dataframe-iteration-modification", node=for_node),
    #     ):
    #         self.checker.visit_module(module_tree)
    #         self.checker.visit_for(for_node)
