"""Class which tests the HyperparameterChecker."""
import astroid
import pylint.testutils

import dslinter


class TestHyperParameterChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the HyperparameterChecker."""

    CHECKER_CLASS = dslinter.plugin.HyperparameterChecker

    def test_has_keyword_true(self):
        """Test if the function returns true when the keyword is present."""
        call_node = astroid.extract_node(
            """
            f(keyword0=0, keyword1=1, keyword2=2) #@
            """
        )
        keywords = call_node.keywords

        assert self.checker.has_keywords(keywords, ["keyword1", "keyword2"])

    def test_has_keyword_false(self):
        """Test if the function returns false when the keyword is not present."""
        call_node = astroid.extract_node(
            """
            f(keyword0=0) #@
            """
        )
        keywords = call_node.keywords

        assert not self.checker.has_keywords(keywords, ["keyword1"])

    def test_has_keyword_empty(self):
        """Test if the function returns false when there is no keyword present."""
        call_node = astroid.extract_node(
            """
            f() #@
            """
        )
        keywords = call_node.keywords

        assert not self.checker.has_keywords(keywords, ["keyword1"])

    def test_no_keywords(self):
        """Test if a message is added when no keywords are present."""
        call_node = astroid.extract_node(
            """
            KMeans() #@
            """
        )

        with self.assertAddsMessages(
            pylint.testutils.Message(msg_id="hyperparameters", node=call_node),
        ):
            self.checker.visit_call(call_node)

    def test_missing(self):
        """Test if a message is added when no hyperparameters are present."""
        call_node = astroid.extract_node(
            """
            KMeans(n_init=5) #@
            """
        )

        with self.assertAddsMessages(
            pylint.testutils.Message(msg_id="hyperparameters", node=call_node),
        ):
            self.checker.visit_call(call_node)

    def test_correct_keyword(self):
        """Test if no message is added when the hyperparameters are present as keyword."""
        call_node = astroid.extract_node(
            """
            KMeans(n_init=5, n_clusters=5) #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_correct_positional_argument(self):
        """Test if no message is added when the hyperparameters are present as positional args."""
        call_node = astroid.extract_node(
            """
            KMeans(5) #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_correct_optional_keyword(self):
        """Test if no message is added when the hyperparameters are present as keyword."""
        call_node_option_one = astroid.extract_node(
            """
            AgglomerativeClustering(n_init=5, n_clusters=5) #@
            """
        )
        call_node_option_two = astroid.extract_node(
            """
            AgglomerativeClustering(n_init=5, linkage="ward", distance_threshold=1) #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_call(call_node_option_one)
            self.checker.visit_call(call_node_option_two)
