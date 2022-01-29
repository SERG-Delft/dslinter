import astroid
import pylint.testutils

import dslinter.plugin


class TestUnnecessaryIterationTensorflow(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.UnnecessaryIterationTensorflowChecker

    def test_iteration(self):
        module_tree = astroid.parse("import tensorflow as tf\nx = tf.random.uniform([500, 10])\nz = tf.zeros([10])\nfor i in range(500):\n\tz += x[i]")
        for_node = module_tree.body[-1]
        with self.assertAddsMessages(pylint.testutils.Message(msg_id="iteration-tensorflow", node = for_node),):
            self.checker.visit_for(for_node)

