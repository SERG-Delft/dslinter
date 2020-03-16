"""Class which tests the TypeInference util class."""
import astroid

from dslinter.util.type_inference import TypeInference


class TestTypeInference:
    """Class which tests the TypeInference util class."""

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
