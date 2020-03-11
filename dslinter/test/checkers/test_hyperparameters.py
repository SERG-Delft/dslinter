"""Class which tests the HyperparameterChecker."""
import os
from pathlib import Path

import astroid
import pylint.testutils
from pylint.testutils import set_config

import dslinter


class TestHyperParameterChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the HyperparameterChecker."""

    CHECKER_CLASS = dslinter.plugin.HyperparameterChecker

    @staticmethod
    def get_strict_pickle() -> str:
        """
        Get the path to the strict hyperparameters dict pickle.

        :return: path of pickle.
        """
        package_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent.parent.parent
        return os.path.join(package_dir, "resources\\hyperparameters_dict.pickle")

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

    @set_config(strict_hyperparameters=True)
    def test_strict_incorrect(self):
        """Test if a message is added when not strictly all hyperparameters are added."""
        call_node = astroid.extract_node(
            """
            KMeans(n_clusters=5) #@
            """
        )

        with self.assertAddsMessages(
            pylint.testutils.Message(msg_id="hyperparameters", node=call_node),
        ):
            self.checker.strict_pickle = self.get_strict_pickle()
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters=True)
    def test_strict_correct(self):
        """Test if no message is added when strictly all hyperparameters are added."""
        call_node = astroid.extract_node(
            """
            KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
            precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=None, \
            algorithm='auto') #@
            """
        )

        with self.assertNoMessages():
            self.checker.strict_pickle = self.get_strict_pickle()
            self.checker.visit_call(call_node)
