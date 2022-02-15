"""Class which tests RandomnessControllingPytorchChecker"""
import astroid
import pylint.testutils
import dslinter


class TestRandomnessControllingPytorchChecker(pylint.testutils.CheckerTestCase):
    """Class which tests RandomnessControllingPytorchChecker"""

    CHECKER_CLASS = dslinter.plugin.RandomnessControllingPytorchChecker

    def test_with_pytorch_randomness_control(self):
        """Tests whether no message is added if manual seed is set."""
        script = """
        import torch #@
        torch.manual_seed(0) #@
        torch.randn(10).index_copy(0, torch.tensor([0]), torch.randn(1))
        """
        import_node, call_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)

    def test_without_pytorch_randomness_control(self):
        """Tests whether a message is added if manual seed is not set"""
        script = """
        import torch #@
        torch.randn(10).index_copy(0, torch.tensor([0]), torch.randn(1)) #@
        """
        import_node, call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="randomness-control-pytorch", node = call_node)):
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)
