"""Class which tests the DataLeakageChecker."""
import astroid
import pylint.testutils

import dslinter


class TestDataLeakageChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the DataLeakageChecker."""

    CHECKER_CLASS = dslinter.plugin.DataLeakageChecker

    def test_pipeline_violation_on_call(self):
        """Message should be added when learning function is called directly on a learning class."""
        call_node = astroid.extract_node("KMeans().fit()")
        with self.assertAddsMessages(
            pylint.testutils.Message(msg_id="sk-pipeline", node=call_node),
        ):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_on_name(self):
        """Message should be added when learning function is called directly on a learning class."""
        call_node = astroid.extract_node(
            """
            kmeans = KMeans()
            kmeans.fit() #@
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.Message(msg_id="sk-pipeline", node=call_node),
        ):
            self.checker.visit_call(call_node)
