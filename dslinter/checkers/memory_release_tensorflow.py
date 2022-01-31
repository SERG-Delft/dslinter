import astroid
from pylint.checkers import BaseChecker

class MemoryReleaseTensorflowChecker(BaseChecker):

    name = "memory_release_tensorflow"
    priority = -1
    msgs = {
        "":{
            "",
            "memory",
            ""
        }
    }
    options = ()

    MODELS = [
        "Sequential"
    ]

    def visit_for(self, node: astroid.Call):

        hasClearSession = False

        for item in node.body:
            # if there is no clear_session call before calling a model, the rule is violated.
            if( item.value.func.attrname == "clear_session"):
                hasClearSession = True
            if( item.value.func.attrname in self.MODELS and hasClearSession == False):
                self.add_message("memory", node = node)
