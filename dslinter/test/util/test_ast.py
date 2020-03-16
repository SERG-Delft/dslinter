"""Class which tests the AST util class."""
import astroid

from dslinter.util.ast import AST


class TestAST:
    """Class which tests the AST util class."""

    def test_search_nodes(self):
        """Test the search_nodes method."""
        module_tree = astroid.parse(
            """
            a = b.c(d)

            def e(f):
                return g.h(i)
            """
        )
        found = AST.search_nodes(module_tree, astroid.nodes.Call)
        # noinspection PyUnresolvedReferences
        assert len(found) == 2 and found[0].func.attrname == "c" and found[1].func.attrname == "h"

    def test_get_source_code(self):
        """Test the get_source_code method."""
        source_code = "a = b.c(d)"
        module_tree = astroid.parse(source_code)
        assert AST.get_source_code(module_tree) == source_code
