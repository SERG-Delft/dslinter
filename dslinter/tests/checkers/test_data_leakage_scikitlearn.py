"""Class which tests the DataLeakageChecker."""
import astroid
import pylint.testutils
import dslinter


class TestDataLeakageScikitLearnChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the DataLeakageChecker."""

    CHECKER_CLASS = dslinter.plugin.DataLeakageScikitLearnChecker

    def test_pipeline_violation_on_call(self):
        """Message should be added when learning function is called directly on a learning class."""
        script = "KMeans().fit()"
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_learning_function_on_not_an_estimator(self):
        """No message should be added when a learning function is called on a non-estimator."""
        script = "A().fit()"
        call_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_pipeline_violation_outside_block(self):
        """Test whether sk-pipeline violation is found when assignment is done outside block."""
        script = """
            model = KMeans()
            if True:
                model.fit() #@
            """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_on_name(self):
        """Message should be added when learning function is called directly on a learning class."""
        script = """
            kmeans = KMeans()
            kmeans.fit() #@
            """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_on_name_twice(self):
        """Test calling an estimator by multiple assignments."""
        script = """
            kmeans = KMeans()
            kmeans2 = kmeans
            kmeans2.fit() #@
            """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_in_function(self):
        """Test whether sk-pipeline violation is found when assignment is a function argument."""
        script = """
            def f(model):
                model.fit() #@
            f(KMeans())
            """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_in_function_arg_assigned(self):
        """Test calling an estimator within a function, where the argument is assigned."""
        script = """
            def f(model):
                model.fit() #@
            kmeans_model = KMeans()
            f(kmeans_model)
            """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_in_named_function_argument(self):
        """Test calling an estimator with named function argument."""
        script = """
            def f(model):
                model.fit() #@
            f(model = KMeans())
            """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_in_second_function_argument(self):
        """Test calling an estimator with a second function argument."""
        script = """
            def f(x, model):
                model.fit() #@
            f(0, KMeans())
            """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)
