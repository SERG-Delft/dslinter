import pylint.testutils
import dslinter
import astroid

class TestInPlaceNumpy(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.InPlaceNumpyChecker

    NP_INIT = "import numpy as np\n"

    def test_operation_call_unassigned(self):
        module_tree = astroid.parse(self.NP_INIT + "np.clip()")
        unassigned_call = module_tree.body[-1].value
        with self.assertAddsMessages(pylint.testutils.Message(msg_id = "inplace-misused-numpy", node = unassigned_call)):
            self.checker.visit_call(unassigned_call)

    def test_operation_call_assigned(self):
        module_tree = astroid.parse(self.NP_INIT + "a = np.clip()")
        assigned_call = module_tree.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_call(assigned_call)


