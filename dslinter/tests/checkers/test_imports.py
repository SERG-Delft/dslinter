"""Class which tests the ImportChecker."""
import astroid
import pylint.testutils
import dslinter


class TestImportChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the ImportChecker."""

    CHECKER_CLASS = dslinter.plugin.ImportChecker

    def test_finds_incorrect_pandas(self):
        """Test if message is added when pandas is imported incorrectly."""
        script = """
            import pandas as pand #@
            """
        import_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-pandas", node=import_node),):
            self.checker.visit_import(import_node)

    def test_ignore_correct_pandas(self):
        """Test if no message is added when pandas is imported correctly."""
        script = """
            import pandas as pd #@
            """
        import_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_finds_incorrect_numpy(self):
        """Test if message is added when numpy is imported incorrectly."""
        script = """
            import numpy #@
            """
        import_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-numpy", node=import_node),):
            self.checker.visit_import(import_node)

    def test_ignore_correct_numpy(self):
        """Test if no message is added when numpy is imported correctly."""
        script = """
            import numpy as np #@
            """
        import_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_finds_incorrect_pyplot(self):
        """Test if message is added when pyplot is imported incorrectly."""
        script = """
            import matplotlib.pyplot as plot #@
            """
        import_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-pyplot", node=import_node),):
            self.checker.visit_import(import_node)

    def test_ignore_correct_pyplot(self):
        """Test if no message is added when pyplot is imported correctly."""
        script = """
            import matplotlib.pyplot as plt #@
            """
        import_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_finds_incorrect_sklearn(self):
        """Test if message is added when an import from the sklearn module is assigned an alias."""
        script = """
            from sklearn.cluster import KMeans as km #@
            """
        import_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-sklearn", node=import_node),):
            self.checker.visit_importfrom(import_node)

    def test_ignore_correct_sklearn(self):
        """Test if no message is added when an sklearn module import is not assigned an alias."""
        script = """
            from sklearn.cluster import KMeans #@
            """
        import_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_importfrom(import_node)

    def test_finds_incorrect_tensorflow(self):
        """Test if message is added when tensorflow is imported incorrectly."""
        script = """
            import tensorflow as tff
            """
        import_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-tensorflow", node=import_node)):
            self.checker.visit_import(import_node)

    def test_ignore_correct_tensorflow(self):
        """Test if no message is added when tensorflow is imported correctly."""
        script = """
            import tensorflow as tf
            """
        import_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_finds_incorrect_pytorch(self):
        """Test if message is added when pytorch is imported incorrectly."""
        script = """
            import torch as tr
            """
        import_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="import-pytorch", node=import_node)):
            self.checker.visit_import(import_node)

    def test_ignore_correct_pytorch(self):
        """Test if no message is added when pytorch is imported correclty"""
        script =  """
            import torch
            """
        import_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
