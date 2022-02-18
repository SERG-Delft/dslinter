import astroid
import pylint.testutils

import dslinter.plugin

class TestHyperparameterTensorflowChecker(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.HyperparameterTensorflowChecker

    def test_batch_size_set(self):
        script = """
            import tensorflow as tf
            
            class MyModel(tf.keras.Model):
            
              def __init__(self, *args, **kwargs):
                super(MyModel, self).__init__(*args, **kwargs)
                self.loss_tracker = tf.keras.metrics.Mean(name='loss')
            
              def compute_loss(self, x, y, y_pred, sample_weight):
                loss = tf.reduce_mean(tf.math.squared_difference(y_pred, y))
                loss += tf.add_n(self.losses)
                self.loss_tracker.update_state(loss)
                return loss
            
              def reset_metrics(self):
                self.loss_tracker.reset_states()
            
              @property
              def metrics(self):
                return [self.loss_tracker]
            
            tensors = tf.random.uniform((10, 10)), tf.random.uniform((10,))
            dataset = tf.data.Dataset.from_tensor_slices(tensors).repeat().batch(1)
            
            inputs = tf.keras.layers.Input(shape=(10,), name='my_input')
            outputs = tf.keras.layers.Dense(10)(inputs)
            model = MyModel(inputs, outputs)
            model.add_loss(tf.reduce_sum(outputs))
            
            optimizer = tf.keras.optimizers.SGD()
            model.compile(optimizer, loss='mse', steps_per_execution=10)
            model.fit(dataset, batch_size = 4, epochs=2, steps_per_epoch=10) #@
            print('My custom loss: ', model.loss_tracker.result().numpy())
        """
        call_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_batch_size_not_set(self):
        script = """
            import tensorflow as tf
            
            class MyModel(tf.keras.Model):
            
              def __init__(self, *args, **kwargs):
                super(MyModel, self).__init__(*args, **kwargs)
                self.loss_tracker = tf.keras.metrics.Mean(name='loss')
            
              def compute_loss(self, x, y, y_pred, sample_weight):
                loss = tf.reduce_mean(tf.math.squared_difference(y_pred, y))
                loss += tf.add_n(self.losses)
                self.loss_tracker.update_state(loss)
                return loss
            
              def reset_metrics(self):
                self.loss_tracker.reset_states()
            
              @property
              def metrics(self):
                return [self.loss_tracker]
            
            tensors = tf.random.uniform((10, 10)), tf.random.uniform((10,))
            dataset = tf.data.Dataset.from_tensor_slices(tensors).repeat().batch(1)
            
            inputs = tf.keras.layers.Input(shape=(10,), name='my_input')
            outputs = tf.keras.layers.Dense(10)(inputs)
            model = MyModel(inputs, outputs)
            model.add_loss(tf.reduce_sum(outputs))
            
            optimizer = tf.keras.optimizers.SGD()
            model.compile(optimizer, loss='mse', steps_per_execution=10)
            model.fit(dataset, epochs=2, steps_per_epoch=10) #@
            print('My custom loss: ', model.loss_tracker.result().numpy())
        """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id = "hyperparameter-tensorflow", node = call_node)):
            self.checker.visit_call(call_node)

    def test_learning_rate_set(self):
        script = """
        optimizer = SGD(learning_rate=0.001, momentum = 0) #@
        """
        call_node = astroid.extract_node(script).value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_learning_rate_not_set(self):
        script = """
        optimizer = SGD() #@
        """
        call_node = astroid.extract_node(script).value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id = "hyperparameter-tensorflow", node = call_node)):
            self.checker.visit_call(call_node)
