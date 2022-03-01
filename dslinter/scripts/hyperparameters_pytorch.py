"""Get all parameters of the learning algorithms in pytorch."""
# pylint: disable = line-too-long
# pylint: disable = import-error
from torch.utils.data import DataLoader
from torch.optim import Adadelta, Adagrad, Adam, AdamW, SparseAdam, Adamax, ASGD, LBFGS, NAdam, RAdam, RMSprop, Rprop, SGD
from dslinter.scripts.hyperparameters import save_hyperparameter

learning_classes = []
learning_classes.extend([DataLoader])  # dataloader
learning_classes.extend([Adadelta, Adagrad, Adam, AdamW, SparseAdam, Adamax, ASGD, LBFGS, NAdam, RAdam, RMSprop, Rprop, SGD]) #optimizer

if __name__ == "__main__":
    save_hyperparameter(learning_classes, "../resources/hyperparameters_pytorch_dict.pickle")
