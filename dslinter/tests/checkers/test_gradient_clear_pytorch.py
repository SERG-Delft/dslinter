"""Class which tests the GradientClearPytorchChecker."""
import astroid
import pylint.testutils

import dslinter


class TestGradientClearPytorchChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the GradientClearPytorchChecker."""

    CHECKER_CLASS = dslinter.plugin.GradientClearPytorchChecker

    def test_gradient_not_clear(self):
        """Message should be added if the optimizer.zero_grad() is not used in pytorch code when loss_fn.backward() and optimizer.step() are used."""
        script = """
            for epoch in range(2):  # loop over the dataset multiple times
            
                running_loss = 0.0
                for i, data in enumerate(trainloader, 0): #@
                    # get the inputs; data is a list of [inputs, labels]
                    inputs, labels = data
            
                    # forward + backward + optimize
                    outputs = net(inputs)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()
            
                    # print statistics
                    running_loss += loss.item()
                    if i % 2000 == 1999:    # print every 2000 mini-batches
                        print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                        running_loss = 0.0        
        """
        for_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="gradient-clear-pytorch", node=for_node)):
            self.checker.visit_for(for_node)

    def test_gradient_clear(self):
        """No message should be added if the loss_fn.backward() and optimizer.step() should be used together with optimizer.zero_grad()."""
        script = """
            for epoch in range(2):  # loop over the dataset multiple times
            
                running_loss = 0.0
                for i, data in enumerate(trainloader, 0): #@
                    # get the inputs; data is a list of [inputs, labels]
                    inputs, labels = data
            
                    # zero the parameter gradients
                    optimizer.zero_grad()
            
                    # forward + backward + optimize
                    outputs = net(inputs)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()
            
                    # print statistics
                    running_loss += loss.item()
                    if i % 2000 == 1999:    # print every 2000 mini-batches
                        print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                        running_loss = 0.0        
        """
        for_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_for(for_node)
