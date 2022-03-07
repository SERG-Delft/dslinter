import astroid
import pylint.testutils

import dslinter.plugin


class TestMaskMissingPytorchChecker(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.MaskMissingPytorchChecker

    def test_missing_mask(self):
        script = """
        action_mask = torch.log(action_mask) #@
        """
        node = astroid.extract_node(script)
        call_node = node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="missing-mask-pytorch", node = call_node)):
            self.checker.visit_call(call_node)

    def test_with_mask(self):
        script = """
        action_mask = torch.log(torch.clip(action_mask, FLOAT_MIN, FLOAT_MAX))
        """
        node = astroid.extract_node(script)
        call_node = node.value.args[0]
        with self.assertNoMessages():
            self.checker.visit_call(call_node)
