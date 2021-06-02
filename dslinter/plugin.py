"""Main module for the plugin."""
from dslinter.checkers.data_leakage import DataLeakageChecker
from dslinter.checkers.dataframe import DataFrameChecker
from dslinter.checkers.hyperparameters import HyperparameterChecker
from dslinter.checkers.imports import ImportChecker
from dslinter.checkers.nan import NanChecker
from dslinter.checkers.controlling_randomness import ControllingRandomness
from dslinter.checkers.excessive_hyperparameter_precision import ExcessiveHyperparameterPrecision
from dslinter.checkers.pca_scaler import PCAScalerChecker


def register(linter):
    """
    Register checkers of the plugin with the linter.

    :param linter: Linter to add the checkers to.
    """
    linter.register_checker(ImportChecker(linter))
    linter.register_checker(HyperparameterChecker(linter))
    linter.register_checker(NanChecker(linter))
    linter.register_checker(DataFrameChecker(linter))
    linter.register_checker(DataLeakageChecker(linter))
    linter.register_checker(ControllingRandomness(linter))
    linter.register_checker(ExcessiveHyperparameterPrecision(linter))
    linter.register_checker(PCAScalerChecker(linter))
    
