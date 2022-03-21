import astroid
import pylint.testutils

import dslinter


class TestDataframeConversionPandasChecker(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.DataframeConversionPandasChecker

    def test_dataframe_conversion_incorrectly_used(self):
        script = """
        import numpy as np
        import pandas as pd
        
        index = [1, 2, 3, 4, 5, 6, 7]
        a = [np.nan, np.nan, np.nan, 0.1, 0.1, 0.1, 0.1]
        b = [0.2, np.nan, 0.2, 0.2, 0.2, np.nan, np.nan]
        c = [np.nan, 0.5, 0.5, np.nan, 0.5, 0.5, np.nan]
        df = pd.DataFrame({'A': a, 'B': b, 'C': c}, index=index)
        # df = df.rename_axis('ID')
        arr = df.values #@     
        """
        module = astroid.parse(script)
        call_node = astroid.extract_node(script).value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="dataframe-conversion-pandas", node=call_node)):
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)

    def test_dataframe_conversion_correctly_used(self):
        script = """
        import numpy as np
        import pandas as pd
        
        index = [1, 2, 3, 4, 5, 6, 7]
        a = [np.nan, np.nan, np.nan, 0.1, 0.1, 0.1, 0.1]
        b = [0.2, np.nan, 0.2, 0.2, 0.2, np.nan, np.nan]
        c = [np.nan, 0.5, 0.5, np.nan, 0.5, 0.5, np.nan]
        df = pd.DataFrame({'A': a, 'B': b, 'C': c}, index=index)
        # df = df.rename_axis('ID')
        arr = df.to_numpy()   #@
        """
        module = astroid.parse(script)
        call_node = astroid.extract_node(script).value
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)
