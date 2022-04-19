"""Class which tests RandomnessControllingDataLoaderPytorchChecker"""
import astroid
import pylint.testutils
import dslinter


class TestRandomnessControlDataloaderPytorchChecker(pylint.testutils.CheckerTestCase):
    """Class which tests RandomnessControllingDataloaderPytorchChecker"""

    CHECKER_CLASS = dslinter.plugin.RandomnessControlDataloaderPytorchChecker

    def test_with_dataloader_randomness_control1(self):
        """Tests whether no message is added if manual seed is set."""
        script = """
            import torch
            import numpy
            import random
            from torch.utils.data import DataLoader #@

            def seed_worker(worker_id):
                worker_seed = torch.initial_seed() % 2**32
                numpy.random.seed(worker_seed)
                random.seed(worker_seed)

            g = torch.Generator()
            g.manual_seed(0)

            batch_size = 4
            num_workers = 4
            train_dataset = [1, 1, 1, 1]

            train_dataloader = DataLoader( #@
                train_dataset,
                batch_size=batch_size,
                num_workers=num_workers,
                worker_init_fn=seed_worker,
                generator=g,
            )
        """
        import_from_node, assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from_node)
            self.checker.visit_call(call_node)

    def test_without_dataloader_randomness_control1(self):
        """Tests whether a message is added if manual seed is not set"""
        script = """
            from torch.utils.data import DataLoader #@
            train_dataloader = DataLoader( #@
                train_dataset,
                batch_size=batch_size,
                num_workers=num_workers
            )
        """
        import_from_node, assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="randomness-control-dataloader-pytorch", node=call_node)):
            self.checker.visit_importfrom(import_from_node)
            self.checker.visit_call(call_node)

    def test_with_dataloader_randomness_control2(self):
        """Tests whether no message is added if manual seed is set."""
        script = """
            import torch
            import numpy
            import random

            def seed_worker(worker_id):
                worker_seed = torch.initial_seed() % 2**32
                numpy.random.seed(worker_seed)
                random.seed(worker_seed)

            g = torch.Generator()
            g.manual_seed(0)

            batch_size = 4
            num_workers = 4
            train_dataset = [1, 1, 1, 1]

            train_dataloader = torch.utils.data.DataLoader( #@
                train_dataset,
                batch_size=batch_size,
                num_workers=num_workers,
                worker_init_fn=seed_worker,
                generator=g,
            )
        """
        call_node = astroid.extract_node(script).value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_without_dataloader_randomness_control2(self):
        """Tests whether a message is added if manual seed is not set"""
        script = """
            from torch.utils.data import DataLoader
            train_dataloader = torch.utils.data.DataLoader( #@
                train_dataset,
                batch_size=batch_size,
                num_workers=num_workers
            )
        """
        call_node = astroid.extract_node(script).value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="randomness-control-dataloader-pytorch", node=call_node)):
            self.checker.visit_call(call_node)
