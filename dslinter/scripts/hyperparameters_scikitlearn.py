"""Get all parameters of the learning algorithms in scikit-learn 0.22.2."""
# pylint: disable = line-too-long
# pylint: disable = import-error
from sklearn.calibration import CalibratedClassifierCV
from sklearn.cluster import AffinityPropagation, AgglomerativeClustering, Birch, DBSCAN, FeatureAgglomeration, KMeans, MiniBatchKMeans, MeanShift, OPTICS, SpectralClustering, SpectralBiclustering, SpectralCoclustering
from sklearn.covariance import EmpiricalCovariance, EllipticEnvelope, GraphicalLasso, GraphicalLassoCV, LedoitWolf, MinCovDet, OAS, ShrunkCovariance
from sklearn.cross_decomposition import CCA, PLSCanonical, PLSRegression, PLSSVD
from sklearn.decomposition import DictionaryLearning, FactorAnalysis, FastICA, IncrementalPCA, KernelPCA, LatentDirichletAllocation, MiniBatchDictionaryLearning, MiniBatchSparsePCA, NMF, PCA, SparsePCA, SparseCoder, TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor, BaggingClassifier, BaggingRegressor, ExtraTreesClassifier, ExtraTreesRegressor, GradientBoostingClassifier, GradientBoostingRegressor, IsolationForest, RandomForestClassifier, RandomForestRegressor, RandomTreesEmbedding, StackingClassifier, StackingRegressor, VotingClassifier, VotingRegressor, HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.feature_selection import GenericUnivariateSelect, SelectPercentile, SelectKBest, SelectFpr, SelectFdr, SelectFromModel, SelectFwe, RFE, RFECV, VarianceThreshold
from sklearn.gaussian_process import GaussianProcessClassifier, GaussianProcessRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, PassiveAggressiveClassifier, Perceptron, RidgeClassifier, RidgeClassifierCV, SGDClassifier, LinearRegression, Ridge, RidgeCV, SGDRegressor, ElasticNet, ElasticNetCV, Lars, LarsCV, Lasso, LassoCV, LassoLars, LassoLarsCV, LassoLarsIC, OrthogonalMatchingPursuit, OrthogonalMatchingPursuitCV, ARDRegression, BayesianRidge, MultiTaskElasticNet, MultiTaskElasticNetCV, MultiTaskLasso, MultiTaskLassoCV, HuberRegressor, RANSACRegressor, TheilSenRegressor, PassiveAggressiveRegressor
from sklearn.manifold import Isomap, LocallyLinearEmbedding, MDS, SpectralEmbedding, TSNE
from sklearn.mixture import BayesianGaussianMixture, GaussianMixture
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier, OutputCodeClassifier
from sklearn.multioutput import ClassifierChain, MultiOutputRegressor, MultiOutputClassifier, RegressorChain
from sklearn.naive_bayes import BernoulliNB, CategoricalNB, ComplementNB, GaussianNB, MultinomialNB
from sklearn.neighbors import BallTree, DistanceMetric, KDTree, KernelDensity, KNeighborsClassifier, KNeighborsRegressor, KNeighborsTransformer, LocalOutlierFactor, RadiusNeighborsClassifier, RadiusNeighborsRegressor, RadiusNeighborsTransformer, NearestCentroid, NearestNeighbors, NeighborhoodComponentsAnalysis
from sklearn.neural_network import BernoulliRBM, MLPClassifier, MLPRegressor
from sklearn.semi_supervised import LabelPropagation, LabelSpreading
from sklearn.svm import LinearSVC, LinearSVR, NuSVC, NuSVR, OneClassSVM, SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, ExtraTreeClassifier, ExtraTreeRegressor

# Collect learning classes. A class is a learning class if it is described in section '1. Supervised learning' or '2. Unsupervised learning' of the scikit-learn user guide.
from dslinter.scripts.hyperparameters import save_hyperparameter

learning_classes = []
learning_classes.extend([CalibratedClassifierCV])  # calibration
learning_classes.extend([AffinityPropagation, AgglomerativeClustering, Birch, DBSCAN, FeatureAgglomeration, KMeans, MiniBatchKMeans, MeanShift, OPTICS, SpectralClustering, SpectralBiclustering, SpectralCoclustering])  # cluster
learning_classes.extend([EmpiricalCovariance, EllipticEnvelope, GraphicalLasso, GraphicalLassoCV, LedoitWolf, MinCovDet, OAS, ShrunkCovariance])  # covariance
learning_classes.extend([CCA, PLSCanonical, PLSRegression, PLSSVD])  # cross_decomposition
learning_classes.extend([DictionaryLearning, FactorAnalysis, FastICA, IncrementalPCA, KernelPCA, LatentDirichletAllocation, MiniBatchDictionaryLearning, MiniBatchSparsePCA, NMF, PCA, SparsePCA, SparseCoder, TruncatedSVD])  # decomposition
learning_classes.extend([LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis])  # discriminant_analysis
learning_classes.extend([AdaBoostClassifier, AdaBoostRegressor, BaggingClassifier, BaggingRegressor, ExtraTreesClassifier, ExtraTreesRegressor, GradientBoostingClassifier, GradientBoostingRegressor, IsolationForest, RandomForestClassifier, RandomForestRegressor, RandomTreesEmbedding, StackingClassifier, StackingRegressor, VotingClassifier, VotingRegressor, HistGradientBoostingClassifier, HistGradientBoostingRegressor])  # ensemble
learning_classes.extend([GenericUnivariateSelect, SelectPercentile, SelectKBest, SelectFpr, SelectFdr, SelectFromModel, SelectFwe, RFE, RFECV, VarianceThreshold])  # feature_selection
learning_classes.extend([GaussianProcessClassifier, GaussianProcessRegressor])  # gaussian_process
learning_classes.extend([IsotonicRegression])  # isotonic
learning_classes.extend([KernelRidge])  # kernel_ridge
learning_classes.extend([LogisticRegression, LogisticRegressionCV, PassiveAggressiveClassifier, Perceptron, RidgeClassifier, RidgeClassifierCV, SGDClassifier, LinearRegression, Ridge, RidgeCV, SGDRegressor, ElasticNet, ElasticNetCV, Lars, LarsCV, Lasso, LassoCV, LassoLars, LassoLarsCV, LassoLarsIC, OrthogonalMatchingPursuit, OrthogonalMatchingPursuitCV, ARDRegression, BayesianRidge, MultiTaskElasticNet, MultiTaskElasticNetCV, MultiTaskLasso, MultiTaskLassoCV, HuberRegressor, RANSACRegressor, TheilSenRegressor, PassiveAggressiveRegressor])  # linear_model
learning_classes.extend([Isomap, LocallyLinearEmbedding, MDS, SpectralEmbedding, TSNE])  # manifold
learning_classes.extend([BayesianGaussianMixture, GaussianMixture])  # mixture_classes
learning_classes.extend([OneVsRestClassifier, OneVsOneClassifier, OutputCodeClassifier])  # multiclass
learning_classes.extend([ClassifierChain, MultiOutputRegressor, MultiOutputClassifier, RegressorChain])  # multioutput
learning_classes.extend([BernoulliNB, CategoricalNB, ComplementNB, GaussianNB, MultinomialNB])  # naive_bayes
learning_classes.extend([BallTree, DistanceMetric, KDTree, KernelDensity, KNeighborsClassifier, KNeighborsRegressor, KNeighborsTransformer, LocalOutlierFactor, RadiusNeighborsClassifier, RadiusNeighborsRegressor, RadiusNeighborsTransformer, NearestCentroid, NearestNeighbors, NeighborhoodComponentsAnalysis])  # neighbors
learning_classes.extend([BernoulliRBM, MLPClassifier, MLPRegressor])  # neural_network
learning_classes.extend([LabelPropagation, LabelSpreading])  # semi_supervised
learning_classes.extend([LinearSVC, LinearSVR, NuSVC, NuSVR, OneClassSVM, SVC, SVR])  # svm_classes
learning_classes.extend([DecisionTreeClassifier, DecisionTreeRegressor, ExtraTreeClassifier, ExtraTreeRegressor])  # tree

if __name__ == "__main__":
    save_hyperparameter(learning_classes, "../resources/hyperparameters_scikitlearn_dict.pickle")
