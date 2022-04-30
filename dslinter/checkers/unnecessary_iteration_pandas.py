"""Check whether there is unnecessary iteration in Pandas code."""
from typing import List
from typing import Dict
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
import astroid
from dslinter.utils.exception_handler import ExceptionHandler
from dslinter.utils.ast import AssignUtil
from dslinter.utils.type_inference import TypeInference


class UnnecessaryIterationPandasChecker(BaseChecker):
    """Check whether there is unnecessary iteration in Pandas code."""
    __implements__ = IAstroidChecker

    name = "unnecessary-iteration-pandas"
    priority = -1
    msgs = {
        "R5501": (
            "Iterating through a DataFrame.",
            "unnecessary-iteration-pandas",
            "Iteration through a DataFrame is generally slow and should be avoided.",
        ),
        "W5501": (
            "Iterated object is modified.",
            "dataframe-iteration-modification-pandas",
            "An object where is iterated over should not be modified.",
        ),
    }
    options = ()

    # [node, inferred type of object the function is called on]
    _call_types: Dict[astroid.Call, str] = {}

    def visit_module(self, node: astroid.Module):
        """
        When an Module node is visited, scan for Call nodes and get type the function is called on.

        :param node: Node which is visited.
        """
        try:
            # noinspection PyTypeChecker
            self._call_types = TypeInference.infer_types(node,
                                                         astroid.Call,
                                                         lambda x: x.func.expr.name)
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, add messages if it violated the defined rules.

        :param node: Node which is visited.
        """
        try:
            if self._iterating_through_dataframe(node):
                self.add_message("dataframe-iteration-modification-pandas", node=node)
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

    def _iterating_through_dataframe(self, node: astroid.Call) -> bool:
        """
        Evaluate whether there is iterated through a DataFrame.

        :param node: Node which is visited.
        :return: True when there is iterated through a DataFrame.
        """
        return (
            isinstance(node.parent, astroid.For)
            and node not in node.parent.body
            and node in self._call_types
            and (
                self._call_types[node] == '"pandas.core.frame.DataFrame"'
                or self._call_types[node] == '"pyspark.sql.dataframe.DataFrame"'
            )
        )

    def visit_for(self, node: astroid.For):
        """
        When a For node is visited, check for dataframe-iteration-modification violations.

        :param node: Node which is visited.
        """
        try:
            if not (
                isinstance(node.iter, astroid.Call)
                and node.iter in self._call_types
                and (
                    self._call_types[node.iter] == '"pandas.core.frame.DataFrame"'
                    or self._call_types[node.iter] == '"pyspark.sql.dataframe.DataFrame"'
                )
            ):
                return

            for_targets = self._get_for_targets(node)
            assigned = AssignUtil.get_assigned_target_names(node)
            modified_iterated_targets = any(target in for_targets for target in assigned)

            if modified_iterated_targets:
                self.add_message("dataframe-iteration-modification-pandas", node=node)
        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)

    @staticmethod
    def _get_for_targets(node: astroid.For) -> List[str]:
        """
        Get the target names of the for-loop definition.

        :param node: For node to get the target names from.
        :return: Target names.
        """
        target_names = []
        if isinstance(node.target, astroid.Tuple):
            for element in node.target.elts:
                if isinstance(element, astroid.AssignName):
                    target_names.append(element.name)
        elif isinstance(node.target, astroid.AssignName):
            target_names.append(node.target.name)
        return target_names
