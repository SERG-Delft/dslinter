from __future__ import absolute_import

import sys

from dslinter import plugin

if sys.version_info < (3,):
    raise DeprecationWarning("Python 2 is not supported. Please migrate to Python 3!")

register = plugin.register
