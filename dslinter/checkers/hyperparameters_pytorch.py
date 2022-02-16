"""Hyperparameter checker for pytorch checks whether important hyperparameters are set."""
import astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from dslinter.util.exception_handler import ExceptionHandler


class HyperparameterPyTorchChecker(BaseChecker):
    """Hyperparameter checker for pytorch checks whether important hyperparameters are set."""

    __implements__ = IAstroidChecker

    name = "hyperparameter_pytorch"
    priority = -1
    msgs = {
        "": (
            "Some of the important hyperparameters(learning rate, batch size, momentum, and weight decay) is not set in the program.",
            "hyperparameter-pytorch",
            "Important hyperparameters should be set in the program."
        )
    }

    OPTIMIZERS = [
        "SGD",
        "Adam"
    ]

    def visit_call(self, node: astroid.Call):
        """"""
        try:
            # if dataloader is used, check whether batch size is set explicitly
            if(
                hasattr(node, "func")
                and hasattr(node.func, "name")
                and node.func.name == "DataLoader"
                and hasattr(node, "keywords")
            ):
                batch_size_set = False
                for k in node.keywords:
                    if(k.arg == "batch_size"):
                        batch_size_set = True
                if(batch_size_set is False):
                    self.add_message("hyperparameter-pytorch", node=node)

            # if optimizer is used, check whether learning rate, momentum and weight_decay are explicitly set.
            if(
                hasattr(node, "func")
                and hasattr(node.func, "attrname")
                and node.func.attrname in self.OPTIMIZERS
            ):
                momentum_set = False
                for k in node.keywords:
                    if(k.arg == "momentum"):
                        momentum_set = True
                if(momentum_set is False):
                    self.add_message("hyperparameter-pytorch", node=node)
        except:
            ExceptionHandler.handle(self, node)

