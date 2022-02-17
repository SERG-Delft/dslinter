"""Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""
from typing import List
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class HyperparameterChecker(BaseChecker):
    """Hyperparameter checker checks whether all hyperparameters for learning algorithms are set."""

    __implements__ = IAstroidChecker

    # Main hyperparameters of learning algorithms, as defined in research.
    # Sources:
    # 1. Probst, P., Boulesteix, A. L., & Bischl, B. (2019). Tunability: Importance of
    #   Hyperparameters of Machine Learning Algorithms. Journal of Machine Learning Research,
    #   20(53), 1-32.
    # 2. van Rijn, J. N., & Hutter, F. (2018, July). Hyperparameter importance across datasets.
    #   In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery &
    #   Data Mining (pp. 2367-2376).


    @staticmethod
    def _has_keywords(keywords: List[astroid.Keyword], keywords_goal: List[str]) -> bool:
        """
        Check if a list of keywords contains certain keywords.

        :param keywords: List of keywords.
        :param keywords_goal: Name of the keywords which are checked against.
        :return: True if keywords are present, False if they are not.
        """
        if keywords is None:
            return False

        found = 0
        for keyword in keywords:
            if keyword.arg in keywords_goal:
                found += 1

        return found == len(keywords_goal)
