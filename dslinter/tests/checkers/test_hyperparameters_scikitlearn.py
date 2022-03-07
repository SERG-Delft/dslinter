"""Class which tests the HyperparameterScikitLearnChecker."""
import astroid
import pylint.testutils
from pylint.testutils import set_config
import dslinter


class TestHyperparameterScikitLearnChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the HyperparameterScikitLearnChecker."""

    CHECKER_CLASS = dslinter.plugin.HyperparameterScikitLearnChecker

    def test_has_keyword_true(self):
        """Test whether the function returns true when the keyword is present."""
        call_node = astroid.extract_node(
            """
            f(keyword0=0, keyword1=1, keyword2=2) #@
            """
        )
        keywords = call_node.keywords

        assert self.checker.has_keywords(keywords, ["keyword1", "keyword2"])

    def test_has_keyword_false(self):
        """Test whether the function returns false when the keyword is not present."""
        call_node = astroid.extract_node(
            """
            f(keyword0=0) #@
            """
        )
        keywords = call_node.keywords

        assert not self.checker.has_keywords(keywords, ["keyword1"])

    def test_has_keyword_empty(self):
        """Test whether the function returns false when there is no keyword present."""
        call_node = astroid.extract_node(
            """
            f() #@
            """
        )
        keywords = call_node.keywords

        assert not self.checker.has_keywords(keywords, ["keyword1"])

    @set_config(strict_hyperparameters_scikitlearn=True)
    def test_strict_keywords_correct(self):
        """No violation when all keywords are set in strict mode."""
        call_node = astroid.extract_node(
            """
            KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
            precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=None, \
            algorithm='auto') #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=True)
    def test_strict_arguments_correct(self):
        """No violation when all arguments are set in strict mode."""
        call_node = astroid.extract_node(
            """
            KMeans(8, 'k-means++', 10, 300, 0.0001, 'auto', 0, None, True, None, 'auto') #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=True)
    def test_strict_empty(self):
        """Violation when no keywords or arguments are set in strict mode."""
        call_node = astroid.extract_node(
            """
            KMeans() #@
            """
        )
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameters-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=True)
    def test_strict_keywords_missing(self):
        """Violation when not all keywords are set in strict mode."""
        call_node = astroid.extract_node(
            """
            KMeans(n_clusters=8, init='k-means++') #@
            """
        )
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameters-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=True)
    def test_strict_arguments_missing(self):
        """Violation when not all arguments are set in strict mode."""
        call_node = astroid.extract_node(
            """
            KMeans(8, 'k-means++') #@
            """
        )
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameters-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=False)
    def test_non_strict_keywords_all(self):
        """No violation when all keywords are set in non-strict mode, function from main list."""
        call_node = astroid.extract_node(
            """
            NearestNeighbors(n_neighbors=5, radius=1.0, algorithm='auto', leaf_size=30, \
            metric='minkowski', p=2, metric_params=None, n_jobs=None) #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=False)
    def test_non_strict_keywords_required(self):
        """No violation when only required keywords are set in non-strict mode, main function."""
        call_node = astroid.extract_node(
            """
            NearestNeighbors(n_neighbors=5) #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=False)
    def test_non_strict_arguments_all(self):
        """No violation when all arguments are set in non-strict mode, function from main list."""
        call_node = astroid.extract_node(
            """
            NearestNeighbors(5, 1.0, 'auto', 30, 'minkowski', 2, None, None) #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=False)
    def test_non_strict_empty(self):
        """Violation when no keywords or arguments are set in non-strict mode, main function."""
        call_node = astroid.extract_node(
            """
            NearestNeighbors() #@
            """
        )
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameters-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=False)
    def test_non_strict_keywords_missing(self):
        """Violation when not all required keywords are set in non-strict mode, main function."""
        call_node = astroid.extract_node(
            """
            ElasticNet(alpha=1.0) #@
            """
        )
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameters-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=False)
    def test_non_strict_arguments_missing(self):
        """Violation when not all required arguments are set in non-strict mode, main function."""
        call_node = astroid.extract_node(
            """
            ElasticNet(1.0) #@
            """
        )
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="hyperparameters-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=False)
    def test_non_strict_non_main_keywords_all(self):
        """No violation when all keywords are set in non-strict mode, no main function."""
        call_node = astroid.extract_node(
            """
            KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
            precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=None, \
            algorithm='auto') #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameter_scikitlearn=False)
    def test_non_strict_non_main_keywords_one(self):
        """No violation when one keyword is set in non-strict mode, no main function."""
        call_node = astroid.extract_node(
            """
            KMeans(n_neighbors=5) #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=False)
    def test_non_strict_non_main_arguments_all(self):
        """No violation when all arguments are set in non-strict mode, no main function."""
        call_node = astroid.extract_node(
            """
            KMeans(8, 'k-means++', 10, 300, 0.0001, 'auto', 0, None, True, None, 'auto') #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    @set_config(strict_hyperparameters_scikitlearn=False)
    def test_non_strict_non_main_arguments_required(self):
        """No violation when one arguments is set in non-strict mode,no main function."""
        call_node = astroid.extract_node(
            """
            KMeans(5) #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    # @set_config(strict_hyperparameters=False)
    # def test_non_strict_non_main_empty(self):
    #     """Violation when no keywords or arguments are set in non-strict mode, no main function."""
    #     call_node = astroid.extract_node(
    #         """
    #         KMeans() #@
    #         """
    #     )
    #     with self.assertAddsMessages(pylint.testutils.Message(msg_id="hyperparameters", node=call_node),):
    #         self.checker.visit_call(call_node)
