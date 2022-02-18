"""Class which tests the InPlaceNumpyChecker"""
import astroid
import pylint.testutils
import dslinter


class TestInPlaceNumpy(pylint.testutils.CheckerTestCase):
    """Class which tests the InPlaceNumpyChecker"""

    CHECKER_CLASS = dslinter.plugin.InPlaceNumpyChecker

    NP_INIT = "import numpy as np\n"

    def test_operation_call_unassigned1(self):
        """Test whether a message is added when the result is lost."""
        module_tree = astroid.parse(self.NP_INIT + "np.clip([1,2,3] ,1, -1)")
        unassigned_call = module_tree.body[-1].value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id = "inplace-numpy", node = unassigned_call)):
            self.checker.visit_call(unassigned_call)

    def test_operation_call_unassigned2(self):
        """Test whether a message is added when the result is lost."""
        module_tree = astroid.parse(self.NP_INIT + "np.sin(1)")
        unassigned_call = module_tree.body[-1].value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id = "inplace-numpy", node = unassigned_call)):
            self.checker.visit_call(unassigned_call)

    def test_operation_call_assigned(self):
        """Test whether no message is added when the result is assigned."""
        module_tree = astroid.parse(self.NP_INIT + "a = np.clip([1,2,3], 1, -1)")
        assigned_call = module_tree.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_call(assigned_call)

    def test_operation_call_inplace(self):
        """Test whether no message is added when the inplace parameter is set."""
        module_tree = astroid.parse(self.NP_INIT + "a = np.array([1,2,3])\nnp.clip(a, 1, -1, out = a)")
        unassigned_call = module_tree.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_call(unassigned_call)
