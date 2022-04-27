"""Class which tests DataframeConversionPandasChecker."""
import astroid
import pylint.testutils

import dslinter


class TestDataframeConversionPandasChecker(pylint.testutils.CheckerTestCase):
    """Class which tests DataframeConversionPandasChecker."""

    CHECKER_CLASS = dslinter.plugin.DataframeConversionPandasChecker

    def test_dataframe_conversion_incorrectly_used1(self):
        """Message should be added if .values is used for dataframe conversion."""
        script = """
        import numpy as np
        import pandas as pd #@
        
        index = [1, 2, 3, 4, 5, 6, 7]
        a = [np.nan, np.nan, np.nan, 0.1, 0.1, 0.1, 0.1]
        b = [0.2, np.nan, 0.2, 0.2, 0.2, np.nan, np.nan]
        c = [np.nan, 0.5, 0.5, np.nan, 0.5, 0.5, np.nan]
        df = pd.DataFrame({'A': a, 'B': b, 'C': c}, index=index)
        # df = df.rename_axis('ID')
        arr = df.values #@     
        """
        import_node, assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="dataframe-conversion-pandas", node=call_node)):
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)

    def test_dataframe_conversion_correctly_used(self):
        """No message should be added if .to_numpy() is used for dataframe conversion."""
        script = """
        import numpy as np
        import pandas as pd #@
        
        index = [1, 2, 3, 4, 5, 6, 7]
        a = [np.nan, np.nan, np.nan, 0.1, 0.1, 0.1, 0.1]
        b = [0.2, np.nan, 0.2, 0.2, 0.2, np.nan, np.nan]
        c = [np.nan, 0.5, 0.5, np.nan, 0.5, 0.5, np.nan]
        df = pd.DataFrame({'A': a, 'B': b, 'C': c}, index=index)
        # df = df.rename_axis('ID')
        arr = df.to_numpy()   #@
        """
        import_node, assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)

    def test_dataframe_conversion_incorrectly_used2(self):
        """Message should be added if .values is used for dataframe conversion."""
        script = """
        # LOAD LIBRARIES
        import pandas as pd #@
        import numpy as np
        from sklearn.model_selection import train_test_split
        from keras.utils.np_utils import to_categorical
        from keras.models import Sequential
        from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization
        from keras.preprocessing.image import ImageDataGenerator
        from keras.callbacks import LearningRateScheduler

        # # Load Kaggle's 42,000 training images

        # In[ ]:

        # LOAD THE DATA
        train = pd.read_csv("../input/train.csv")
        test = pd.read_csv("../input/test.csv")

        # In[ ]:

        # PREPARE DATA FOR NEURAL NETWORK
        Y_train = train["label"]
        X_train = train.drop(labels = ["label"],axis = 1)
        X_train = X_train / 255.0
        X_test = test / 255.0
        X_train = X_train.values.reshape(-1,28,28,1) #@
        X_test = X_test.values.reshape(-1,28,28,1)
        Y_train = to_categorical(Y_train, num_classes = 10)
        """
        import_node, assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="dataframe-conversion-pandas", node=call_node)):
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)

    def test_dataframe_conversion_incorrectly_used3(self):
        """Message should be added if .values is used for dataframe conversion."""
        script = """
        import pandas as pd #@
        price_mm = MinMaxScaler().fit_transform(price.values.reshape(-1, 1).astype(np.float64)).flatten() #@
        """
        import_node, assign_node = astroid.extract_node(script)
        call_node = assign_node.value.func.expr.args[0].func.expr
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="dataframe-conversion-pandas", node=call_node)):
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)
