"""Import checker which checks whether imports are bound to local names by the conventions."""
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class ImportChecker(BaseChecker):
    """Import checker which checks whether imports are bound to local names by the conventions."""

    __implements__ = IAstroidChecker

    name = "import"
    priority = -1
    msgs = {
        "C0001": (
            "Import of pandas not bound to 'pd'.",
            "import-pandas",
            "The pandas module should be imported as 'pd'.",
        ),
        "C0002": (
            "Import of numpy not bound to 'np'.",
            "import-numpy",
            "The numpy module should be imported as 'np'.",
        ),
        "C0003": (
            "Import of matplotlib.pyplot not bound to 'plt'.",
            "import-pyplot",
            "The matplotlib.pyplot module should be imported as 'plt'.",
        ),
        "C0004": (
            "Import from sklearn module has an alias.",
            "import-sklearn",
            "Imports from sklearn modules should not have an alias.",
        ),
    }
    options = ()

    def visit_import(self, node):
        """
        When an Import node is visited, check if it follows the conventions.

        :param Import node: Node which is visited.
        """
        for name, alias in node.names:
            if name == "pandas" and alias != "pd":
                self.add_message("import-pandas", node=node)
            elif name == "numpy" and alias != "np":
                self.add_message("import-numpy", node=node)
            elif name == "matplotlib.pyplot" and alias != "plt":
                self.add_message("import-pyplot", node=node)

    def visit_import_from(self, node):
        """
        When an ImportFrom node is visited, check if it follows the conventions.

        :param ImportFrom node: Node which is visited.
        """
        if node.modname[:7] == "sklearn":
            for _, alias in node.names:
                if alias is not None:
                    self.add_message("import-sklearn", node=node)
