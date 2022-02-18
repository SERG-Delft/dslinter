"""Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""
from typing import List, Dict
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.resources import Resources
from pylint.lint import PyLinter


class HyperparameterChecker(BaseChecker):
    """Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""

    __implements__ = IAstroidChecker

    options = (
        (
            "strict_hyperparameters",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Force that all parameters of learning algorithms are set.",
            },
        ),
    )

    def __init__(self, linter: PyLinter = None) -> None:
        super(HyperparameterChecker, self).__init__(linter)
        self.HYPERPARAMETERS_MAIN = {}
        self.HYPERPARAMETER_RESOURCE = ""
        self.MESSAGE = ""

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether hyperparameters are set.

        In strict mode, all hyperparameters should be set.
        In non-strict mode, function calls to learning functions should either contain all
        hyperparameters defined in HYPERPARAMETERS_MAIN or have at least one hyperparameter defined.

        :param node: Node which is visited.
        """
        try:
            if(
                hasattr(node, "func")
                and hasattr(node.func, "name")
            ):
                self.hyperparameter_in_class(node, node.func.name)
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

    def hyperparameter_in_class(self, node: astroid.Call, function_name: str):
            hyperparams_all = Resources.get_hyperparameters(self.HYPERPARAMETER_RESOURCE)

            if function_name in hyperparams_all:  # pylint: disable=unsupported-membership-test
                if self.config.strict_hyperparameters: # strict mode
                    if not self.has_required_hyperparameters(node, hyperparams_all, function_name):
                        self.add_message(self.MESSAGE, node=node)
                else:  # non-strict mode
                    if (
                        function_name in self.HYPERPARAMETERS_MAIN
                        and not self.has_required_hyperparameters(node, self.HYPERPARAMETERS_MAIN, function_name)
                    ):
                        self.add_message(self.MESSAGE, node=node)
                    elif len(node.args) == 0 and node.keywords is None:
                        self.add_message(self.MESSAGE, node=node)

    def has_required_hyperparameters(self, node: astroid.Call, hyperparameters: Dict, name: str):
        """
        Evaluate whether a function call has all required hyperparameters defined.

        :param node: Node which is visited.
        :param hyperparameters: Dict of functions with their required hyperparameters.
        :return: True when all required hyperparameters are defined.
        """
        return len(node.args) >= hyperparameters[name]["positional"] or self.has_keywords(
            node.keywords, hyperparameters[name]["keywords"]
        )

    @staticmethod
    def has_keywords(keywords: List[astroid.Keyword], keywords_goal: List[str]) -> bool:
        """
        Check if a list of keywords contains certain keywords.

        :param keywords: List of keywords.
        :param keywords_goal: Name of the keywords which are checked against.
        :return: True if keywords are present, False if they are not.
        """
        if keywords is None:
            return False

        found = 0
        for keyword in keywords:
            if keyword.arg in keywords_goal:
                found += 1

        return found == len(keywords_goal)
