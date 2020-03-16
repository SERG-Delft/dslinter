"""Utility class for type inference."""
from typing import List, Callable

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
