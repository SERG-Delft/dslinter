""""""
import astroid as astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker

class DependentThresholdScikitLearnChecker(BaseChecker):
    """"""
    __implements__ = IAstroidChecker

    name = "dependent_threshold_scikitlearn"
    priority = -1
    msgs = {
        "": (
            "dependent-threshold-scikitlearn",
            "dependent-threshold-scikitlearn",
            "dependent-threshold-scikitlearn"
        )
    }

    options = ()

    def visit_module(self, module):

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
                    and call_node.func.name == "auc"
                ):
                    __has_auc = True
                if(
                    hasattr(call_node, "func")
                    and hasattr(call_node.func, "name")
                    and call_node.func.name == "f1_score"
                ):
                    __has_f1_score = True

        # if f1 score is used but auc is not used
        if(__has_f1_score == True and __has_auc == False):
            self.add_message("dependent-threshold-scikitlearn", node = module)
