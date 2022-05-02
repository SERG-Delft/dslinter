"""DependentThresholdPytorchChecker checks whether threshold-independent
evaluation methods(e.g. auc) is used when a threshold-dependent method is used
 in Tensorflow programs, because threshold-independent method is always
 preferred over threshold-dependent method in evaluation."""
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
import astroid

from dslinter.utils.exception_handler import ExceptionHandler


class DependentThresholdTensorflowChecker(BaseChecker):
    """DependentThresholdPytorchChecker checks whether threshold-independent
    evaluation methods(e.g. auc) is used when a threshold-dependent method is used
     in Tensorflow programs, because threshold-independent method is always
     preferred over threshold-dependent method in evaluation."""

    __implements__ = IAstroidChecker

    name = "dependent-threshold-tensorflow"
    priority = -1
    msgs = {
        "W5520": (
            "The F1 Score is used but AUC is not used in the Tensorflow code.",
            "dependent-threshold-tensorflow",
            "The threshold independent evaluation method(e.g., AUC) is preferred over threshold dependent method(e.g., F1 Score)."
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
        try:
            _has_auc = False
            _has_f1_score = False
            _f1_score_node = None

            for nod in module.body:
                if hasattr(nod, "value") and isinstance(nod.value, astroid.Call):
                    call_node = nod.value
                    if(
                        hasattr(call_node, "func")
                        and hasattr(call_node.func, "name")
                        and call_node.func.name == "AUC"
                    ):
                        _has_auc = True
                    if(
                        hasattr(call_node, "func")
                        and hasattr(call_node.func, "name")
                        and call_node.func.name == "F1Score"
                    ):
                        _has_f1_score = True
                        _f1_score_node = call_node

            # if f1 score is used but auc is not used
            if _has_f1_score is True and _has_auc is False:
                self.add_message("dependent-threshold-tensorflow", node=_f1_score_node)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)
