class TestUnnecessaryIterationTensorflow():
    def test_iteration(self):
        module_tree = astroid.parse("")
        call = module_tree.body[-1].iter
        with assertAddsMessage(msg_id="", node = call, ):
            self.check.visit_call(call)
