"""Hyperparameter checker for pytorch checks whether important hyperparameters are set."""
import astroid as astroid
from pylint.interfaces import IAstroidChecker
from dslinter.checkers.hyperparameters import HyperparameterChecker
from pylint.lint import PyLinter
from dslinter.utils.exception_handler import ExceptionHandler


class HyperparameterTensorflowChecker(HyperparameterChecker):
    """Hyperparameter checker for pytorch checks whether important hyperparameters are set."""

    __implements__ = IAstroidChecker

    name = "hyperparameter_tensorflow"
    priority = -1
    msgs = {
        "W5533": (
            "Some of the important hyperparameters(learning rate, batch size, momentum, and weight decay) is not set in the program.",
            "hyperparameter-tensorflow",
            "Important hyperparameters should be set in the program."
        )
    }

    def __init__(self, linter: PyLinter = HyperparameterChecker):
        super(HyperparameterTensorflowChecker, self).__init__(linter)
        self.HYPERPARAMETER_RESOURCE = "hyperparameters_tensorflow_dict.pickle"
        self.MESSAGE = "hyperparameter-tensorflow"
        self.HYPERPARAMETERS_MAIN = {
            # training
            # optimizer
            "Adadelta": {"positional": 5,"keywords": ["learning_rate"]},
            "Adagrad": {'positional': 5,"keywords": ["learning_rate"]},
            "Adam": {'positional': 7, "keywords": ["learning_rate"]},
            "Adamax": {'positional': 6, "keywords": ["learning_rate"]},
            "Ftrl": {'positional': 9, "keywords": ["learning_rate"]},
            "Nadam": {'positional': 6, "keywords": ["learning_rate"]},
            "RMSprop": {'positional': 7, "keywords": ["earning_rate", "momentum"]},
            "SGD": {'positional': 5, "keywords": ["learning_rate", "momentum"]},
        }
        self.HYPERPARAMETERS_MAIN2 = {
            "fit": {"positional": 19,"keywords": ["batch_size"]},
        }

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether hyperparameters are set.

        In strict mode, all hyperparameters should be set.
        In non-strict mode, function calls to learning functions should either contain all
        hyperparameters defined in HYPERPARAMETERS_MAIN or have at least one hyperparameter defined.

        :param node: Node which is visited.
        """
        try:
            # pdb.set_trace()
            if(
                hasattr(node, "func")
                and hasattr(node.func, "name")
            ):
                self.hyperparameter_in_class(node, node.func.name)
            if(
                hasattr(node, "func")
                and hasattr(node.func, "attrname")
                and node.func.attrname == "fit"
            ):
                self.hyperparameters_in_function(node)

        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

    def hyperparameters_in_function(self, node: astroid.Call):
        self.has_required_hyperparameters(node, self.HYPERPARAMETERS_MAIN2, node.func.attrname)

        hyperparams_all = {
            "fit": {"positional": 19,"keywords": ["x", "y", "batch_size", "epochs", "verbose",
                                                  "callbacks", "validation_split", "validation_data", "shuffle",
                                                  "class_weight", "sample_weight", "initial_epoch", "steps_per_epoch",
                                                  "validation_steps", "validation_batch_size", "validation_freq",
                                                  "max_queue_size", "workers", "use_multiprocessing"]},
        }

        function_name = node.func.attrname

        if function_name in hyperparams_all:  # pylint: disable=unsupported-membership-test
            if self.config.strict_hyperparameters: # strict mode
                if not self.has_required_hyperparameters(node, hyperparams_all, function_name):
                    self.add_message(self.MESSAGE, node=node)
            else:  # non-strict mode
                if (
                    function_name in self.HYPERPARAMETERS_MAIN2
                    and not self.has_required_hyperparameters(node, self.HYPERPARAMETERS_MAIN2, function_name)
                ):
                    self.add_message(self.MESSAGE, node=node)
                elif len(node.args) == 0 and node.keywords is None:
                    self.add_message(self.MESSAGE, node=node)
