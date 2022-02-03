import astroid
import pylint.testutils
import dslinter


class TestImportChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the ImportChecker."""

    CHECKER_CLASS = dslinter.plugin.ImportChecker

    def test_finds_incorrect_pandas(self):
        """Test if message is added when pandas is imported incorrectly."""
        import_node = astroid.extract_node(
            """
            import pandas as pand #@
            """
        )

        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-pandas", node=import_node),):
            self.checker.visit_import(import_node)

    def test_ignore_correct_pandas(self):
        """Test if no message is added when pandas is imported correctly."""
        import_node = astroid.extract_node(
            """
            import pandas as pd #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_finds_incorrect_numpy(self):
        """Test if message is added when numpy is imported incorrectly."""
        import_node = astroid.extract_node(
            """
            import numpy #@
            """
        )

        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-numpy", node=import_node),):
            self.checker.visit_import(import_node)

    def test_ignore_correct_numpy(self):
        """Test if no message is added when numpy is imported correctly."""
        import_node = astroid.extract_node(
            """
            import numpy as np #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_finds_incorrect_pyplot(self):
        """Test if message is added when pyplot is imported incorrectly."""
        import_node = astroid.extract_node(
            """
            import matplotlib.pyplot as plot #@
            """
        )

        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-pyplot", node=import_node),):
            self.checker.visit_import(import_node)

    def test_ignore_correct_pyplot(self):
        """Test if no message is added when pyplot is imported correctly."""
        import_node = astroid.extract_node(
            """
            import matplotlib.pyplot as plt #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_finds_incorrect_sklearn(self):
        """Test if message is added when an import from the sklearn module is assigned an alias."""
        import_node = astroid.extract_node(
            """
            from sklearn.cluster import KMeans as km #@
            """
        )

        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-sklearn", node=import_node),):
            self.checker.visit_import_from(import_node)

    def test_ignore_correct_sklearn(self):
        """Test if no message is added when an sklearn module import is not assigned an alias."""
        import_node = astroid.extract_node(
            """
            from sklearn.cluster import KMeans #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_import_from(import_node)

    def test_finds_incorrect_tensorflow(self):
        """Test if message is added when tensorflow is imported incorrectly."""
        import_node = astroid.extract_node(
            """
            import tensorflow as tff
            """
        )

        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-tensorflow", node=import_node)):
            self.checker.visit_import(import_node)

    def test_ignore_correct_tensorflow(self):
        """Test if no message is added when tensorflow is imported correctly."""
        import_node = astroid.extract_node(
            """
            import tensorflow as tf
            """
        )

        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_finds_inccorrect_pytorch(self):
        """Test if message is added when pytorch is imported incorrectly."""
        import_node = astroid.extract_node(
            """
            import torch as tr
            """
        )

        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-pytorch", node=import_node)):
            self.checker.visit_import(import_node)

    def test_ignore_correct_pytorch(self):
        """Test if no message is added when pytorch is imported correclty"""
        import_node = astroid.extract_node(
            """
            import torch
            """
        )

        with self.assertNoMessages():
            self.checker.visit_import(import_node)


