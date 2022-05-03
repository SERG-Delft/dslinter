"""Check whether the memory is freed in time."""
from typing import Dict
import astroid
from pylint.checkers import BaseChecker
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.type_inference import TypeInference


class MemoryReleaseTensorflowChecker(BaseChecker):
    """Check whether the memory is freed in time."""

    name = "memory-release-tensorflow"
    priority = -1
    msgs = {
        "W5506":{
            "The memory has not freed in time.",
            "memory-release-tensorflow",
            "The `clean_session()` can be used to free memory in the loop."
        }
    }
    options = ()

    MODELS = [
        "Sequential",
        "Model"
    ]

    # [variable name, inferred type of object the function is called on]
    _variable_types: Dict[str, str] = {}

    def visit_module(self, module: astroid.Module):
        """Visit module and infer which library the variables are from. """
        try:
            self._variable_types = TypeInference.infer_native_variable_most_recent_types(module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    def visit_for(self, node: astroid.For):
        """Evaluate whether memory is freed in a loop with model creation."""
        try:
            has_clear_session = False
            has_model_creation = False

            for nod in node.body:
                if (
                    hasattr(nod, "value")
                    and hasattr(nod.value, "func")
                    and hasattr(nod.value.func, "attrname")
                    and nod.value.func.attrname == "clear_session"
                ):
                    has_clear_session = True

                if (
                    hasattr(nod, "value")
                    and hasattr(nod.value, "func")
                    and hasattr(nod.value.func, "attrname")
                    and nod.value.func.attrname in self.MODELS
                ):
                    if(
                        hasattr(nod, "targets")
                        and len(nod.targets) > 0
                        and hasattr(nod.targets[0], "name")
                        and self._is_tf_variable(nod.targets[0].name)
                    ):
                        has_model_creation = True

            if(
                has_clear_session is False
                and has_model_creation is True
            ):
                # if there is no clear_session call in the loop
                # while there is a model creation, the rule is violated.
                self.add_message("memory-release-tensorflow", node=node)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, node)

    def _is_tf_variable(self, name) -> bool:
        """
        Check whether the variable with the name is a tensorflow variable
        :param name: name of the variable
        :return: True when meeting the requirements
        """
        return name in self._variable_types and self._variable_types[name] in ["tf", "tensorflow"]
