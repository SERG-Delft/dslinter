"""DataFrame checker which checks correct handling of DataFrames."""
import os
from typing import Dict

import astroid
import mypy.api
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class DataFrameChecker(BaseChecker):
    """DataFrame checker which checks correct handling of DataFrames."""

    __implements__ = IAstroidChecker

    name = "dataframe"
    priority = -1
    msgs = {
        "W5501": (
            "Result of operation on a DataFrame is not saved.",
            "dataframe-lost",
            "An operation on a DataFrame returns a new DataFrame, which should be assigned to \
            a variable",
        ),
    }
    options = ()

    _call_nodes: Dict[astroid.nodes.Call, str] = {}

    def visit_module(self, node: astroid.nodes.Module):
        """
        When an Module node is visited, scan for Call nodes and get the type of the func expr.

        :param node: Node which is visited.
        """
        self._search_call_nodes(node)
        code = self._get_file_code(node)
        mypy_code = self._add_reveal_type_calls(code)
        mypy_result = self._run_mypy(mypy_code)
        mypy_types = self._parse_types(mypy_result)
        self._add_types_to_calls(mypy_types)

    def _search_call_nodes(self, node: astroid.nodes.Module):
        """
        Search recursively for Call nodes and add them to the instance variable _call_nodes.

        :param node: Node which is visited.
        """
        for child in node.get_children():
            self._search_call_nodes(child)
        if isinstance(node, astroid.nodes.Call) and isinstance(node.func.expr, astroid.nodes.Name):
            # Only add "single" call nodes for now, such as a.f() and not a.f().g().
            print("Found a call on line {}".format(node.lineno))
            self._call_nodes[node] = "Any"

    @staticmethod
    def _get_file_code(node: astroid.nodes.Module) -> str:
        """
        Get the source code of a Module node.

        :param node: Node to get source code from.
        :return: Source code.
        """
        if node.file_bytes is not None:
            return node.file_bytes.decode("utf-8")
        elif node.file is not None:
            with open(node.file, "r") as file:
                return file.read()
        else:
            print("ERROR: Could not retrieve the source code of the module.")

    def _add_reveal_type_calls(self, code: str) -> str:
        """
        Add reveal_type() calls to the source code, so mypy will infer the types.

        :param code: Code to add calls to.
        :return: Code including the calls.
        """
        lines = code.splitlines()
        for node in self._call_nodes:
            lines[node.tolineno - 1] += "; reveal_type({})".format(node.func.expr.name)

        return "\n".join(lines)

    @staticmethod
    def _run_mypy(code: str) -> str:
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
        return result[0]

    @staticmethod
    def _parse_types(mypy_result: str):
        """
        Parse the result of mypy to obtain all revealed types.

        :param mypy_result: mypy result to parse.
        """
        types = {}
        indicator = ": note: Revealed type is '"
        for line in mypy_result.splitlines():
            if indicator in line:
                line_number = line.split(indicator)[0].split(":")[-1]
                inferred_type = line.split(indicator)[1][:-1]
                types[int(line_number)] = inferred_type
        return types

    def _add_types_to_calls(self, mypy_types):
        """
        Add the inferred types to the instance variable _call_nodes.

        :param mypy_types:
        :return:
        """
        for node in self._call_nodes:
            self._call_nodes[node] = mypy_types[node.tolineno]
