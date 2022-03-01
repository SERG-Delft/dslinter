"""Class which tests RandomnessControllingScikitlearn."""
import astroid
import pylint.testutils
import dslinter.plugin


class TestRandomnessControllingScikitLearnChecker(pylint.testutils.CheckerTestCase):
    """Class which tests RandomnessControllingScikitlearn."""

    CHECKER_CLASS = dslinter.plugin.RandomnessControllingScikitLLearnChecker

    def test_with_randomness_controlling(self):
        """If there is randomness controlling in the fucntion, no message is added."""
        script = """
            from sklearn.model_selection import KFold
            rng = 0
            kf = KFold(random_state=rng) #@
        """
        assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_without_randomness_controlling(self):
        """If there is no randomness controlling in the function, a violation message is added."""
        script = """
            from sklearn.model_selection import KFold
            kf = KFold(random_state=None) #@
        """
        assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="controlling_randomness_scikitlearn", node=call_node)):
            self.checker.visit_call(call_node)

    def test_without_randomness_controlling2(self):
        """If there is no randomness controllling in the function, a ciolation message is added."""
        script = """
            from sklearn.model_selection import KFold
            kf = KFold() #@
        """
        assign_node = astroid.extract_node(script)
        call_node = assign_node.value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="controlling_randomness_scikitlearn", node=call_node)):
            self.checker.visit_call(call_node)
