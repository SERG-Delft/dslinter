"""Checker which checks rules for excessive hyperparameter precision."""
import traceback
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.resources import Resources

import decimal

class ExcessiveHyperparameterPrecision(BaseChecker):
    """Checker which checks rules for excessive hyperparameter precision."""

    __implements__ = IAstroidChecker

    name = "excessive-hyperparameter-precision"
    priority = -1
    msgs = {
        "W5507": (
            "excessive hyperparameter precision might suggest over-tuning",
            "excessive hyperparameter precision",
            "excessive hyperparameter precision might suggest over-tuning"
        ),
    }
    options = ()

    highPrecisionCombinations={
        "KMeans":["tol"],
        "GraphicalLasso":[" tol","enet_tol"],
        "CCA":["tol"],"PLSCanonical":["tol"],
        "PLSRegression":["tol"],
        "GraphicalLassoCV":["tol","enet_tol"],
        "DictionaryLearning":["tol"],
        "FastICA":["tol"],
        "NMF":["tol"],
        "SparsePCA":["tol"],
        "LinearDiscriminantAnalysis":["tol"],
        "QuadraticDiscriminantAnalysis":["tol"],
        "GradientBoostingClassifier":["tol"],
        "GradientBoostingRegressor":["tol"],
        "HistGradientBoostingRegressor":["tol"],
        "HistGradientBoostingClassifier":["tol"],
        "GenericUnivariateSelect":["param"],
        "GaussianProcessRegressor": ["alpha"],
        "LogisticRegression":["tol"],
        "LogisticRegressionCV":["tol"],
        "Perceptron":["alpha"],
        "SGDClassifier":["alpha"],
        "SGDRegressor":["alpha"],
        "ElasticNet":["tol"],
        "ElasticNetCV":["tol"],
        "Lars":["eps"],
        "LarsCV":["eps"],
        "Lasso":["tol"],
        "LassoCV":["tol"],
        "LassoLars":["eps"],
        "LassoLarsCV":["eps"],
        "LassoLarsIC":["eps"],
        "ARDRegression":["alpha_1","alpha_2","lambda_1","lambda_2"],
        "BayesianRidge":["alpha_1","alpha_2","lambda_1","lambda_2"],
        "MultiTaskElasticNet":["tol"],
        "MultiTaskElasticNetCV":["tol"],
        "MultiTaskLasso":["tol"],
        "MultiTaskLassoCV":["tol"],
        "HuberRegressor":["alpha","tol"],
        "LocallyLinearEmbedding":["tol","hessian_tol","modified_tol"],
        "TSNE":["min_grad_norm"],
        "BayesianGaussianMixture":["reg_covar"],
        "GaussianMixture":["reg_covar"],
        "GaussianNB":["var_smoothing"],
        "NeighborhoodComponentsAnalysis":["tol"],
        "MLPClassifier":["alpha","tol"],
        "MLPRegressor":["alpha","tol"],
        "LinearSVC":["tol"],
        "LinearSVR":["tol"],
        }

    precisionThreshold = 3

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rules in this checker.

        :param node: The node which is visited.
        """
        try:
            try:
                function_name = node.func.name
            except AttributeError:
                return

            hyperparams_all = Resources.get_hyperparameters()
            if function_name in hyperparams_all:
                if(node.keywords is not None):
                    for keyword in node.keywords:
                        if(
                            function_name in self.highPrecisionCombinations
                            and keyword.arg in self.highPrecisionCombinations[function_name]
                        ):
                            continue
                        if (
                                hasattr(keyword, "value")
                                and hasattr(keyword.value, "value")
                                and type(keyword.value.value) == float
                                and decimal.Decimal(keyword.value.as_string()).as_tuple().exponent < 0
                                and abs(decimal.Decimal(keyword.value.as_string()).as_tuple().exponent) > self.precisionThreshold
                        ):
                            self.add_message("excessive hyperparameter precision", node=node)
        except:
            ExceptionHandler.handle(self, node)
            traceback.print_exc()