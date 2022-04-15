"""Class which tests DependentThresholdTensorflowChecker."""
import astroid
import pylint.testutils
import dslinter.plugin


class TestDependentThresholdTensorflowChecker(pylint.testutils.CheckerTestCase):
    """Class which tests DependentThresholdTensorflowChecker."""
    CHECKER_CLASS = dslinter.plugin.DependentThresholdTensorflowChecker

    def test_with_auc_used(self):
        script = """
            import tensorflow as tf
            from tf.keras.metrics import AUC
            AUC(
                num_thresholds=200, curve='ROC',
                summation_method='interpolation', name=None, dtype=None,
                thresholds=None, multi_label=False, num_labels=None, label_weights=None,
                from_logits=False
            )
            F1Score(
                # num_classes: tfa.types.FloatTensorLike,
                # average: str = None,
                # threshold: Optional[FloatTensorLike] = None,
                # name: str = 'f1_score',
                # dtype: tfa.types.AcceptableDTypes = None
            )             
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_with_only_f1_score_used(self):
        script = """
            import tensorflow.addons as tfa
            from tensorflow.addons.metrics import F1Score
            F1Score(
                # num_classes: tfa.types.FloatTensorLike,
                # average: str = None,
                # threshold: Optional[FloatTensorLike] = None,
                # name: str = 'f1_score',
                # dtype: tfa.types.AcceptableDTypes = None
            )
        """
        module = astroid.parse(script)
        f1_score_node = module.body[-1].value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="dependent-threshold-tensorflow", node=f1_score_node)):
            self.checker.visit_module(module)
