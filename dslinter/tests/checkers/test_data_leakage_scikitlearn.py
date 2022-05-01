"""Class which tests the DataLeakageChecker."""
import astroid
import pylint.testutils
import dslinter


class TestDataLeakageScikitLearnChecker(pylint.testutils.CheckerTestCase):
    """Class which tests the DataLeakageChecker."""

    CHECKER_CLASS = dslinter.plugin.DataLeakageScikitLearnChecker

    def test_pipeline_violation_on_call(self):
        """Message should be added when learning function is called directly on a learning class."""
        script = """
        from sklearn.datasets import load_wine
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        from sklearn.svm import SVC
        from sklearn.preprocessing import StandardScaler
        
        # Make a train/tests split using 30% tests size
        RANDOM_STATE = 42
        features, target = load_wine(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.30, random_state=RANDOM_STATE
        )
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.fit_transform(X_test)
        
        # Fit to data and predict using pipelined GNB and PCA
        SVC().fit(X_train, y_train) #@
        """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_learning_function_without_preprocessor(self):
        """No message should be added when a learning function is called on a non-estimator."""
        script = """
        KMeans().fit(X_train) #@
        """
        call_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_learning_function_on_not_an_estimator(self):
        """No message should be added when a learning function is called on a non-estimator."""
        script = """
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        A().fit(X_train) #@
        """
        call_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_pipeline_violation_outside_block(self):
        """Test whether sk-pipeline violation is found when assignment is done outside block."""
        script = """
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)        
        model = KMeans()
        if True:
            model.fit(X_train) #@
        """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_on_name(self):
        """Message should be added when learning function is called directly on a learning class."""
        script = """
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)          
        kmeans = KMeans()
        kmeans.fit(X_train) #@
        """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_on_name_twice(self):
        """Test calling an estimator by multiple assignments."""
        script = """
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)          
        kmeans = KMeans()
        kmeans2 = kmeans
        kmeans2.fit(X_train) #@
        """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_in_function(self):
        """Test whether sk-pipeline violation is found when assignment is a function argument."""
        script = """
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)          
        def f(model):
            model.fit(X_train) #@
        f(KMeans())
        """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_in_function_arg_assigned(self):
        """Test calling an estimator within a function, where the argument is assigned."""
        script = """
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)             
        def f(model):
            model.fit(X_train) #@
        kmeans_model = KMeans()
        f(kmeans_model)
        """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)

    def test_pipeline_violation_in_second_function_argument(self):
        """Test calling an estimator with a second function argument."""
        script = """
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)        
        def f(x, model):
            model.fit(X_train) #@
        f(0, KMeans())
        """
        call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-leakage-scikitlearn", node=call_node),):
            self.checker.visit_call(call_node)
