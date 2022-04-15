"""Class which tests DependentThresholdScikitLearnChecker."""
import astroid
import pylint.testutils
import dslinter.plugin


class TestDependentThresholdScikitLearnChecker(pylint.testutils.CheckerTestCase):
    """Class which tests DependentThresholdScikitLearnChecker."""

    CHECKER_CLASS = dslinter.plugin.DependentThresholdScikitLearnChecker

    def test_with_auc_used(self):
        script = """
        import numpy as np
        from sklearn.metrics import auc
        y = np.array([1, 1, 2, 2])
        pred = np.array([0.1, 0.4, 0.35, 0.8])
        fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=2)
        auc(fpr, tpr)
        
        from sklearn.metrics import f1_score
        y_true = [0, 1, 2, 0, 1, 2]
        y_pred = [0, 2, 1, 0, 0, 1]
        f1_score(y_true, y_pred, average='macro')
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_with_only_f1_score_used(self):
        script = """
        from sklearn.metrics import f1_score
        y_true = [0, 1, 2, 0, 1, 2]
        y_pred = [0, 2, 1, 0, 0, 1]
        f1_score(y_true, y_pred, average='macro')
        """
        module = astroid.parse(script)
        f1_score_node = module.body[-1].value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="dependent-threshold-scikitlearn", node=f1_score_node)):
            self.checker.visit_module(module)
