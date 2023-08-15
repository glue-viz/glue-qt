import pytest

from glue.tests.helpers import PYQT5_INSTALLED, PYQT6_INSTALLED, PYSIDE2_INSTALLED, PYSIDE6_INSTALLED

requires_pyqt = pytest.mark.skipif(str(not PYQT5_INSTALLED and not PYQT6_INSTALLED),
                                   reason='An installation of PyQt is required')

requires_pyside = pytest.mark.skipif(str(not PYSIDE2_INSTALLED and not PYSIDE6_INSTALLED),
                                     reason='An installation of PySide is required')
