"""Checker which checks whether random seed is set in pytorch dataloader"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid


class RandomnessControllingDataloaderPytorchChecker(BaseChecker):
    """Checker which checks whether random seed is set in pytorch dataloader"""
    __implements__ = IAstroidChecker

    name = "randomness_control_dataloader_pytorch"
    priority = -1
    msgs = {
        "W5575" : (
            "worker_init_fn() and generator is not set in pytorch dataloader",
            "randomness-control-dataloader-pytorch",
            "Use worker_init_fn() and generator to preserve reproducibility"
        )
    }
    options = ()

    def visit_call(self, node: astroid.Call):
        """
        Check whether there is a rule violation.
        :param node:
        """
        keywords = []
        if hasattr(node, "keywords"):
            for k in node.keywords:
                if hasattr(k, "arg"):
                    keywords.append(k.arg)
        if(
            "worker_init_fn" not in keywords
            or "generator" not in keywords
        ):
            self.add_message("randomness-control-dataloader-pytorch", node = node)

