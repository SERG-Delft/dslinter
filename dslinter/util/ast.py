"""Utility class for working with the Abstract Syntax Tree (AST)."""
from typing import List

import astroid


class AST:
    """Utility class for working with the Abstract Syntax Tree (AST)."""

    @staticmethod
    def search_nodes(node: astroid.node_classes.NodeNG, type_searched: type) -> List[astroid.node_classes.NodeNG]:
        """
        Search recursively for all nodes of a certain type.

        :param node: Node which is visited.
        :param type_searched: Type of node where is searched for.
        """
        found: List = []
        for child in node.get_children():
            found += AST.search_nodes(child, type_searched)

        if isinstance(node, type_searched):
            found.append(node)
        return found
