"""Checker which checks whether random seed is set in pytorch dataloader"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid

from dslinter.utils.exception_handler import ExceptionHandler


class RandomnessControlDataloaderPytorchChecker(BaseChecker):
    """Checker which checks whether random seed is set in pytorch dataloader"""
    __implements__ = IAstroidChecker

    name = "randomness-control-dataloader-pytorch"
    priority = -1
    msgs = {
        "W5512": (
            "The worker_init_fn() and generator is not set in PyTorch DataLoader API",
            "randomness-control-dataloader-pytorch",
            "Use worker_init_fn() and generator in PyTorch DataLoader API to preserve reproducibility"
        )
    }
    options = ()

    _import_DataLoader = False

    def visit_importfrom(self, importfrom_node: astroid.ImportFrom):
        """
        Check whether there is DataLoader imported.
        """
        try:
            if(
                hasattr(importfrom_node, "modname")
                and importfrom_node.modname == "torch.utils.data"
                and hasattr(importfrom_node, "names")
            ):
                for name, _ in importfrom_node.names:
                    if name == "DataLoader":
                        self._import_DataLoader = True
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, importfrom_node)

    def visit_call(self, node: astroid.Call):
        """
        Check whether there is a rule violation.
        :param node:
        """
        try:
            if self._use_dataloader_from_import(node) or self._use_dataloader_from_torch(node):
                # In dataloader, check if "worker_init_fn" and "generator" is set.
                keywords = []
                if hasattr(node, "keywords"):
                    for k in node.keywords:
                        if hasattr(k, "arg"):
                            keywords.append(k.arg)
                if "worker_init_fn" not in keywords or "generator" not in keywords:
                    self.add_message("randomness-control-dataloader-pytorch", node=node)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, node)

    def _use_dataloader_from_import(self, node):
        # Dataloader has been imported from torch.utils.data
        if(
            self._import_DataLoader is True
            and hasattr(node.func, "name")
            and node.func.name == "DataLoader"
        ):
            return True
        return False

    def _use_dataloader_from_torch(self, node):
        # Dataloader has not been imported from torch.utils.data
        full_expr = ""
        if hasattr(node, "func"):
            node = node.func
            while hasattr(node, "expr"):
                if hasattr(node, "attrname"):
                    full_expr = node.attrname + "." + full_expr
                node = node.expr
            if hasattr(node, "name"):
                full_expr = node.name + "." + full_expr
            if full_expr[:-1] == "torch.utils.data.DataLoader":
                return True
        return False
