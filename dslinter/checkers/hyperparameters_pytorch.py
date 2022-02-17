"""Hyperparameter checker for pytorch checks whether important hyperparameters are set."""
from typing import Dict
import astroid
from pylint.interfaces import IAstroidChecker
from dslinter.checkers.hyperparameter import HyperparameterChecker
from dslinter.util.exception_handler import ExceptionHandler


class HyperparameterPyTorchChecker(HyperparameterChecker):
    """Hyperparameter checker for pytorch checks whether important hyperparameters are set."""

    # __implements__ = IAstroidChecker

    name = "hyperparameter_pytorch"
    priority = -1
    msgs = {
        "": (
            "Some of the important hyperparameters(learning rate, batch size, momentum, and weight decay) is not set in the program.",
            "hyperparameter-pytorch",
            "Important hyperparameters should be set in the program."
        )
    }

    OPTIMIZERS = {
        "Adadelta": {"keywords": ["lr", "weight_decay"]},
        "Adagrad": {"keywords": ["lr", "weight_decay"]},
        "Adam": {"keywords": ["lr", "weight_decay"]},
        "AdamW": {"keywords": ["lr", "weight_decay"]},
        "SparseAdam": {"keywords": ["lr"]},
        "Adamax": {"keywords": ["lr", "weight_decay"]},
        "ASGD": {"keywords": ["lr", "weight_decay"]},
        "LBFGS": {"keywords": ["lr"]},
        "NAdam": {"keywords": ["lr", "weight_decay", "momentum_decay"]},
        "RAdam": {"keywords": ["lr", "weight_decay"]},
        "RMSprop": {"keywords": ["lr", "weight_decay", "momentum"]},
        "Rprop": {"keywords": ["lr"]},
        "SGD": {"keywords": ["lr", "weight_decay", "momentum"]},
    }

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
                and not self.has_required_hyperparameters(node, self.OPTIMIZERS)
            ):
                self.add_message("hyperparameter-pytorch", node=node)
        except:
            ExceptionHandler.handle(self, node)

    def has_required_hyperparameters(self, node, hyperparameters: Dict):
        """"""
        return self._has_keywords(
            node.keywords, hyperparameters[node.func.attrname]["keywords"]
        )

