"""Class which tests the InPlaceNumpyChecker"""
import astroid
import pylint.testutils
import dslinter


class TestInPlaceNumpyChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the InPlaceNumpyChecker"""

    CHECKER_CLASS = dslinter.plugin.InPlaceNumpyChecker

    def test_operation_call_unassigned1(self):
        """Test whether a message is added when the result is lost."""
        script = """
        import numpy as np
        np.clip([1,2,3] ,1, -1) #@
        """
        unassigned_call = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="inplace-numpy", node=unassigned_call)):
            self.checker.visit_call(unassigned_call)

    def test_operation_call_unassigned2(self):
        """Test whether a message is added when the result is lost."""
        script = """
        import numpy as np
        np.sin(1) #@
        """
        unassigned_call = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="inplace-numpy", node=unassigned_call)):
            self.checker.visit_call(unassigned_call)

    def test_operation_call_assigned(self):
        """Test whether no message is added when the result is assigned."""
        script = """
        import numpy as np
        a = np.clip([1,2,3], 1, -1) #@
        """
        assigned_call = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_call(assigned_call)

    def test_operation_call_inplace(self):
        """Test whether no message is added when the inplace parameter is set."""
        script = """
        import numpy as np
        a = np.array([1,2,3]) 
        np.clip(a, 1, -1, out = a) #@
        """
        unassigned_call = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_call(unassigned_call)

    def test_np_call_in_a_function(self):
        """Test whether no message is added when the call is in a another call."""
        script = """
        import numpy as np
        print(np.sum(y)) #@
        """
        call_node = astroid.extract_node(script).args[0]
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_np_call_in_return_node(self):
        """Test whether no message is added when the call is in a return node."""
        script = """
        import numpy as np
        def test_function():
            return np.sum() #@
        """
        call_node = astroid.extract_node(script).value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_call_name_in_whitelist(self):
        """Tesr whether no message is added if the call name is in whitelist"""
        script = """
        import numpy as np
        a = [1, 2, 3]
        np.save(a) #@
        """
        call_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_call(call_node)
