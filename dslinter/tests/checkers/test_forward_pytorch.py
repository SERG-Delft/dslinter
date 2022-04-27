"""Class which tests the ForwardPytorchChecker."""
import astroid
import pylint.testutils

import dslinter


class TestForwardPytorchChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the ForwardPytorchChecker."""

    CHECKER_CLASS = dslinter.plugin.ForwardPytorchChecker

    def test_use_forward(self):
        """Message will be added if the self.net.forward() is used in the code rather than self.net()."""
        script = """
        import torch.nn as nn
        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.conv1 = nn.Conv2d(3, 6, 5)
                self.pool = nn.MaxPool2d(2, 2)
                self.conv2 = nn.Conv2d(6, 16, 5)
                self.fc1 = nn.Linear(16 * 5 * 5, 120)
                self.fc2 = nn.Linear(120, 84)
                self.fc3 = nn.Linear(84, 10)
        
            def forward(self, x):
                x = self.pool.forward(F.relu(self.conv1(x))) #@
                x = self.pool(F.relu(self.conv2(x)))
                x = torch.flatten(x, 1) # flatten all dimensions except batch
                x = F.relu(self.fc1(x))
                x = F.relu(self.fc2(x))
                x = self.fc3(x)
                return x
        """
        call_node = astroid.extract_node(script).value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="forward-pytorch", node=call_node)):
            self.checker.visit_call(call_node)

    def test_not_use_forward(self):
        """No message will be added if self.net() is used in the code."""
        script = """
        import torch.nn as nn
        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.conv1 = nn.Conv2d(3, 6, 5)
                self.pool = nn.MaxPool2d(2, 2)
                self.conv2 = nn.Conv2d(6, 16, 5)
                self.fc1 = nn.Linear(16 * 5 * 5, 120)
                self.fc2 = nn.Linear(120, 84)
                self.fc3 = nn.Linear(84, 10)
        
            def forward(self, x):
                x = self.pool(F.relu(self.conv1(x))) #@
                x = self.pool(F.relu(self.conv2(x)))
                x = torch.flatten(x, 1) # flatten all dimensions except batch
                x = F.relu(self.fc1(x))
                x = F.relu(self.fc2(x))
                x = self.fc3(x)
                return x
        """
        call_node = astroid.extract_node(script).value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_use_self_forward(self):
        """No Message will be added if the self.forward() is used in the code."""
        script = """
        def training_step(self, batch, batch_nb):
            idx = batch['idx']
            loss = self.forward(batch)[0] #@
            return {'loss': loss, 'idx': idx}
        """
        call_node = astroid.extract_node(script).value.value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_use_super_forward(self):
        """No Message will be added if the super().forward() is used in the code."""
        script = """
        class SpatialDropout(nn.Dropout2d):
            def forward(self, x):
                x = x.unsqueeze(2)    # (N, T, 1, K)
                x = x.permute(0, 3, 2, 1)  # (N, K, 1, T)
                x = super(SpatialDropout, self).forward(x)  # (N, K, 1, T), some features are masked #@
                x = x.permute(0, 3, 2, 1)  # (N, T, 1, K)
                x = x.squeeze(2)  # (N, T, K)
                return x        
        """
        call_node = astroid.extract_node(script).value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)
