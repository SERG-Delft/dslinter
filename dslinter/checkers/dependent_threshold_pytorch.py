"""DependentThresholdPytorchChecker checks whether threshold-independent evaluation methods(e.g. auc) is used
when a threshold-dependent method is used in Pytorch programs, because threshold-independent method is always preferred over threshold-dependent method in evaluation."""
import astroid as astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker


class DependentThresholdPytorchChecker(BaseChecker):
    """DependentThresholdPytorchChecker checks whether threshold-independent evaluation methods(e.g. auc) is used
when a threshold-dependent method is used in pytorch programs, because threshold-independent method is always preferred over threshold-dependent method in evaluation."""

    __implements__ = IAstroidChecker

    name = "dependent-threshold-pytorch"
    priority = -1
    msgs = {
        "W5592": (
            "dependent-threshold-pytorch",
            "dependent-threshold-pytorch",
            "dependent-threshold-pytorch"
        )
    }

    options = ()

    def visit_module(self, module):
        """
        When a module node is visited, check whether there is f1 score function called.
        If true, check whether there is auc function.
        If f1 score is called but auc is not called, the rule is violated.
        :param module:
        :return:
        """

        __has_auc = False
        __has_f1_score = False

        for n in module.body:
            if(
                hasattr(n, "value")
                and isinstance(n.value, astroid.Call)
            ):
                call_node = n.value
                if(
                    hasattr(call_node, "func")
                    and hasattr(call_node.func, "name")
                    and call_node.func.name == "AUROC"
                ):
                    __has_auc = True
                if(
                    hasattr(call_node, "func")
                    and hasattr(call_node.func, "name")
                    and call_node.func.name == "F1Score"
                ):
                    __has_f1_score = True

        # if f1 score is used but auc is not used
        if(__has_f1_score == True and __has_auc == False):
            self.add_message("dependent-threshold-pytorch", node = module)
