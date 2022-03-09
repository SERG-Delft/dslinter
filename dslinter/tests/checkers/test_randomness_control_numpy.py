"""Class which tests RandomnessControllingNumpyChecker"""
import astroid
import pylint.testutils
import dslinter


class TestRandomnessControlNumpyChecker(pylint.testutils.CheckerTestCase):
    """Class which tests RandomnessControllingNumpyChecker"""

    CHECKER_CLASS = dslinter.plugin.RandomnessControlNumpyChecker

    def test_with_numpy_randomness_control(self):
        """Tests whether no message is added if manual seed is set."""
        script = """
        import numpy as np #@
        np.random.seed(0)
        np.random.rand(4)
                
        if __name__ == '__main__':
            pass
        """
        import_node = astroid.extract_node(script)
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_module(module)

    def test_without_numpy_randomness_control(self):
        """Tests whether a message is added if manual seed is not set"""
        script = """
        import numpy as np #@
        np.random.rand(4) 
                
        if __name__ == '__main__':
            pass
        """
        import_node = astroid.extract_node(script)
        module = astroid.parse(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="randomness-control-numpy", node = module)):
            self.checker.visit_import(import_node)
            self.checker.visit_module(module)
