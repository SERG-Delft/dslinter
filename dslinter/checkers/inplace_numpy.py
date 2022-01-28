import astroid
from pylint. checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

class InPlaceNumpyChecker(BaseChecker):
    """ In-Place Checker for NumPy which checker In-Place APIs are correclty used. """
    __implement__ = IAstroidChecker

    name = "inplace_numpy"
    priority = -1
    msgs = {
        "W5601":(
            "The operation has not been assigned to another variable",
            "inplace-misused-numpy",
            ""
        )
    }
    options = ()

    LIST = [
        "clip",
    ]

    def visit_call(self, node:astroid.Call):
        try:
            if(self._result_is_lost(node)):
                self.add_message("inplace-misused-numpy", node = node)
        except:
            Exception.handler(self, node)

    def _result_is_lost(self, node: astroid.Call) -> bool:
        print("node.parent")
        print(node.parent)
        return (
            not self._is_inplace_operation(node) and
            isinstance(node.parent, astroid.Expr) #assign to a variable
        )


    @staticmethod
    def _is_inplace_operation(node: astroid.Call) -> bool:
        """
        Evaluate whether the call has an 'inplace==True' keyword argument.

        :param node: Node to check the arguments from.
        :return: True when the call has an 'inplace==True' keyword argument.
        """
        if node.keywords is None:
            return False

        for keyword in node.keywords:
            if keyword.arg == "inplace":
                return keyword.value.value
        return False
