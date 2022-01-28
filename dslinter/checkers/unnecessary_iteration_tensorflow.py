from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
import astroid
from dslinter.util.exception_handler import ExceptionHandler

class UnnecessaryIterationTensorflowChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = ""
    priority = -1
    msgs = {

    }
    options = ()

    def visit_call(self):
        try:
            if():
                self.add_message()
        except:
            Exception.handler(self, node)
