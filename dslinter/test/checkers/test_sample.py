"""Class which tests the UniqueReturnChecker."""
import astroid
import pylint.testutils

import dslinter


class TestUniqueReturnChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the UniqueReturnChecker."""

    CHECKER_CLASS = dslinter.plugin.SampleChecker

    def test_finds_non_unique_ints(self):
        """Test if message is added when there are non-unique returns."""
        func_node, return_node_a, return_node_b = astroid.extract_node(
            """
        def test(): #@
            if True:
                return 5 #@
            return 5 #@
        """
        )

        self.checker.visit_functiondef(func_node)
        self.checker.visit_return(return_node_a)
        with self.assertAddsMessages(
            pylint.testutils.Message(msg_id="non-unique-returns", node=return_node_b,),
        ):
            self.checker.visit_return(return_node_b)

    def test_ignores_unique_ints(self):
        """Test if no message is added when there are only unique returns."""
        func_node, return_node_a, return_node_b = astroid.extract_node(
            """
        def test(): #@
            if True:
                return 1 #@
            return 5 #@
        """
        )

        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)
            self.checker.visit_return(return_node_a)
            self.checker.visit_return(return_node_b)
