"""Class which tests RandomnessControllingTensorflowChecker"""
import astroid
import pylint.testutils
import dslinter


class TestRandomnessControllingTensorflowChecker(pylint.testutils.CheckerTestCase):
    """Class which tests RandomnessControllingTensorflowChecker"""

    CHECKER_CLASS = dslinter.plugin.RandomnessControllingTensorflowChecker

    def test_with_tensorflow_randomness_control(self):
        """Tests whether no message is added if manual seed is set."""
        script = """
        import tensorflow as tf #@
        tf.random.set_seed(0)
        tf.random.uniform([1])
        """
        import_node = astroid.extract_node(script)
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_module(module)

    def test_without_tensorflow_randomness_control(self):
        """Tests whether a message is added if manual seed is not set"""
        script = """
        import tensorflow as tf #@
        tf.random.uniform([1])
        """
        import_node = astroid.extract_node(script)
        module = astroid.parse(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="randomness-control-tensorflow", node = module)):
            self.checker.visit_import(import_node)
            self.checker.visit_module(module)
