import astroid
import pylint.testutils

import dslinter.plugin


class TestHyperparameterPyTorchChecker(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.HyperparameterPyTorchChecker

    def test_batch_size_set(self):
        script = """
        from torch.utils.data import DataLoader
        DataLoader(dataset, batch_size=4)     #@
        """
        call_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_batch_size_not_set(self):
        script = """
        from torch.utils.data import DataLoader
        DataLoader(dataset)   #@
        """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameter-pytorch", node=call_node)):
            self.checker.visit_call(call_node)

    def test_momentum_set(self):
        script = """
        optimizer = SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay = 0) #@
        """
        call_node = astroid.extract_node(script).value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_momentum_not_set(self):
        script = """
        optimizer = SGD(model.parameters(), lr=0.01) #@
        """
        call_node = astroid.extract_node(script).value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameter-pytorch", node=call_node)):
            self.checker.visit_call(call_node)
