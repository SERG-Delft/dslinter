import astroid
import pylint.testutils
import dslinter.plugin

class TestUnnecessaryIterationTensorflowChecker(pylint.testutils.CheckerTestCase):
    """Class which tests UnnecessaryIterationTensorflowChecker"""
    CHECKER_CLASS = dslinter.plugin.UnnecessaryIterationTensorflowChecker

    def test_iteration(self):
        """Test whether there is a message added when there is a iteration with augmented assign."""
        module_tree = astroid.parse("import tensorflow as tf\nx = tf.random.uniform([500, 10])\nz = tf.zeros([10])\nfor i in range(500):\n\tz += x[i]")
        for_node = module_tree.body[-1]
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="iteration-tensorflow", node = for_node),):
            self.checker.visit_for(for_node)

    def test_no_iteration(self):
        """Test whether there is no message added when there is no iteration."""
        module_tree = astroid.parse("import tensorflow as tf\nx = tf.random.uniform([500, 10])\nz = tf.reduce_sum(x, axis=0)")
        for_node = module_tree.body[-1]
        with self.assertNoMessages():
            self.checker.visit_for(for_node)
