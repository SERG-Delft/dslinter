"""Utility class for working with the Abstract Syntax Tree (AST)."""
from typing import List, Union

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


class AssignUtil:
    """Utility class for working with (Ann)Assign nodes."""

    @staticmethod
    def is_target(name: str, assign: Union[astroid.Assign, astroid.AnnAssign]):
        """
        Evaluate whether 'name' is the target of an (Ann)Assign node.

        :param name: Name to check.
        :param assign: (Ann)Assign node to check.
        :return: True when this (Ann)Assign node has 'name' as a target.
        """
        if isinstance(assign, astroid.Assign):
            for target in assign.targets:
                if hasattr(target, "name") and target.name == name:
                    return True
        if isinstance(assign, astroid.AnnAssign):
            return hasattr(assign.target, "name") and assign.target.name == name

    @staticmethod
    def assignment_value(name_node: astroid.Name) -> Union[astroid.node_classes.NodeNG, None]:
        """
        Search for the value of the assignment to the name of a Name node.

        :param name_node: Node of which the assignment value is searched.
        :return: Value node which is assigned to the name from the Name node.
        """
        name = name_node.name
        value_in_body_of_parents = AssignUtil._assign_value_in_body_of_parents(name, name_node)
        if value_in_body_of_parents is not None:
            return value_in_body_of_parents
        return None

    @staticmethod
    def _assign_value_in_body_of_parents(
        name: str, node: astroid.node_classes.NodeNG
    ) -> Union[astroid.node_classes.NodeNG, None]:
        """
        Search for the value of the assignment to the name of a Name node in body of parents.

        :param name: Name to look for.
        :param node: Node of which is searched in the body of its parents.
        :return: The value node of the assignment or None when it is not found.
        """
        body_block = ASTUtil.search_body(node)
        for child in body_block:
            if (
                isinstance(child, astroid.Assign) or isinstance(child, astroid.AnnAssign)
            ) and AssignUtil.is_target(name, child):
                return child.value
        if hasattr(node, "parent"):
            return AssignUtil._assign_value_in_body_of_parents(name, node.parent)
        return None
