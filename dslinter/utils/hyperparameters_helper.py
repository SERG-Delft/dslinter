import astroid


def check_module_with_library(node, library_name: str):
    while not isinstance(node.parent, astroid.Module):
        node = node.parent
    module = node

    if isinstance(module, astroid.Module):
        for node in module.body:
            if isinstance(node, astroid.Import):
                for name, _ in node.names:
                    if name == library_name:
                        return True
    return False
