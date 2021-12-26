---
title: "Train Eval Mode Improper Toggling"
disableShare: true
# ShowReadingTime: true
tags: ["api-specific", "model training", "error-prone"]
weight: 22
---

### Description

In PyTorch, calling `.eval()` means we are going into the evaluation mode and the Dropout layer will be deactivated. If the training mode did not toggle back in time, the Dropout layer would not be used in some data training and thus affect the training result. Therefore, we suggest to "have the training mode set as close as possible to the inference step to avoid forgetting to set it".

### Type

API Specific

### Existing Stage

Model Training

### Effect

Error-prone

### Example

```python

### PyTorch

# Violated Code
def train(model, optimizer, epoch, train_loader, validation_loader):
    model.train() # 👈👈👈
    for batch_idx, (data, target) in experiment.batch_loop(iterable=train_loader):
        data, target = Variable(data), Variable(target)
        # Inference
        output = model(data)
        loss_t = F.nll_loss(output, target)
        # The iconic grad-back-step trio
        optimizer.zero_grad()
        loss_t.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            train_loss = loss_t.item()
            train_accuracy = get_correct_count(output, target) * 100.0 / len(target)
            experiment.add_metric(LOSS_METRIC, train_loss)
            experiment.add_metric(ACC_METRIC, train_accuracy)
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx, len(train_loader),
                100. * batch_idx / len(train_loader), train_loss))
            with experiment.validation():
                val_loss, val_accuracy = test(model, validation_loader) # 👈👈👈
                experiment.add_metric(LOSS_METRIC, val_loss)
                experiment.add_metric(ACC_METRIC, val_accuracy)

def test(model, test_loader):
   model.eval()


# Recommended Fix
def train(model, optimizer, epoch, train_loader, validation_loader):
    for batch_idx, (data, target) in experiment.batch_loop(iterable=train_loader):
        model.train() # 👈👈👈
        data, target = Variable(data), Variable(target)
        # Inference
        output = model(data)
        loss_t = F.nll_loss(output, target)
        # The iconic grad-back-step trio
        optimizer.zero_grad()
        loss_t.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            train_loss = loss_t.item()
            train_accuracy = get_correct_count(output, target) * 100.0 / len(target)
            experiment.add_metric(LOSS_METRIC, train_loss)
            experiment.add_metric(ACC_METRIC, train_accuracy)
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx, len(train_loader),
                100. * batch_idx / len(train_loader), train_loss))
            with experiment.validation():
                val_loss, val_accuracy = test(model, validation_loader) # 👈👈👈
                experiment.add_metric(LOSS_METRIC, val_loss)
                experiment.add_metric(ACC_METRIC, val_accuracy)

def test(model, test_loader):
   model.eval()

```

### Source:

#### Paper 

#### Grey Literature
- https://medium.com/missinglink-deep-learning-platform/most-common-neural-net-pytorch-mistakes-456560ada037

#### GitHub Commit

#### Stack Overflow

#### Documentation

