"""Class which tests the HyperparameterPyTorchChecker."""
import astroid
import pylint.testutils
import dslinter.plugin


class TestHyperparameterPyTorchChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the HyperparameterPyTorchChecker."""

    CHECKER_CLASS = dslinter.plugin.HyperparameterPyTorchChecker

    def test_batch_size_set(self):
        script = """
        from torch.utils.data import DataLoader #@
        DataLoader(dataset, batch_size=4)     #@
        """
        importfrom_node, call_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(call_node)

    def test_batch_size_not_set(self):
        script = """
        from torch.utils.data import DataLoader #@
        DataLoader(dataset)   #@
        """
        importfrom_node, call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameter-pytorch", node=call_node)):
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(call_node)

    def test_momentum_set(self):
        script = """
        from torch.optim import SGD #@
        optimizer = SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay = 0) #@
        """
        importfrom_node, assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertNoMessages():
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(call_node)

    def test_momentum_not_set(self):
        script = """
        from torch.optim import SGD #@
        optimizer = SGD(model.parameters(), lr=0.01) #@
        """
        importfrom_node, assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameter-pytorch", node=call_node)):
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(call_node)
