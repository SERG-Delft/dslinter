"""Class which tests the AST util class."""
import astroid

from dslinter.util.ast import AST


class TestAST:
    """Class which tests the AST util class."""

    def test_search_nodes(self):
        module_tree = astroid.parse(
            """
            df = pd.DataFrame(data)

            def df_function(dataf: pd.DataFrame):
                return dataf.append(df)
            """
        )
        found = AST.search_nodes(module_tree, astroid.nodes.Call)
        # noinspection PyUnresolvedReferences
        assert len(found) == 2 and found[0].func.attrname == "DataFrame" and found[1].func.attrname == "append"
