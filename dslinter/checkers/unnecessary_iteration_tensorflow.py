from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
import astroid
from dslinter.util.exception_handler import ExceptionHandler

class UnnecessaryIterationTensorflowChecker(BaseChecker):
    """Check whether there is an unnecessary iteration in Tensorflow code."""
    __implements__ = IAstroidChecker

    name = "unnecessary_iteration_tensorflow"
    priority = -1
    msgs = {
        "":{
            "There is an unnecessary iteration.",
            "iteration-tensorflow",
            "There is a efficient solution(Vectorization or Reduction) to replace the iteration.",
        }
    }
    options = ()

    def visit_for(self, node: astroid.Call):
        """Evaluate whether there is an augmented assign in the loop, it can be replaced by a reduction operation, which is faster."""
        try:
            if(isinstance(node.body[0], astroid.AugAssign)):
                self.add_message("iteration-tensorflow", node=node)
        except:
            ExceptionHandler.handle(self, node)
