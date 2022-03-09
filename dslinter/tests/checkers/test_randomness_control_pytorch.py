"""Class which tests RandomnessControllingPytorchChecker"""
import astroid
import pylint.testutils
import dslinter


class TestRandomnessControlPytorchChecker(pylint.testutils.CheckerTestCase):
    """Class which tests RandomnessControllingPytorchChecker"""

    CHECKER_CLASS = dslinter.plugin.RandomnessControlPytorchChecker

    def test_with_pytorch_randomness_control(self):
        """Tests whether no message is added if manual seed is set."""
        script = """
        import torch #@
        torch.manual_seed(0) 
        torch.randn(10).index_copy(0, torch.tensor([0]), torch.randn(1))
                
        if __name__ == '__main__':
            pass
        """
        import_node = astroid.extract_node(script)
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_module(module)

    def test_without_pytorch_randomness_control(self):
        """Tests whether a message is added if manual seed is not set"""
        script = """
        import torch #@
        torch.randn(10).index_copy(0, torch.tensor([0]), torch.randn(1)) 
                
        if __name__ == '__main__':
            pass
        """
        import_node = astroid.extract_node(script)
        module = astroid.parse(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="randomness-control-pytorch", node = module)):
            self.checker.visit_import(import_node)
            self.checker.visit_module(module)

    def test_pytorch_randomness_with_main_module(self):
        script = """
        # import statements
        import torch #@
        import torch.nn as nn
        from torch.utils import data
        
        # set flags / seeds
        torch.backends.cudnn.benchmark = True
        np.random.seed(1)
        torch.manual_seed(1)
        torch.cuda.manual_seed(1)
        
        # Start with main code
        if __name__ == '__main__':
            # argparse for additional flags for experiment
            parser = argparse.ArgumentParser(description="Train a network for ...")
            opt = parser.parse_args() 
        """
        import_node = astroid.extract_node(script)
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_module(module)
