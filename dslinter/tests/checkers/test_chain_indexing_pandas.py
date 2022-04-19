"""Class which test ChainIndexingPandasChecker."""
import astroid
import pylint.testutils

import dslinter


class TestChainIndexingPandasChecker(pylint.testutils.CheckerTestCase):
    """Class which test ChainIndexingPandasChecker."""

    CHECKER_CLASS = dslinter.plugin.ChainIndexingPandasChecker

    def test_chain_indexing_on_dataframe1(self):
        """Message should be added if there is a chain indexing on pandas dataframe."""
        script = """
        import pandas as pd
        df = pd.DataFrame([[1,2,3],[4,5,6]])
        col = 1
        x = 0
        df[col][x] = 42 #@
        """
        module = astroid.parse(script)
        assign_node = astroid.extract_node(script)
        subscript_node = assign_node.targets[0]
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="chain-indexing-pandas", node=subscript_node)):
            self.checker.visit_module(module)
            self.checker.visit_subscript(subscript_node)

    def test_chain_indexing_on_dataframe2(self):
        """Message should be added if there is a chain indexing on pandas dataframe."""
        script = """
        import pandas as pd
        df = pd.DataFrame([[[1, 1],[2, 2],[3, 3]],[[4, 4],[5, 5],[6, 6]]])
        col = 1
        x = 0
        y = 0
        df[col][x][y] = 42 #@
        """
        module = astroid.parse(script)
        assign_node = astroid.extract_node(script)
        subscript_node = assign_node.targets[0]
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="chain-indexing-pandas", node=subscript_node)):
            self.checker.visit_module(module)
            self.checker.visit_subscript(subscript_node)

    def test_chain_indexing_on_normal_array(self):
        """No message should be added if there is a chain indexing on normal array."""
        script = """
        a = [[0, 0][0, 0]]
        a[0][1] = 2 #@
        """
        module = astroid.parse(script)
        assign_node = astroid.extract_node(script)
        subscript_node = assign_node.targets[0]
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_subscript(subscript_node)

    def test_indexing_on_dataframe(self):
        """No message should be added if there is a normal indexing on pandas dataframe."""
        script = """
        import pandas as pd
        df = pd.DataFrame([[1,2,3],[4,5,6]])
        col = 1
        x = 0
        df[col] = 42 #@        
        """
        module = astroid.parse(script)
        assign_node = astroid.extract_node(script)
        subscript_node = assign_node.targets[0]
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_subscript(subscript_node)

    def test_no_chain_indexing_on_dataframe(self):
        """No message should be added when there is no chain indexing on dataframe."""
        script = """
        import pandas as pd
        df = pd.DataFrame([[1,2,3],[4,5,6]])
        col = 1
        x = 0
        df.loc[x, col] = 42  #@     
        """
        module = astroid.parse(script)
        assign_node = astroid.extract_node(script)
        subscript_node = assign_node.targets[0]
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_subscript(subscript_node)

