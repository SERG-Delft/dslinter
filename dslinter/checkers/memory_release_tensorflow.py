"""Check whether the memory is freed in time."""
import astroid
from pylint.checkers import BaseChecker

class MemoryReleaseTensorflowChecker(BaseChecker):
    """Check whether the memory is freed in time."""

    name = "memory_release_tensorflow"
    priority = -1
    msgs = {
        "":{
            "The memory has not freed in time.",
            "memory-release-tensorflow",
            "`clean_session()` can be used to free memory in the loop."
        }
    }
    options = ()

    MODELS = [
        "Sequential",
        "Model"
    ]

    def visit_for(self, node: astroid.Call):
        """Evaluate whether memory is freed in a loop with model creation."""
        has_clear_session = False

        for item in node.body:
            # if there is no clear_session call before calling a model, the rule is violated.
            if item.value.func.attrname == "clear_session":
                has_clear_session = True
            if (item.value.func.attrname in self.MODELS and has_clear_session is False):
                self.add_message("memory-release-tensorflow", node = node)
