"""Checker which checks whether random seed is set in pytorch dataloader"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid


class RandomnessControlDataloaderPytorchChecker(BaseChecker):
    """Checker which checks whether random seed is set in pytorch dataloader"""
    __implements__ = IAstroidChecker

    name = "randomness-control-dataloader-pytorch"
    priority = -1
    msgs = {
        "W5565": (
            "worker_init_fn() and generator is not set in PyTorch DataLoader API",
            "randomness-control-dataloader-pytorch",
            "Use worker_init_fn() and generator in PyTorch DataLoader API to preserve reproducibility"
        )
    }
    options = ()

    def visit_call(self, node: astroid.Call):
        """
        Check whether there is a rule violation.
        :param node:
        """
        keywords = []
        if(
            hasattr(node.func, "name")
            and node.func.name == "DataLoader"
        ):
            if hasattr(node, "keywords"):
                for k in node.keywords:
                    if hasattr(k, "arg"):
                        keywords.append(k.arg)
            if(
                "worker_init_fn" not in keywords
                or "generator" not in keywords
            ):
                self.add_message("randomness-control-dataloader-pytorch", node=node)
