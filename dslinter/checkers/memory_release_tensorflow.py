"""Check whether the memory is freed in time."""
import astroid
from pylint.checkers import BaseChecker
from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.type_inference import TypeInference


class MemoryReleaseTensorflowChecker(BaseChecker):
    """Check whether the memory is freed in time."""

    name = "memory_release_tensorflow"
    priority = -1
    msgs = {
        #TODO: add the message code
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

    def visit_module(self, module: astroid.For):
        """Visit module and infer which library the variables are from. """
        try:
            self._variable_types = TypeInference.infer_variable_types(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_for(self, node: astroid.For):
        """Evaluate whether memory is freed in a loop with model creation."""
        has_clear_session = False
        has_model_creation = False

        for n in node.body:
            if (
                hasattr(n, "value")
                and hasattr(n.value, "func")
                and hasattr(n.value.func, "attrname")
                and n.value.func.attrname == "clear_session"
            ):
                has_clear_session = True

            if (
                hasattr(n, "value")
                and hasattr(n.value, "func")
                and hasattr(n.value.func, "attrname")
                and n.value.func.attrname in self.MODELS
            ):
                if(
                    hasattr(n, "targets")
                    and len(n.targets) > 0
                    and hasattr(n.targets[0], "name")
                    and self._is_tf_variable(n.targets[0].name)
                ):
                    has_model_creation = True

        if(
            has_clear_session == False
            and has_model_creation == True
        ):
            # if there is no clear_session call in the loop while there is a model creation, the rule is violated.
            self.add_message("memory-release-tensorflow", node = node)

    def _is_tf_variable(self, name) -> bool:
        """
        Check whether the variable with the name is a tensorflow variable
        :param name: name of the variable
        :return: True when meeting the requirements
        """
        return self._variable_types[name] in ["tf", "tensorflow"]
