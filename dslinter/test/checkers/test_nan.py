"""Class which tests the NanChecker."""
import astroid
import pylint.testutils

import dslinter


class TestNanChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the NanChecker."""

    CHECKER_CLASS = dslinter.plugin.NanChecker

    def test_nan_left(self):
        """Test whether a message is added when np.nan is compared with something."""
        compare_node = astroid.extract_node(
            """
            np.nan == b #@
            """
        )

        with self.assertAddsMessages(pylint.testutils.Message(msg_id="nan-equality", node=compare_node),):
            self.checker.visit_compare(compare_node)

    def test_nan_right(self):
        """Test whether a message is added when something is compared with np.nan."""
        compare_node = astroid.extract_node(
            """
            a == np.nan #@
            """
        )

        with self.assertAddsMessages(pylint.testutils.Message(msg_id="nan-equality", node=compare_node),):
            self.checker.visit_compare(compare_node)

    def test_nan_both(self):
        """Test whether only one message is added when np.nan is compared with np.nan."""
        compare_node = astroid.extract_node(
            """
            np.nan == np.nan #@
            """
        )

        with self.assertAddsMessages(pylint.testutils.Message(msg_id="nan-equality", node=compare_node),):
            self.checker.visit_compare(compare_node)

    def test_nan_none(self):
        """Test whether no message is added when np.nan is not compared with."""
        compare_node = astroid.extract_node(
            """
            row == nan #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_compare(compare_node)
