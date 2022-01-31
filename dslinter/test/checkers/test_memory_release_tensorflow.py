import astroid
import pylint.testutils
import dslinter.plugin


class TestMemoryReleaseTensorflowChecker(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.MemoryReleaseTensorflowChecker

    def test_iteration(self):
        module_tree = astroid.parse("import tensorflow as tf\nfor _ in range(100):\n\tmodel = tf.keras.Sequential([tf.keras.layers.Dense(10) for _ in range(10)])")
        for_node = module_tree.body[-1]
        with self.assertAddsMessages(pylint.testutils.Message(msg_id = "memory", node = for_node),):
            self.checker.visit_for(for_node)


