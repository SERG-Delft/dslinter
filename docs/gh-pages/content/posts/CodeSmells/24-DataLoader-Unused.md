---
title: "DataLoader Unused"
disableShare: true
# ShowReadingTime: true
tags: ["api-specific", "model evaluation", "robustness"]
weight: 24
summary: "Use `DataLoader` to load the data in PyTorch instead of splitting data manually and feed into the network."
---

### Description

#### Context

`DataLoader` API supports the data loading utility in PyTorch.

#### Problem

Some new developers are unaware of existing functions and end up reinventing the wheel. For instance, in a Stack Overflow post, the developer does not use the `DataLoader` and feeds the data directly to the network. However, it is recommended to use the APIs because the APIs provided by the library often consider more cases. 

#### Solution

Using `DataLoader` API has several advantages: 1) It enables developers to take random samples of the data. 2) It does not preload data into memory, which is especially beneficial when dealing with large datasets. 3) It runs in the background of the code, fetching data in parallel to train, hence saving time. Therefore, it is more efficient and robust to use the `DataLoader` API than manually splitting the data and directly feeding the data into the network.

### Type

API-Specific

### Existing Stage

Model Evaluation

### Effect

Robustness

### Example

```diff
### PyTorch
# 1. Load and normalize CIFAR10
import torch
import torchvision
import torchvision.transforms as transforms
import torch.utils.data as data_utils

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 4

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
+ trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
+                                           shuffle=True, num_workers=0)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
+ testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
+                                          shuffle=False, num_workers=0)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# 2. Define a Convolutional Neural Network
import torch.nn as nn
import torch.nn.functional as F

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
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()

# 3. Define a Loss function and optimizer
import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# 4. Train the network
for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    net.train()
-   for i in range(int(len(trainset) / batch_size)):
+   for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
-       inputs, labels = (trainset.data[i * batch_size: (i + 1) * batch_size]
-                            , trainset.targets[i * batch_size: (i + 1) * batch_size])
+       inputs, labels = data

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
            #...

print('Finished Training')

PATH = './cifar_net.pth'
torch.save(net.state_dict(), PATH)

# 5. Test the network on the test data
correct = 0
total = 0
# since we're not training, we don't need to calculate the gradients for our outputs
with torch.no_grad():
    for data in testloader:
        images, labels = data
        # calculate outputs by running images through the network
        outputs = net(images)
        # the class with the highest energy is what we choose as prediction
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Accuracy of the network on the 10000 test images: {100 * correct // total} %')
```

### Source:

#### Paper 

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/67066452/is-this-a-right-way-to-train-and-test-the-model-using-pytorch/67067242#67067242

#### Documentation

