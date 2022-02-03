import astroid
import pylint.testutils
import dslinter.plugin


class TestMemoryReleaseTensorflowChecker(pylint.testutils.CheckerTestCase):
    """Test checks whether the memory is released in time in Tensorflow code."""

    CHECKER_CLASS = dslinter.plugin.MemoryReleaseTensorflowChecker

    def test_iteration(self):
        """Check whether a message is added is there is no clear_session() before model creation in the loop"""
        module_tree = astroid.parse("import tensorflow as tf\nfor _ in range(100):\n\tmodel = tf.keras.Sequential([tf.keras.layers.Dense(10) for _ in range(10)])")
        for_node = module_tree.body[-1]
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id = "memory-release-tensorflow", node = for_node),):
            self.checker.visit_for(for_node)

    def test_memory_clear_in_iteration(self):
        """Check whether no message is added is there is a clear_session() before model creation in the loop"""
        module_tree = astroid.parse("import tensorflow as tf\nfor _ in range(100):\n\ttf.keras.backend.clear_session()\n\tmodel = tf.keras.Sequential([tf.keras.layers.Dense(10) for _ in range(10)])")
        for_node = module_tree.body[-1]
        with self.assertNoMessages():
            self.checker.visit_for(for_node)
