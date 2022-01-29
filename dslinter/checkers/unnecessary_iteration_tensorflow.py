from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
import astroid
from dslinter.util.exception_handler import ExceptionHandler

class UnnecessaryIterationTensorflowChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = ""
    priority = -1
    msgs = {
        "iteration-tensorflow",
        "iteration-tensorflow",
        "iteration-tensorflow",
    }
    options = ()

    def visit_for(self, node: astroid.Call):
        """ Evaluate whether there is a reduction operation in the loop"""
        try:
            if not (
                isinstance(node.iter, astroid.Call)
            ):
                return
            if(isinstance(node.body[0], astroid.AugAssign)):
                print("isinstance(node.body, astroid.nodes.AugAssign)")
                self.add_message("iteration-tensorflow", node=node)
        except:
            Exception.handler(self, node)

