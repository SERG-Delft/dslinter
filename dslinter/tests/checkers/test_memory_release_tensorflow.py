"""Test checks whether the memory is released in time in Tensorflow code."""
import astroid
import pylint.testutils
import dslinter.plugin


class TestMemoryReleaseTensorflowChecker(pylint.testutils.CheckerTestCase):
    """Test checks whether the memory is released in time in Tensorflow code."""

    CHECKER_CLASS = dslinter.plugin.MemoryReleaseTensorflowChecker

    def test_iteration(self):
        """Check whether a message is added is there is no clear_session() before model creation in the loop"""
        script = """
            import tensorflow as tf
            for _ in range(100): #@
                model = tf.keras.Sequential([tf.keras.layers.Dense(10) for _ in range(10)]) 
        """
        module_tree = astroid.parse(script)
        for_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="memory-release-tensorflow", node=for_node),):
            self.checker.visit_module(module_tree)
            self.checker.visit_for(for_node)

    def test_memory_clear_in_iteration(self):
        """Check whether no message is added is there is a clear_session() before model creation in the loop"""
        script = """
            import tensorflow as tf
            for _ in range(100): #@
                tf.keras.backend.clear_session()
                model = tf.keras.Sequential([tf.keras.layers.Dense(10) for _ in range(10)])
        """
        module_tree = astroid.parse(script)
        for_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_module(module_tree)
            self.checker.visit_for(for_node)
