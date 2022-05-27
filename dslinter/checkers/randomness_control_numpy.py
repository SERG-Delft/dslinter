"""Checker which checks whether random seed is set in numpy"""
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid

from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.randomness_control_helper import check_main_module, has_import, has_importfrom_sklearn


class RandomnessControlNumpyChecker(BaseChecker):
    """Checker which checks whether random seed is set in numpy"""
    __implements__ = IAstroidChecker

    name = "randomness-control-numpy"
    priority = -1
    msgs = {
        "W5508": (
            "The np.random.seed() is not set in numpy program.",
            "randomness-control-numpy",
            "The np.random.seed() should be set in numpy program for reproducible result."
        )
    }

    options = (
        (
            "no_main_module_check_randomness_control_numpy",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Check every module whether np.random.seed() is used.",
            },
        ),
    )

    def visit_module(self, module: astroid.Module):
        """
        Check whether there is a rule violation.
        :param module:
        """
        try:
            _import_numpy = False
            _import_ml_libraries = False
            _has_numpy_manual_seed = False

            # if the user wants to only check main module, but the current file is not main module, just return
            _is_main_module = check_main_module(module)
            if self.config.no_main_module_check_randomness_control_numpy is False and _is_main_module is False:
                return

            # traverse over the node in the module
            for node in module.body:
                if isinstance(node, astroid.Import):
                    if _import_ml_libraries is False:
                        _import_ml_libraries = has_import(node, "tensorflow") or has_import(node, "torch") or has_import(node, "sklearn")
                    if _import_numpy is False:
                        _import_numpy = has_import(node, "numpy")

                if isinstance(node, astroid.ImportFrom):
                    if _import_ml_libraries is False:
                        _import_ml_libraries = has_importfrom_sklearn(node)

                if isinstance(node, astroid.nodes.Expr):
                    if _has_numpy_manual_seed is False:
                        _has_numpy_manual_seed = self._check_numpy_manual_seed_in_expr_node(node)

                if isinstance(node, astroid.nodes.FunctionDef):
                    for nod in node.body:
                        if isinstance(nod, astroid.nodes.Expr):
                            if _has_numpy_manual_seed is False:
                                _has_numpy_manual_seed = self._check_numpy_manual_seed_in_expr_node(nod)

            # check if the rules are violated
            if(
                _import_numpy is True
                and _import_ml_libraries is True
                and _has_numpy_manual_seed is False
            ):
                self.add_message("randomness-control-numpy", node=module)
        except: # pylint: disable = bare-except
            ExceptionHandler.handle(self, module)

    @staticmethod
    def _check_numpy_manual_seed_in_expr_node(expr_node: astroid.Expr):
        if hasattr(expr_node, "value"):
            call_node = expr_node.value
            return RandomnessControlNumpyChecker._check_numpy_manual_seed_in_call_node(call_node)

    @staticmethod
    def _check_numpy_manual_seed_in_call_node(call_node: astroid.Call):
        if(
            hasattr(call_node, "func")
            and hasattr(call_node.func, "attrname")
            and call_node.func.attrname == "seed"
            and hasattr(call_node.func.expr, "attrname")
            and call_node.func.expr.attrname == "random"
            and hasattr(call_node.func.expr, "expr")
            and hasattr(call_node.func.expr.expr, "name")
            and call_node.func.expr.expr.name in ["np", "numpy"]
        ):
            return True
        return False
