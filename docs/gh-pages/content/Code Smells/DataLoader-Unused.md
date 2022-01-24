---
title: "DataLoader Unused"
disableShare: true
# ShowReadingTime: true
tags: ["api-specifc", "data segregation", "robustness"]
weight: 18
---

### Description

Some new developers are not aware of using the existing function and writing the function by themselves. However, it is recommended to use the APIs because the APIs provided by the library often consider more things. For instance, in a post, the developer does not use the DataLoader and feeds the data directly to the network. The answerer noted that using DataLoader has several benefits: 1) It allows the developers to sample the data randomly. 2) It does not preload data into memory, which is particularly useful for huge datasets. 3) It operates in the background of code, so it fetches data parallel to train thus saving time. 4) It is very efficient at batching the data. Therefore, it is better to use the DataLoader API than manually splitting the data and directly feeding the data into the network.

### Type

API Specific

### Existing Stage

Data Segregation

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

