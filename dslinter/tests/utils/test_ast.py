"""Class which tests the AST utils class."""
import astroid

from dslinter.utils.ast import ASTUtil


class TestAST:
    """Class which tests the AST utils class."""

    def test_search_nodes(self):
        """Test the search_nodes method."""
        module_tree = astroid.parse(
            """
            a = b.c(d)

            def e(f):
                return g.h(i)
            """
        )
        found = ASTUtil.search_nodes(module_tree, astroid.Call)
        # noinspection PyUnresolvedReferences
        assert len(found) == 2 and found[0].func.attrname == "c" and found[1].func.attrname == "h"

    def test_get_source_code(self):
        """Test the get_source_code method."""
        source_code = "a = b.c(d)"
        module_tree = astroid.parse(source_code)
        assert ASTUtil.get_source_code(module_tree) == source_code

    def test_search_body_parent_module(self):
        """Test whether the module is returned when searching for the parent of its child."""
        module_tree = astroid.parse(
            """
            f()
            """
        )
        node = module_tree.body[0]
        assert ASTUtil.search_body_parent(node) == module_tree

    def test_search_body(self):
        """Test whether the correct body is returned."""
        module_tree = astroid.parse(
            """
            f()
            """
        )
        node = module_tree.body[0]
        assert ASTUtil.search_body(node) == module_tree.body

    def test_search_body_parent_function(self):
        """Test whether the function is returned when searching for the parent of its child."""
        module_tree = astroid.parse(
            """
            def f():
                return 0
            """
        )
        node = module_tree.body[0].body[0]
        assert ASTUtil.search_body_parent(node) == module_tree.body[0]
