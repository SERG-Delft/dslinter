"""Class which tests MaskMissingTensorflowChecker."""
import astroid
import pylint.testutils

import dslinter.plugin


class TestMaskMissingTensorflowChecker(pylint.testutils.CheckerTestCase):
    """Class which tests MaskMissingTensorflowChecker."""

    CHECKER_CLASS = dslinter.plugin.MaskMissingTensorflowChecker

    def test_missing_mask_1(self):
        script = """
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y_conv),reduction_indices=[1])) #@
        """
        module = astroid.parse(script)
        node = astroid.extract_node(script)
        call_node = node.value.args[0].operand.args[0].right
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="missing-mask-tensorflow", node = call_node)):
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)

    def test_missing_mask_2(self):
        script = """
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y_conv + 1e-9),reduction_indices=[1])) #@
        """
        module = astroid.parse(script)
        node = astroid.extract_node(script)
        call_node = node.value.args[0].operand.args[0].right
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="missing-mask-tensorflow", node = call_node)):
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)

    def test_with_mask_1(self):
        script = """
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(tf.clip_by_value(y_conv,1e-10,1.0)),reduction_indices=[1])) #@
        """
        module = astroid.parse(script)
        node = astroid.extract_node(script)
        call_node = node.value.args[0].operand.args[0].right
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)

    def test_with_mask_2(self):
        script = """
        y_conv = tf.clip_by_value(y_conv,1e-10,1.0)
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y_conv),reduction_indices=[1])) #@
        """
        module = astroid.parse(script)
        node = astroid.extract_node(script)
        call_node = node.value.args[0].operand.args[0].right
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_call(call_node)
