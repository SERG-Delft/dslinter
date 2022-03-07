"""Checker which checkes whether random seed is set in pytorch"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid


class RandomnessControllingPytorchChecker(BaseChecker):
    """Checker which checks whether random seed is set in pytorch"""
    __implements__ = IAstroidChecker

    name = "randomness-control-pytorch"
    priority = -1
    msgs = {
        "W5573": (
            "torch.manual_seed() is not set in pytorch program",
            "randomness-control-pytorch",
            "torch.manual_seed() should be set in pytorch program for reproducible result"
        )
    }
    options = ()

    _import_pytorch = False
    _has_manual_seed = False
    _is_main_module = False

    def visit_import(self, node: astroid.Import):
        """
        Check whether there is a pytorch import.
        :param node: import node
        """
        for name, _ in node.names:
            if name == "torch":
                self._import_pytorch = True

    def visit_module(self, module: astroid.Module):
        """
        Check whether there is a rule violation.
        :param module:
        """

        self._is_main_module = self._check_main_module(module)

        for node in module.body:
            if isinstance(node, astroid.nodes.Expr) and hasattr(node, "value"):
                call_node = node.value
                if(
                    hasattr(call_node, "func")
                    and hasattr(call_node.func, "attrname")
                    and call_node.func.attrname == "manual_seed"
                ):
                    self._has_manual_seed = True

        if(
            self._is_main_module is True
            and self._import_pytorch is True
            and self._has_manual_seed is False
        ):
            self.add_message("randomness-control-pytorch", node = module)

    def _check_main_module(self, module: astroid.Module) -> bool:
        return True
        # for node in module.body:
        #     if isinstance(node, astroid.nodes.If) and hasattr(node, "test"):
        #         if_compare_node = node.test
        #         if(
        #             if_compare_node.left.name == "__name__"
        #             and if_compare_node.ops[0][1] == '__main__'
        #         ):
        #             return True

