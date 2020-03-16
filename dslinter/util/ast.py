"""Utility class for working with the Abstract Syntax Tree (AST)."""
from typing import List

import astroid


class AST:
    """Utility class for working with the Abstract Syntax Tree (AST)."""

    @staticmethod
    def search_nodes(node: astroid.nodes, type_searched: type) -> List[astroid.nodes]:
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

    @staticmethod
    def get_source_code(node: astroid.nodes.Module) -> str:
        """
        Get the source code of a Module node.

        :param node: Node to get source code from.
        :return: Source code.
        """
        if node.file_bytes is not None:
            # First try if 'file_bytes' attribute is present with the source code.
            return node.file_bytes.decode("utf-8")
        elif node.file is not None:
            # Otherwise, read the entire file stated in the 'file' attribute.
            with open(node.file, "r") as file:
                return file.read()
        else:
            raise Exception("Could not retrieve the source code of the module.")
