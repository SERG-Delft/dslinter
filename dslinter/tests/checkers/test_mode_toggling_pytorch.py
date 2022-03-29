"""Class which tests ModeTogglingPytorchChecker."""
import astroid
import pylint.testutils

import dslinter.plugin


class TestModeTogglingPytorchChecker(pylint.testutils.CheckerTestCase):
    """Class which tests ModeTogglingPytorchChecker."""

    CHECKER_CLASS = dslinter.plugin.ModeTogglingPytorchChecker

    def test_mode_improper_toggling(self):
        """Message will be added when the training mode is not toggling back in time."""
        script = """
        for epoch in range(2):  # loop over the dataset multiple times 
            running_loss = 0.0
            net.train()
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
                    # validation
                    net.eval()        
        """
        for_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="mode-toggling-pytorch", node=for_node)):
            self.checker.visit_for(for_node)

    def test_mode_proper_toggling(self):
        """No message will be added if the training mode is toggling back in time."""
        script = """
        for epoch in range(2):  # loop over the dataset multiple times 
            running_loss = 0.0
            for i, data in enumerate(trainloader, 0): #@
                # get the inputs; data is a list of [inputs, labels]
                net.train()        
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
                    # validation
                    net.eval()        
        """
        for_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_for(for_node)
