"""Class which tests ColumnSelectionPandasChecker."""
import pylint.testutils
import astroid
import dslinter.plugin


class TestColumnSelectionPandasChecker(pylint.testutils.CheckerTestCase):
    """Class which tests ColumnSelectionPandasChecker."""

    CHECKER_CLASS = dslinter.plugin.ColumnSelectionPandasChecker

    def test_column_not_selected(self):
        """A message should be added if there is no column selection after the dataframe is imported."""
        script = """
        import pandas as pd
        df = pd.read_csv('data.csv')
        """
        module = astroid.parse(script)
        assign_node = module.body[-1]
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="column-selection-pandas", node=assign_node)):
            self.checker.visit_module(module)

    def test_column_selected1(self):
        """No message should be added if there is column selection after the dataframe is imported."""
        script = """
        import pandas as pd
        df = pd.read_csv('data.csv')
        df = df[['col1', 'col2', 'col3']]
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_column_selected2(self):
        """No message should be added if there is column selection after the dataframe is imported."""
        script = """
        import pandas as pd
        df = pd.read_csv('data.csv')
        print(df)
        df = df[['col1', 'col2', 'col3']]
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_a_column_not_selected(self):
        """A message should be added if some imported dataframe are not selected by columns."""
        script = """
        import pandas as pd
        df1 = pd.read_csv('data1.csv')
        df2 = pd.read_csv('data2.csv')
        df1 = df1[['col1', 'col2', 'col3']]
        """
        module = astroid.parse(script)
        assign_node = module.body[-2]
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="column-selection-pandas", node=assign_node)):
            self.checker.visit_module(module)

    def test_all_columns_selected(self):
        """No message should be added if every imported dataframe is selected by columns."""
        script = """
        import pandas as pd
        df1 = pd.read_csv('data1.csv')
        df2 = pd.read_csv('data2.csv')
        df1 = df1[['col1', 'col2', 'col3']]
        df3 = df2[['col1', 'col2']]
        """
        module = astroid.parse(script)
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_violation_in_function_def(self):
        script = """
        import os
        from unittest import TestCase
        import pandas as pd
        from typing import List
        
        from lexnlp.extract.common.base_path import lexnlp_test_path
        from lexnlp.extract.common.annotations.law_annotation import LawAnnotation
        # pylint:disable=no-name-in-module
        from lexnlp.extract.de.laws import LawsParser, get_laws
        from lexnlp.tests.typed_annotations_tests import TypedAnnotationsTester
        
        class TestParseDeLaws(TestCase):
            def setup_parser(): #@
                base_path = os.path.join(lexnlp_test_path, 'lexnlp/extract/de/laws/')
                gesetze_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                      base_path + 'gesetze_list.csv'),
                                         encoding="utf-8")
            
                # verordnungen_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                #                                           base_path + 'verordnungen_list.csv'),
                #                              encoding="utf-8")
            
                # concept_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                #                                      base_path + 'de_concept_sample.csv'),
                #                         encoding="utf-8")
            
                law_parser = LawsParser(gesetze_df,
                                        verordnungen_df,
                                        concept_df)
                return law_parser
        
        parser = setup_parser()
        """
        module = astroid.parse(script)
        functiondef_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="column-selection-pandas", node=functiondef_node.body[1])):
            self.checker.visit_module(module)
            self.checker.visit_functiondef(functiondef_node)
