"""Class which tests UnnecessaryIterationTensorflowChecker"""
import astroid
import pylint.testutils
import dslinter.plugin


class TestUnnecessaryIterationTensorflowChecker(pylint.testutils.CheckerTestCase):
    """Class which tests UnnecessaryIterationTensorflowChecker"""
    CHECKER_CLASS = dslinter.plugin.UnnecessaryIterationTensorflowChecker

    def test_iteration(self):
        """Test whether there is a message added when there is a iteration with augmented assign."""
        script = """
            import tensorflow as tf
            x = tf.random.uniform([500, 10]) 
            z = tf.zeros([10])
            for i in range(500): #@
                z += x[i]
        """
        module_node = astroid.parse(script)
        for_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="iteration-tensorflow", node = for_node),):
            self.checker.visit_module(module_node)
            self.checker.visit_for(for_node)

    def test_no_iteration(self):
        """Test whether there is no message added when there is no iteration."""
        script = """
            import tensorflow as tf
            x = tf.random.uniform([500, 10])
            z = tf.reduce_sum(x, axis=0) #@
        """
        module_node = astroid.parse(script)
        for_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_module(module_node)
            self.checker.visit_for(for_node)
