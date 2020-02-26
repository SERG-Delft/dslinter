"""Sample checker which checks for non-unique returns."""
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class SampleChecker(BaseChecker):
    """Sample checker which checks for non-unique returns."""

    __implements__ = IAstroidChecker

    name = "sample"
    priority = -1
    msgs = {
        "W0001": (
            "Returns a non-unique constant.",
            "non-unique-returns",
            "All constants returned in a function should be unique.",
        ),
    }
    options = (
        (
            "ignore-ints",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Allow returning non-unique integers",
            },
        ),
    )

    def __init__(self, linter=None):
        """
        Initialize the checker.

        :param linter: Linter where the checker is added to.
        """
        super(SampleChecker, self).__init__(linter)
        self._function_stack = []

    def visit_functiondef(self, node):  # pylint: disable=unused-argument
        """
        Append an empty list to the stack when a FunctionDef node is visited.

        :param FunctionDef node: Node which is visited.
        """
        self._function_stack.append([])

    def leave_functiondef(self, node):  # pylint: disable=unused-argument
        """
        Pop the list from the stack when a FunctionDef node is left.

        :param FunctionDef node: Node which is left.
        """
        self._function_stack.pop()

    def visit_return(self, node):
        """
        When a return node is visited, check if it returns the same constant as another return node.

        :param Return node: Node which is visited.
        """
        if not isinstance(node.value, astroid.node_classes.Const):
            return

        for other_return in self._function_stack[-1]:
            if node.value.value == other_return.value.value and not (
                self.config.ignore_ints and node.value.pytype() == int
            ):
                self.add_message(
                    "non-unique-returns", node=node,
                )

        self._function_stack[-1].append(node)
