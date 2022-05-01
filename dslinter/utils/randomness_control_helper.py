import astroid


def check_main_module(module: astroid.Module) -> bool:
    for node in module.body:
        if isinstance(node, astroid.nodes.If) and hasattr(node, "test"):
            if_compare_node = node.test
            if(
                hasattr(if_compare_node, "left")
                and hasattr(if_compare_node.left, "name")
                and if_compare_node.left.name == "__name__"
                and hasattr(if_compare_node, "ops")
                and len(if_compare_node.ops) > 0
                and hasattr(if_compare_node.ops[0][1], "value")
                and if_compare_node.ops[0][1].value == '__main__'
            ):
                return True
    return False


def has_import(node: astroid.Import, library_name: str):
    for name, _ in node.names:
        if name == library_name:
            return True
    return False


def has_importfrom_sklearn(node: astroid.ImportFrom):
    if node.modname[:7] == "sklearn":
        return True
    return False

