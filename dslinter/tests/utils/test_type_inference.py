"""Class which tests the TypeInference utils class."""
import astroid

from dslinter.utils.type_inference import TypeInference


class TestTypeInference:
    """Class which tests the TypeInference utils class."""

    # def test_infer_types(self):
    #     """Test the infer_types method."""
    #     code = "a = 'b'; a.join([])"
    #     module_node = astroid.parse(code)
    #     node_type = astroid.Call
    #     result = TypeInference.infer_types(module_node, node_type, lambda x: x.func.expr.name)
    #
    #     assert result == {module_node.body[1].value: "builtins.str"}

    def test_add_reveal_type_calls(self):
        """Test the add_reveal_type_calls() method with a single expression."""
        code = "a = b.c(d)"
        nodes = [astroid.parse(code).body[0].value]

        result = TypeInference.add_reveal_type_calls(code, nodes, lambda node: node.func.expr.name)
        assert result == "a = b.c(d); reveal_type(b)"

    def test_add_reveal_type_calls_multiple(self):
        """Test the add_reveal_type_calls() method with multiple expressions."""
        code = "a = b.c(d)\nx = 5 \ne = f.g()"
        tree = astroid.parse(code)
        nodes = [tree.body[0].value, tree.body[2].value]

        result = TypeInference.add_reveal_type_calls(code, nodes, lambda node: node.func.expr.name)
        assert result == "a = b.c(d); reveal_type(b)\nx = 5 \ne = f.g(); reveal_type(f)"

    def test_run_mypy_success(self):
        """Test if mypy is ran successfully on some correct code."""
        result = TypeInference.run_mypy("a = 5")
        assert result == "Success: no issues found in 1 source file\n"

    def test_run_mypy_error(self):
        """Test if mypy returns an error when code is incorrect."""
        result = TypeInference.run_mypy("a: str = 5")
        assert result.splitlines()[1] == "Found 1 error in 1 file (checked 1 source file)"

    def test_parse_mypy_result(self):
        """Test if the parse_mypy_result method returns the correct type."""
        mypy_result = "<string>:1: note: Revealed type is 'builtins.int'"
        assert TypeInference.parse_mypy_result(mypy_result) == [(1, "'builtins.int'")]

    def test_parse_mypy_result_multiple(self):
        """Test if the parse_mypy_result method returns the correct types."""
        mypy_result = "<string>:1: note: Revealed type is 'builtins.int'"
        mypy_result += "\n<string>:2: note: Revealed type is 'builtins.str'"

        result = TypeInference.parse_mypy_result(mypy_result)
        assert result == [(1, "'builtins.int'"), (2, "'builtins.str'")]

    def test_combine_nodes_with_inferred_types(self):
        """Test if combine_nodes_with_inferred_types returns a correct dict on a single line."""
        nodes = [astroid.extract_node("a.b()")]
        types = [(1, "builtins.str")]
        result = TypeInference.combine_nodes_with_inferred_types(nodes, types)
        assert result == {nodes[0]: types[0][1]}

    def test_add_reveal_type_calls_block(self):
        """Test if the reveal_type() call is added to the body of a block statement."""
        code = "y = ''\nfor x in y.join([]):\n\tpass"
        nodes = [astroid.parse(code).body[1].iter]

        result = TypeInference.add_reveal_type_calls(code, nodes, lambda node: node.func.expr.name)
        assert result == "y = ''\nfor x in y.join([]):\n\tpass; reveal_type(y)"

    # def test_type_inference_in_for_loop_definition(self):
    #     """Test if type inference works for Calls inside for loop definitions."""
    #     code = "y = ''\nfor x in y.join([]):\n\tpass"
    #     module_node = astroid.parse(code)
    #     node_type = astroid.Call
    #     result = TypeInference.infer_types(module_node, node_type, lambda x: x.func.expr.name)
    #
    #     assert result == {module_node.body[1].iter: "builtins.str"}
