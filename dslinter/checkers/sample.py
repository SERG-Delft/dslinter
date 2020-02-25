import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class SampleChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'sample'
    priority = -1
    msgs = {
        'W0001': (
            'Returns a non-unique constant.',
            'non-unique-returns',
            'All constants returned in a function should be unique.'
        ),
    }
    options = (
        (
            'ignore-ints',
            {
                'default': False, 'type': 'yn', 'metavar': '<y_or_n>',
                'help': 'Allow returning non-unique integers',
            }
        ),
    )

    def __init__(self, linter=None):
        super(SampleChecker, self).__init__(linter)
        self._function_stack = []

    def visit_functiondef(self, node):
        self._function_stack.append([])

    def leave_functiondef(self, node):
        self._function_stack.pop()

    def visit_return(self, node):
        if not isinstance(node.value, astroid.node_classes.Const):
            return

        for other_return in self._function_stack[-1]:
            if (node.value.value == other_return.value.value and
                    not (self.config.ignore_ints and node.value.pytype() == int)):
                self.add_message(
                    'non-unique-returns', node=node,
                )

        self._function_stack[-1].append(node)
