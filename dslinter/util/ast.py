"""Utility class for working with the Abstract Syntax Tree (AST)."""
from typing import List

import astroid


class ASTUtil:
    """Utility class for working with the Abstract Syntax Tree (AST)."""

    @staticmethod
    def search_nodes(
        node: astroid.node_classes.NodeNG, type_searched: type
    ) -> List[astroid.node_classes.NodeNG]:
        """
        Search recursively for all nodes of a certain type.

        :param node: Node which is visited.
        :param type_searched: Type of node where is searched for.
        """
        found: List = []
        for child in node.get_children():
            found += ASTUtil.search_nodes(child, type_searched)

        if isinstance(node, type_searched):
            found.append(node)
        return found

    @staticmethod
    def get_source_code(node: astroid.Module) -> str:
        """
        Get the source code of a Module node.

        :param node: Node to get source code from.
        :return: Source code.
        """
        if node.file_bytes is not None:
            # First try if 'file_bytes' attribute is present with the source code.
            return node.file_bytes.decode("utf-8")
        if node.file is not None:
            # Otherwise, read the entire file stated in the 'file' attribute.
            with open(node.file, "r") as file:
                return file.read()
        raise Exception("Could not retrieve the source code of the module.")

    @staticmethod
    def search_body_parent(node: astroid.node_classes.NodeNG) -> astroid.node_classes.NodeNG:
        """
        Search the parent of the body block a node is part of.

        :param node: Node to search the parent of the body block of.
        :return: Parent node of the body block.
        """
        if hasattr(node, "body"):
            return node
        return ASTUtil.search_body_parent(node.parent)

    @staticmethod
    def search_body(node: astroid.node_classes.NodeNG) -> List[astroid.node_classes.NodeNG]:
        """
        Search the body block a node is part of.

        :param node: Node to search the body block of.
        :return: Body block the node is part of.
        """
        # noinspection PyUnresolvedReferences
        return ASTUtil.search_body_parent(node).body
