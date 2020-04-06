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

    @staticmethod
    def retrieve_keyword_from_list(
        keywords: List[astroid.Keyword], arg_name: str
    ) -> Union[astroid.Keyword, None]:
        """
        Retrieve the keyword with a certain arg from a list of keywords.

        :param keywords: List of keywords.
        :param arg_name: Arg name to look for.
        :return: Keyword node with arg 'arg' or None if it not found.
        """
        for keyword in keywords:
            if keyword.arg == arg_name:
                return keyword
        return None


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
    def assignment_values(name_node: astroid.Name) -> List[astroid.node_classes.NodeNG]:
        """
        Search for the value of the assignment to the name of a Name node.

        :param name_node: Node of which the assignment value is searched.
        :return: Value nodes which are assigned to the name from the Name node.
        """
        name = name_node.name
        function_with_arg = AssignUtil._name_is_arg_from_function(name, name_node)
        if function_with_arg is not None:
            return AssignUtil._function_arg_values(function_with_arg, "", 0)  # TODO: Hardcoded

        return AssignUtil._assign_values_in_body_of_parents(name, name_node)

    @staticmethod
    def _assign_values_in_body_of_parents(
        name: str, node: astroid.node_classes.NodeNG
    ) -> List[astroid.node_classes.NodeNG]:
        """
        Search for the value of the assignment to the name of a Name node in body of parents.

        :param name: Name to look for.
        :param node: Node of which is searched in the body of its parents.
        :return: The value node of the assignment or None when it is not found.
        """
        values = []
        body_block = ASTUtil.search_body(node)
        for child in body_block:
            if (
                isinstance(child, astroid.Assign) or isinstance(child, astroid.AnnAssign)
            ) and AssignUtil.is_target(name, child):
                values.append(child.value)
        if hasattr(node, "parent") and node.parent is not None:
            return AssignUtil._assign_values_in_body_of_parents(name, node.parent)
        return values

    @staticmethod
    def _name_is_arg_from_function(
        name: str, node: astroid.node_classes.NodeNG
    ) -> Union[astroid.FunctionDef, None]:
        """
        Get the FunctionDef the name is part of (if it exists).

        :param name: Name to look for.
        :param node: Node to look for FunctionDef nodes in.
        :return: FunctionDef with arg 'name' or None when it is not found.
        """
        if isinstance(node, astroid.FunctionDef):
            for arg in node.args.args:
                if hasattr(arg, "name") and arg.name == name:
                    return node
            return None
        if hasattr(node, "parent"):
            return AssignUtil._name_is_arg_from_function(name, node.parent)
        return None

    # noinspection PyUnresolvedReferences
    @staticmethod
    def _function_arg_values(node: astroid.FunctionDef, arg_name: str, arg_position: int):
        """
        Search the values a certain argument of a function gets assigned.

        Calls to the function will be searched for in the parent of the FunctionDef node.

        :param node: FunctionDef node which contains the argument.
        :param arg_name: Name of the argument.
        :param arg_position: Position of the argument.
        :return: All values this argument gets assigned.
        """
        values = []
        for call_node in ASTUtil.search_nodes(node.parent, astroid.Call):
            if hasattr(call_node.func, "name") and call_node.func.name == node.name:
                if call_node.args is not None and len(call_node.args) >= arg_position:
                    values.append(call_node.args[arg_position])
                if call_node.keywords is not None:
                    keyword = ASTUtil.retrieve_keyword_from_list(call_node.keywords, arg_name)
                    if keyword is not None:
                        values.append(keyword.value)
        return values
