"""Class which tests the DataLeakageChecker."""
import os
from pathlib import Path

import astroid
import pylint.testutils
import pytest

import dslinter
from dslinter.util.resources import Resources


class TestDataLeakageChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the DataLeakageChecker."""

    CHECKER_CLASS = dslinter.plugin.DataLeakageChecker

    @pytest.fixture(autouse=True)
    def set_pickle_path(self):
        """Set the path of the strict hyperparameters dict pickle for testing."""
        package_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent.parent.parent
        pickle_path = os.path.join(package_dir, "resources\\hyperparameters_dict.pickle")
        Resources.__HYPERPARAMETER_PATH = pickle_path

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
