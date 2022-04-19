"""Class which tests the NanChecker."""
import astroid
import pylint.testutils
import dslinter


class TestNanNumpyChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the NanChecker."""

    CHECKER_CLASS = dslinter.plugin.NanNumpyChecker

    def test_nan_left(self):
        """Test whether a message is added when np.nan is compared with something."""
        script = """
        np.nan == b #@
        """
        compare_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="nan-numpy", node=compare_node),):
            self.checker.visit_compare(compare_node)

    def test_nan_right(self):
        """Test whether a message is added when something is compared with np.nan."""
        script = """
        a == np.nan #@
        """
        compare_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="nan-numpy", node=compare_node),):
            self.checker.visit_compare(compare_node)

    def test_nan_both(self):
        """Test whether only one message is added when np.nan is compared with np.nan."""
        script = """
        np.nan == np.nan #@
        """
        compare_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="nan-numpy", node=compare_node),):
            self.checker.visit_compare(compare_node)

    def test_nan_none(self):
        """Test whether no message is added when np.nan is not compared with."""
        script = """
        row == nan #@
        """
        compare_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_compare(compare_node)
