"""Main module for the plugin."""
from dslinter.checkers.chain_indexing_pandas import ChainIndexingPandasChecker
from dslinter.checkers.column_selection_pandas import ColumnSelectionPandasChecker
from dslinter.checkers.dataframe_conversion_pandas import DataframeConversionPandasChecker
from dslinter.checkers.datatype_pandas import DatatypePandasChecker
from dslinter.checkers.dependent_threshold_pytorch import DependentThresholdPytorchChecker
from dslinter.checkers.dependent_threshold_scikitlearn import DependentThresholdScikitLearnChecker
from dslinter.checkers.dependent_threshold_tensorflow import DependentThresholdTensorflowChecker
from dslinter.checkers.forward_pytorch import ForwardPytorchChecker
from dslinter.checkers.gradient_clear_pytorch import GradientClearPytorchChecker
from dslinter.checkers.imports import ImportChecker
from dslinter.checkers.inplace_pandas import InPlacePandasChecker
from dslinter.checkers.deprecated.inplace_numpy import InPlaceNumpyChecker
from dslinter.checkers.mask_missing_pytorch import MaskMissingPytorchChecker
from dslinter.checkers.mask_missing_tensorflow import MaskMissingTensorflowChecker
from dslinter.checkers.memory_release_tensorflow import MemoryReleaseTensorflowChecker
from dslinter.checkers.merge_parameter_pandas import MergeParameterPandasChecker
from dslinter.checkers.deprecated.mode_toggling_pytorch import ModeTogglingPytorchChecker
from dslinter.checkers.randomness_control_numpy import RandomnessControlNumpyChecker
from dslinter.checkers.randomness_control_pytorch import RandomnessControlPytorchChecker
# pylint: disable = line-too-long
from dslinter.checkers.randomness_control_dataloader_pytorch import RandomnessControlDataloaderPytorchChecker
# pylint: disable = line-too-long
from dslinter.checkers.randomness_control_tensorflow import RandomnessControlTensorflowChecker
from dslinter.checkers.randomness_control_scikitlearn import RandomnessControlScikitLLearnChecker
from dslinter.checkers.tensor_array_tensorflow import TensorArrayTensorflowChecker
from dslinter.checkers.unnecessary_iteration_pandas import UnnecessaryIterationPandasChecker
from dslinter.checkers.unnecessary_iteration_tensorflow import UnnecessaryIterationTensorflowChecker
from dslinter.checkers.deterministic_pytorch import DeterministicAlgorithmChecker
from dslinter.checkers.data_leakage_scikitlearn import DataLeakageScikitLearnChecker
from dslinter.checkers.hyperparameters_pytorch import HyperparameterPyTorchChecker
from dslinter.checkers.hyperparameters_tensorflow import HyperparameterTensorflowChecker
# pylint: disable = line-too-long
from dslinter.checkers.hyperparameters_scikitlearn import HyperparameterScikitLearnChecker
from dslinter.checkers.nan_numpy import NanNumpyChecker
from dslinter.checkers.scaler_missing_scikitlearn import ScalerMissingScikitLearnChecker


def register(linter):
    """
    Register checkers of the plugin with the linter.

    :param linter: Linter to add the checkers to.
    """
    linter.register_checker(ImportChecker(linter))
    linter.register_checker(InPlacePandasChecker(linter))
    linter.register_checker(InPlaceNumpyChecker(linter))
    linter.register_checker(UnnecessaryIterationPandasChecker(linter))
    linter.register_checker(UnnecessaryIterationTensorflowChecker(linter))
    linter.register_checker(ScalerMissingScikitLearnChecker(linter))
    linter.register_checker(HyperparameterPyTorchChecker(linter))
    linter.register_checker(HyperparameterTensorflowChecker(linter))
    linter.register_checker(HyperparameterScikitLearnChecker(linter))
    linter.register_checker(MemoryReleaseTensorflowChecker(linter))
    linter.register_checker(DeterministicAlgorithmChecker(linter))
    linter.register_checker(RandomnessControlScikitLLearnChecker(linter))
    linter.register_checker(RandomnessControlPytorchChecker(linter))
    linter.register_checker(RandomnessControlDataloaderPytorchChecker(linter))
    linter.register_checker(RandomnessControlTensorflowChecker(linter))
    linter.register_checker(RandomnessControlNumpyChecker(linter))
    linter.register_checker(DataLeakageScikitLearnChecker(linter))
    linter.register_checker(DependentThresholdPytorchChecker(linter))
    linter.register_checker(DependentThresholdTensorflowChecker(linter))
    linter.register_checker(DependentThresholdScikitLearnChecker(linter))
    linter.register_checker(MaskMissingTensorflowChecker(linter))
    linter.register_checker(MaskMissingPytorchChecker(linter))

    linter.register_checker(NanNumpyChecker(linter))
    linter.register_checker(ChainIndexingPandasChecker(linter))
    linter.register_checker(MergeParameterPandasChecker(linter))
    linter.register_checker(DatatypePandasChecker(linter))
    linter.register_checker(ColumnSelectionPandasChecker(linter))
    linter.register_checker(DataframeConversionPandasChecker(linter))
    linter.register_checker(TensorArrayTensorflowChecker(linter))
    linter.register_checker(ForwardPytorchChecker(linter))
    linter.register_checker(ModeTogglingPytorchChecker(linter))
    linter.register_checker(GradientClearPytorchChecker(linter))
