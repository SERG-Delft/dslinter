import astroid
import pylint.testutils

import dslinter

class TestChainIndexingPandasChecker(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.ChainIndexingPandasChecker

    def test_chain_indexing_on_dataframe(self):
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

    def test_chain_indexing_on_normal_array(self):
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

