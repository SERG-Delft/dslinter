import astroid as astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

class DatatypePandasChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = "datatype-pandas"
    priority = -1
    msgs = {
        "":(
            "datatype-pandas",
            "datatype-pandas",
            "datatype-pandas",
        )
    }
    options = ()

    def visit_call(self, call_node: astroid.Call):
        # pd and read_source and datatype
        if(
            hasattr(call_node.func, "attrname")
            and call_node.func.attrname == "read_csv"
            and hasattr(call_node.func, "expr")
            and hasattr(call_node.func.expr, "name")
            and call_node.func.expr.name in ["pandas", "pd"]
        ):
            kws = [kw.arg for kw in call_node.keywords if hasattr(kw, "arg")]
            if "dtype" not in kws:
                self.add_message(msgid="datatype-pandas", node=call_node)
