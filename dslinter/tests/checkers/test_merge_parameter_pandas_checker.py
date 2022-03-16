import astroid
import pylint.testutils

import dslinter.plugin


class TestMergeParameterPandasChecker(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.MergeParameterPandasChecker

    def test_merge_parameter_pandas_checker_not_set(self):
        script = """
            import pandas as pd
            df1 = pd.DataFrame({'key': ['foo', 'bar', 'baz', 'foo'],
                                'value': [1, 2, 3, 5]})
            df2 = pd.DataFrame({'key': ['foo', 'bar', 'baz', 'foo'],
                                'value': [5, 6, 7, 8]})    
            df3 = df1.merge(df2)   #@                   
        """
        module = astroid.parse(script)
        assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="merge-parameter-pandas", node=call_node)):
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)

    def test_merge_parameter_pandas_checker_set(self):
        script = """
            import pandas as pd
            df1 = pd.DataFrame({'key': ['foo', 'bar', 'baz', 'foo'],
                                'value': [1, 2, 3, 5]})
            df2 = pd.DataFrame({'key': ['foo', 'bar', 'baz', 'foo'],
                                'value': [5, 6, 7, 8]})                  
            df3 = df1.merge(df2, how='inner', on='key', validate='m:m')     #@
        """
        module = astroid.parse(script)
        assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)
