"""Class which tests TensorArrayTensorflowChecker."""
import astroid as astroid
import pylint.testutils

import dslinter


class TestTensorArrayTensorflowChecker(pylint.testutils.CheckerTestCase):
    """Class which tests TensorArrayTensorflowChecker."""

    CHECKER_CLASS = dslinter.plugin.TensorArrayTensorflowChecker

    def test_not_use_tensor_array(self):
        """Message should be added if tf.constant() type variable is changed in the loop."""
        script = """
        import tensorflow as tf
        @tf.function
        def fibonacci(n):
            a = tf.constant(1)
            b = tf.constant(1)
            c = tf.constant([1, 1])
        
            for i in range(2, n): #@
                a, b = b, a + b
                c = tf.concat([c, [b]], 0)
            
            return c
            
        n = tf.constant(5)
        d = fibonacci(n)        
        """
        module = astroid.parse(script)
        for_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="tensor-array-tensorflow", node=for_node)):
            self.checker.visit_module(module)
            self.checker.visit_for(for_node)

    def test_use_tensor_array(self):
        """No message should be added if tf.TensorArray() type variable is changed in the loop."""
        script = """
        import tensorflow as tf
        @tf.function
        def fibonacci(n):
            a = tf.constant(1)
            b = tf.constant(1)
            c = tf.TensorArray(tf.int32, n)
            c = c.write(0, a)
            c = c.write(1, b)
        
            for i in range(2, n): #@
                a, b = b, a + b
                c = c.write(i, b)
            
            return c.stack()
            
        n = tf.constant(5)
        d = fibonacci(n)        
        """
        module = astroid.parse(script)
        for_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_for(for_node)
