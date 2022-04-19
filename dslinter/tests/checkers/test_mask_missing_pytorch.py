"""Class which tests MaskMissingPytorchChecker."""
import astroid
import pylint.testutils

import dslinter.plugin


class TestMaskMissingPytorchChecker(pylint.testutils.CheckerTestCase):
    """Class which tests MaskMissingPytorchChecker."""

    CHECKER_CLASS = dslinter.plugin.MaskMissingPytorchChecker

    def test_missing_mask_1(self):
        script = """
        action_mask = torch.log(action_mask) #@
        """
        module = astroid.parse(script)
        node = astroid.extract_node(script)
        call_node = node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="missing-mask-pytorch", node = call_node)):
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)

    def test_missing_mask_2(self):
        script = """
        action_mask = torch.log(action_mask + 1e-9) #@
        """
        module = astroid.parse(script)
        node = astroid.extract_node(script)
        call_node = node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="missing-mask-pytorch", node = call_node)):
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)

    def test_with_mask_1(self):
        script = """
        action_mask = torch.log(torch.clip(action_mask, FLOAT_MIN, FLOAT_MAX))
        """
        module = astroid.parse(script)
        node = astroid.extract_node(script)
        call_node = node.value
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)

    def test_with_mask_2(self):
        script = """
        action_mask = torch.log(torch.clamp(action_mask, FLOAT_MIN, FLOAT_MAX))
        """
        module = astroid.parse(script)
        node = astroid.extract_node(script)
        call_node = node.value
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)

    def test_with_mask_3(self):
        script = """
        action_mask = torch.clip(action_mask, FLOAT_MIN, FLOAT_MAX)
        action_mask = torch.log(action_mask) #@
        """
        module = astroid.parse(script)
        node = astroid.extract_node(script)
        call_node = node.value
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)
