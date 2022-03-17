import astroid
import pylint.testutils

import dslinter.plugin


class TestDatatypePandasChecker(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.DatatypePandasChecker

    def test_datatype_not_set(self):
        script = """
        df = pd.read_csv('data.csv')  #@   
        """
        assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="datatype-pandas", node=call_node)):
            self.checker.visit_call(call_node)

    def test_datatype_set(self):
        script = """
        df = pd.read_csv('data.csv', dtype={'col1': 'str', 'col2': 'int', 'col3': 'float'})   #@
        """
        assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)


