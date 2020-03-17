"""Utility class for type inference."""
import os
from typing import Callable, Dict, List, Tuple

import astroid
import mypy.api

from dslinter.util.ast import AST


class TypeInference:
    """Utility class for type inference."""

    @staticmethod
    def infer_types(
        module: astroid.nodes.Module, node_type: type, expr: Callable
    ) -> Dict[astroid.node_classes.NodeNG, str]:
        """
        Infer the types of an attribute of all nodes of the same type in a module.

        :param module: The module node where all nodes are located in.
        :param node_type: Type of node of which the type will be inferred on a certain attribute.
        :param expr: Expression to extract the attribute from the node where the type will be
            inferred on. E.g., lambda node: node.func.expr.name
        :return: All nodes in the module of type 'node_type' with the inferred type of the attribute
            accessible with the expression 'expr'.
        """
        nodes = AST.search_nodes(module, node_type)
        source_code = AST.get_source_code(module)
        mypy_code = TypeInference.add_reveal_type_calls(source_code, nodes, expr)
        mypy_result = TypeInference.run_mypy(mypy_code)
        mypy_types = TypeInference.parse_mypy_result(mypy_result)
        return TypeInference.combine_nodes_with_inferred_types(nodes, mypy_types)

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
            try:
                lines[node.tolineno - 1] += "; reveal_type({})".format(expr(node))
            except AttributeError:
                pass  # The attribute from the expression is not found. Continue.

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

    @staticmethod
    def parse_mypy_result(mypy_result: str) -> List[Tuple[int, str]]:
        """
        Parse the result of mypy to obtain all revealed types.

        :param mypy_result: mypy result to parse.
        :return: List of (line number, inferred type) Tuples.
        """
        types = []
        indicator = ": note: Revealed type is '"
        for line in mypy_result.splitlines():
            if indicator in line:
                line_number = int(line.split(indicator)[0].split(":")[-1])
                inferred_type = line.split(indicator)[1][:-1]
                types.append((line_number, inferred_type))
        return types

    @staticmethod
    def combine_nodes_with_inferred_types(
        nodes: List[astroid.node_classes.NodeNG], types: List[Tuple[int, str]]
    ) -> Dict[astroid.node_classes.NodeNG, str]:
        """
        Create a Dict with nodes and their inferred types.

        :param nodes: Nodes where a type is inferred from.
        :param types: List of (line number, inferred type) Tuples.
        :return: Dict with nodes and their inferred types.
        """
        nodes_with_types = {}
        for node in nodes:
            for line, type_inferred in types:
                if node.tolineno == line:
                    nodes_with_types[node] = type_inferred
                    types.remove((line, type_inferred))  # Remove for any next call on same line.
        return nodes_with_types
