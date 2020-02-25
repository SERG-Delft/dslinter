from dslinter.checkers.sample import SampleChecker


def register(linter):
    linter.register_checker(SampleChecker(linter))
