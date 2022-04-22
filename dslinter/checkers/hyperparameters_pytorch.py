"""Hyperparameter checker for pytorch checks whether important hyperparameters are set."""
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter
from dslinter.checkers.hyperparameters import HyperparameterChecker


class HyperparameterPyTorchChecker(HyperparameterChecker):
    """Hyperparameter checker for pytorch checks whether important hyperparameters are set."""

    __implements__ = IAstroidChecker

    name = "hyperparameter-pytorch"
    priority = -1
    msgs = {
        "R5508": (
            "Some of the important hyperparameters(learning rate, batch size, momentum, and weight decay) is not set in the program.",
            "hyperparameter-pytorch",
            "Important hyperparameters should be set in the program."
        )
    }

    options = (
        (
            "strict_hyperparameters_pytorch",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Force that all parameters of learning algorithms are set.",
            },
        ),
    )

    def __init__(self, linter: PyLinter = HyperparameterChecker):
        super().__init__(linter)
        self.HYPERPARAMETER_RESOURCE = "hyperparameters_pytorch_dict.pickle"
        self.MESSAGE = "hyperparameter-pytorch"
        self.HYPERPARAMETERS_MAIN = {
            # dataloader
            "DataLoader": {"positional": 2,"keywords":["batch_size"]},
            # optimizer
            "Adadelta": {"positional": 5, "keywords": ["lr", "weight_decay"]},
            "Adagrad": {"positional": 6, "keywords": ["lr", "weight_decay"]},
            "Adam": {"positional": 6, "keywords": ["lr", "weight_decay"]},
            "AdamW": {"positional": 6, "keywords": ["lr", "weight_decay"]},
            "SparseAdam": {"positional": 4, "keywords": ["lr"]},
            "Adamax": {"positional": 5, "keywords": ["lr", "weight_decay"]},
            "ASGD": {"positional": 6, "keywords": ["lr", "weight_decay"]},
            "LBFGS": {"positional": 8, "keywords": ["lr"]},
            "NAdam": {"positional": 6, "keywords": ["lr", "weight_decay", "momentum_decay"]},
            "RAdam": {"positional": 5, "keywords": ["lr", "weight_decay"]},
            "RMSprop": {"positional": 7, "keywords": ["lr", "weight_decay", "momentum"]},
            "Rprop": {"positional": 4, "keywords": ["lr"]},
            "SGD": {"positional": 6, "keywords": ["lr", "weight_decay", "momentum"]},
        }
        self.LIBRARY = "pytorch"
