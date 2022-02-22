"""Get all parameters of the learning algorithms in pytorch."""
# pylint: disable = line-too-long
# pylint: disable = import-error
from tensorflow.keras.optimizers import Adadelta, Adagrad, Adam, Adamax, Ftrl, Nadam, RMSprop, SGD
from dslinter.scripts.hyperparameters import save_hyperparameter

learning_classes = []
# learning_classes.extend([])  # fit
learning_classes.extend([Adadelta, Adagrad, Adam, Adamax, Ftrl, Nadam, RMSprop, SGD]) #optimizer

if __name__ == "__main__":
    save_hyperparameter(learning_classes, "../resources/hyperparameters_tensorflow_dict.pickle")
