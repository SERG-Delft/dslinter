"""Some helper functions for inplace checkers"""
import astroid


def inplace_is_true(node: astroid.Call, argument: str) -> bool:
    """
    Evaluate whether the call has an 'out==True' keyword argument.

    :param node: Node to check the arguments from.
    :return: True when the call has an 'inplace==True' keyword argument.
    """
    if node.keywords is None:
        return False

    for keyword in node.keywords:
        if keyword.arg == argument:
            return keyword.value.value
    return False
