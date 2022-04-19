import astroid
import dslinter.plugin
import pylint.testutils


class TestScalerMissingScikitLearnChecker(pylint.testutils.CheckerTestCase):
    """Class which tests ScalerMissingScikitLearnChecker"""

    CHECKER_CLASS = dslinter.plugin.ScalerMissingScikitLearnChecker

    def test_PCA_missing_scaling(self):
        assign_node = astroid.extract_node("""
            from sklearn.datasets import load_wine
            from sklearn.model_selection import train_test_split
            from sklearn.pipeline import make_pipeline
            from sklearn.decomposition import PCA
            from sklearn.naive_bayes import GaussianNB
            from sklearn.metrics import accuracy_score

            RANDOM_STATE = 42
            features, target = load_wine(return_X_y=True)
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.30, random_state=RANDOM_STATE
            )
            clf = make_pipeline(PCA(n_components=2), GaussianNB()) #@
            clf.fit(X_train, y_train)
            pred_test = clf.predict(X_test)
            ac = accuracy_score(y_test, pred_test)
        """)
        call_node = assign_node.value
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id= 'scaler-missing-scikitlearn',
                node = call_node,
            )
        ):
            self.checker.visit_call(call_node)

    def test_PCA_with_scaling(self):
        assign_node = astroid.extract_node("""
            from sklearn.datasets import load_wine
            from sklearn.model_selection import train_test_split
            from sklearn.pipeline import make_pipeline
            from sklearn.decomposition import PCA
            from sklearn.naive_bayes import GaussianNB
            from sklearn.metrics import accuracy_score
            from sklearn.preprocessing import StandardScaler

            RANDOM_STATE = 42
            features, target = load_wine(return_X_y=True)
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.30, random_state=RANDOM_STATE
            )
            clf = make_pipeline(StandardScaler(), PCA(n_components=2), GaussianNB()) #@
            clf.fit(X_train, y_train)
            pred_test = clf.predict(X_test)
            ac = accuracy_score(y_test, pred_test)
        """)
        call_node = assign_node.value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_SVC_missing_scaling(self):
        call_node = astroid.extract_node("""
            from sklearn.datasets import load_wine
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import accuracy_score
            from sklearn.svm import SVC
            
            # Make a train/tests split using 30% tests size
            RANDOM_STATE = 42
            features, target = load_wine(return_X_y=True)
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.30, random_state=RANDOM_STATE
            )
            
            # Fit to data and predict using pipelined GNB and PCA
            clf = SVC() 
            clf.fit(X_train, y_train) #@
            pred_test = clf.predict(X_test)
            ac = accuracy_score(y_test, pred_test)
        """)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id='scaler-missing-scikitlearn', node = call_node)):
            self.checker.visit_call(call_node)


    def test_SVC_with_scaling(self):
        assign_node = astroid.extract_node("""
            from sklearn.datasets import load_wine
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import accuracy_score
            from sklearn.svm import SVC
            from sklearn.pipeline import make_pipeline
            from sklearn.preprocessing import StandardScaler
            
            # Make a train/tests split using 30% tests size
            RANDOM_STATE = 42
            features, target = load_wine(return_X_y=True)
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.30, random_state=RANDOM_STATE
            )
            
            # Fit to data and predict using pipelined GNB and PCA
            clf = make_pipeline(StandardScaler(), SVC()) #@
            clf.fit(X_train, y_train)
            pred_test = clf.predict(X_test)
            ac = accuracy_score(y_test, pred_test)
        """)
        call_node = assign_node.value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_SVC_with_scaling2(self):
        call_node = astroid.extract_node("""
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
            clf = SVC() 
            clf.fit(X_train, y_train) #@
            pred_test = clf.predict(X_test)
            ac = accuracy_score(y_test, pred_test)
        """)
        with self.assertNoMessages():
            self.checker.visit_call(call_node)
