import sys
from .qglue import qglue

__all__ = ['qglue']

# In PyQt 5.5+, PyQt overrides the default exception catching and fatally
# crashes the Qt application without printing out any details about the error.
# Below we revert the exception hook to the original Python one. Note that we
# can't just do sys.excepthook = sys.__excepthook__ otherwise PyQt will detect
# the default excepthook is in place and override it.


def handle_exception(exc_type, exc_value, exc_traceback):
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = handle_exception
