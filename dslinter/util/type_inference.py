"""Utility class for type inference."""
import os
from typing import Callable, List

import mypy.api


class TypeInference:
    """Utility class for type inference."""

    @staticmethod
    def add_reveal_type_calls(code: str, nodes: List, expr: Callable) -> str:
        """
        Add reveal_type() calls to source code, so mypy will infer the types.

        :param code: Code to add calls to.
        :param nodes: Nodes of which the type will be inferred on a certain attribute.
        :param expr: Expression to extract the attribute from the node where the type will be
            inferred on. E.g., lambda node: node.func.expr.name
        :return: Code including the calls.
        """
        lines = code.splitlines()
        for node in nodes:
            lines[node.tolineno - 1] += "; reveal_type({})".format(expr(node))

        return "\n".join(lines)

    @staticmethod
    def run_mypy(code: str) -> str:
        """
        Run mypy on some code.

        :param code: Code to run mypy on.
        :return: Normal report written to sys.stdout by mypy.
        """
        file = open("_tmp_dslinter.py", "w")
        file.write(code)
        file.close()
        result = mypy.api.run(["_tmp_dslinter.py"])
        os.remove("_tmp_dslinter.py")

        if result[1] != "":
            raise Exception("Running mypy resulted in an error: " + result[1])
        return result[0]
