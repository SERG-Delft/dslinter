"""Class which tests DependentThresholdPytorchChecker."""
import astroid
import pylint.testutils
import dslinter.plugin


class TestDependentThresholdPytorchChecker(pylint.testutils.CheckerTestCase):
    """Class which tests DependentThresholdPytorchChecker."""

    CHECKER_CLASS = dslinter.plugin.DependentThresholdPytorchChecker

    def test_with_auc_used(self):
        script = """
        from torchmetrics import F1Score
        target = torch.tensor([0, 1, 2, 0, 1, 2])
        preds = torch.tensor([0, 2, 1, 0, 0, 1])
        f1 = F1Score(num_classes=3)
        f1(preds, target)

        from torchmetrics import AUROC
        preds = torch.tensor([0.13, 0.26, 0.08, 0.19, 0.34])
        target = torch.tensor([0, 0, 1, 1, 1])
        auroc = AUROC(pos_label=1)
        auroc(preds, target)
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_with_only_f1_score_used(self):
        script = """
        from torchmetrics import F1Score
        target = torch.tensor([0, 1, 2, 0, 1, 2])
        preds = torch.tensor([0, 2, 1, 0, 0, 1])
        f1 = F1Score(num_classes=3)
        f1(preds, target)
        """
        module = astroid.parse(script)
        f1_score_node = module.body[-2].value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="dependent-threshold-pytorch", node=f1_score_node)):
            self.checker.visit_module(module)
