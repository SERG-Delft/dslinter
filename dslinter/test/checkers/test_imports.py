"""Class which tests the ImportChecker."""
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

        with self.assertAddsMessages(
            pylint.testutils.Message(msg_id="import-pandas", node=import_node),
        ):
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

        with self.assertAddsMessages(
            pylint.testutils.Message(msg_id="import-numpy", node=import_node),
        ):
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

        with self.assertAddsMessages(
            pylint.testutils.Message(msg_id="import-pyplot", node=import_node),
        ):
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
