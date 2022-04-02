"""Utility module for type inference."""
import os
from typing import Callable, Dict, List, Tuple

import astroid
import mypy.api

from dslinter.utils.ast import ASTUtil
import uuid


class TypeInference:
    """Utility class for type inference."""

    #pylint: disable = line-too-long
    @staticmethod
    def infer_types(module: astroid.Module, node_type: type, expr: Callable) -> Dict[astroid.node_classes.NodeNG, str]:
        """
        Infer the types of an attribute of all nodes of the same type in a module.

        :param module: The module node where all nodes are located in.
        :param node_type: Type of node of which the type will be inferred on a certain attribute.
        :param expr: Expression to extract the attribute from the node where the type will be
            inferred on. E.g., lambda node: node.func.expr.name
        :return: All nodes in the module of type 'node_type' with the inferred type of the attribute
            accessible with the expression 'expr'.
        """
        nodes = ASTUtil.search_nodes(module, node_type)
        source_code = ASTUtil.get_source_code(module)
        mypy_code = TypeInference.add_reveal_type_calls(source_code, nodes, expr)
        mypy_result = TypeInference.run_mypy(mypy_code)
        try:
            mypy_types = TypeInference.parse_mypy_result(mypy_result)
        except SyntaxError as ex:
            mypy_code_split = mypy_code.splitlines()
            faulty_code = mypy_code_split[int(ex.lineno) - 1]
            if "; reveal_type(" in faulty_code:
                original_code = faulty_code.split("; reveal_type(")[0]
                mypy_code_split[int(ex.lineno) - 1] = original_code
                mypy_types = TypeInference.parse_mypy_result("\n".join(mypy_code_split))
                return TypeInference.combine_nodes_with_inferred_types(nodes, mypy_types)
            else:
                print(
                    "Skipping type checking of module {}: {}. Line {}: {}".format(
                        module.name, ex.msg, ex.lineno, faulty_code
                    )
                )
                return {}
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
                line_no = TypeInference.line_to_add_call(node) - 1
                lines[line_no] += "; reveal_type({})".format(expr(node))
                if lines[line_no].strip()[0] == ";":
                    # If the call is added to a new line, remove the semicolon.
                    lines[line_no] = lines[line_no].strip()[1:]
            except AttributeError:
                pass  # The attribute from the expression is not found. Continue.

        return "\n".join(lines)

    @staticmethod
    def line_to_add_call(node: astroid.node_classes.NodeNG):
        """
        Determine the line number where the reveal_type() call can be added to.

        In case the node starts a block, the call cannot be added to the end of the line, as it
        will break the syntax. An example how this would break the syntax:
        '''
        for x in y:;reveal_type(x)
            print(x)
        '''
        The call will be added to the end of the first non block node in the body of the node:
        '''
        for x in y:
            for z in x:
                print(z);reveal_type(x)
        '''

        :param node: The node where a call is added to in the source code.
        :return: Line number where the reveal_type() call can be added.
        """
        if hasattr(node.parent, "blockstart_tolineno") and node not in node.parent.body:
            return TypeInference.line_to_add_call(node.parent.body[0])
        return node.tolineno

    @staticmethod
    def run_mypy(code: str) -> str:
        """
        Run mypy on some code.

        :param code: Code to run mypy on.
        :return: Normal report written to sys.stdout by mypy.
        """
        id1 = str(uuid.uuid1())
        _tmp_dslinter_file = "_tmp_dslinter"+id1+".py"
        file = open(_tmp_dslinter_file, "w", encoding="utf-8")
        file.write(code)
        file.close()
        result = mypy.api.run([_tmp_dslinter_file])
        os.remove(_tmp_dslinter_file)

        if result[1] != '':
            raise Exception("Running mypy resulted in an error: " + result[1])
        return result[0]

    @staticmethod
    def parse_mypy_result(mypy_result: str) -> List[Tuple[int, str]]:
        """
        Parse the result of mypy to obtain all revealed types.

        :param mypy_result: mypy result to parse.
        :return: List of (line number, inferred type) Tuples.
        """
        if "error: invalid syntax" in mypy_result:
            lineno = mypy_result.split(":")[1]
            raise SyntaxError("Mypy cannot run on invalid syntax.", ("", lineno, 0, ""))

        types = []
        revealed_type_indicator = ': note: Revealed type is '
        for line in mypy_result.splitlines():
            if revealed_type_indicator in line:
                line_number = int(line.split(revealed_type_indicator)[0].split(":")[-1])
                inferred_type = line.split(revealed_type_indicator)[1]
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
        unseen_types = types.copy()
        nodes_with_types = {}
        for node in nodes:
            for line, type_inferred in unseen_types:
                if TypeInference.line_to_add_call(node) == line:
                    nodes_with_types[node] = type_inferred
                    # Remove the tuple so multiple calls on the same line get the correct type.
                    unseen_types.remove((line, type_inferred))
        return nodes_with_types

    @staticmethod
    def infer_variable_most_recent_full_types(module: astroid.Module) -> Dict[str, str]:
        """
        When there is no stub available for a library (e.g., missing tensorflow-stubs),
        use this method instead of infer_types. Infer variable type in Assign nodes.
        :param module: code module
        :return: Dict witn variable names and their inferred type
        """
        variables_with_full_types = {}
        nodes = ASTUtil.search_nodes(module, astroid.Assign)
        for node in nodes:
            if hasattr(node, "targets"):
                for var in node.targets:
                    if hasattr(var, "name"):
                        variable_name = var.name
                        if isinstance(node.value, astroid.nodes.Const):
                            variables_with_full_types[variable_name] = 'const'
                        elif hasattr(node.value, "func"):
                            call = node.value.func
                            full_type = ""
                            if hasattr(call, "attrname"):
                                full_type = "." + call.attrname + full_type
                            while hasattr(call, "expr"):
                                call = call.expr
                                if hasattr(call, "attrname"):
                                    full_type = "." + call.attrname + full_type
                            if hasattr(call, "name"):
                                full_type = call.name + full_type
                            variables_with_full_types[variable_name] = full_type

        return variables_with_full_types

    @staticmethod
    def infer_variable_full_types(module: astroid.Module) -> Dict[str, str]:
        """
        When there is no stub available for a library (e.g., missing tensorflow-stubs),
        use this method instead of infer_types. Infer variable type in Assign nodes.
        :param module: code module
        :return: Dict witn variable names and their inferred type
        """
        variables_with_full_types = {}
        nodes = ASTUtil.search_nodes(module, astroid.Assign)
        for node in nodes:
            if hasattr(node, "targets"):
                for var in node.targets:
                    if hasattr(var, "name"):
                        variable_name = var.name
                        if isinstance(node.value, astroid.nodes.Const):
                            variables_with_full_types[variable_name] = ['const']
                        elif hasattr(node.value, "func"):
                            call = node.value.func
                            full_type = ""
                            if hasattr(call, "attrname"):
                                full_type = "." + call.attrname + full_type
                            while hasattr(call, "expr"):
                                call = call.expr
                                if hasattr(call, "attrname"):
                                    full_type = "." + call.attrname + full_type
                            if hasattr(call, "name"):
                                full_type = call.name + full_type
                            if variable_name not in variables_with_full_types:
                                variables_with_full_types[variable_name] = [full_type]
                            else:
                                variables_with_full_types[variable_name].append(full_type)

        return variables_with_full_types

    @staticmethod
    def infer_native_variable_most_recent_types(module: astroid.Module) -> Dict[str, str]:
        """
        When there is no stub available for a library (e.g., missing tensorflow-stubs),
        use this method instead of infer_types. Infer variable type in Assign nodes.
        :param module: code module
        :return: Dict witn variable names and their inferred type
        """
        variables_with_types = {}
        variables_with_full_types = TypeInference.infer_variable_most_recent_full_types(module)
        for k, v in variables_with_full_types.items():
            variables_with_types[k] = v.split(".")[0]
        return variables_with_types

    @staticmethod
    def infer_library_variable_most_recent_types(module: astroid.Module) -> Dict[str, str]:
        """
        When there is no stub available for a library (e.g., missing tensorflow-stubs),
        use this method instead of infer_types. Infer variable type in Assign nodes.
        :param module: code module
        :return: Dict witn variable names and their inferred type
        """
        variables_with_types = {}
        variables_with_full_types = TypeInference.infer_variable_most_recent_full_types(module)
        for k, v in variables_with_full_types.items():
            strings = v.split(".")
            if len(strings) >= 2:
                variables_with_types[k] = strings[0] + "." + strings[1]
        return variables_with_types

    @staticmethod
    def infer_library_variable_first_types(module: astroid.Module) -> Dict[str, str]:
        """
        When there is no stub available for a library (e.g., missing tensorflow-stubs),
        use this method instead of infer_types. Infer variable type in Assign nodes.
        :param module: code module
        :return: Dict witn variable names and their inferred type
        """
        variables_with_types = {}
        variables_with_full_types = TypeInference.infer_variable_full_types(module)
        for k, v in variables_with_full_types.items():
            strings = v[0].split(".")
            if len(strings) >= 2:
                variables_with_types[k] = strings[0] + "." + strings[1]
        return variables_with_types
