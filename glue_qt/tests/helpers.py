# Define decorators that can be used for pytest tests

import pytest

from glue.tests.helpers import make_skipper

PYQT5_INSTALLED, requires_pyqt5 = make_skipper('PyQt5')
PYQT6_INSTALLED, requires_pyqt6 = make_skipper('PyQt6')
PYSIDE2_INSTALLED, requires_pyside2 = make_skipper('PySide2')
PYSIDE6_INSTALLED, requires_pyside6 = make_skipper('PySide6')

PYQT_INSTALLED = PYQT5_INSTALLED or PYQT6_INSTALLED
PYSIDE_INSTALLED = PYSIDE2_INSTALLED or PYSIDE6_INSTALLED
QT_INSTALLED = PYQT_INSTALLED or PYSIDE_INSTALLED

requires_pyqt = pytest.mark.skipif(str(not PYQT_INSTALLED),
                                   reason='An installation of PyQt is required')

requires_pyside = pytest.mark.skipif(str(not PYSIDE_INSTALLED),
                                     reason='An installation of PySide is required')

requires_qt = pytest.mark.skipif(str(not QT_INSTALLED),
                                 reason='An installation of Qt is required')

PYQT_GT_59, _ = make_skipper('PyQt5', version='5.10')

requires_pyqt_gt_59_or_pyside = pytest.mark.skipif(str(not (PYQT_GT_59 or PYQT6_INSTALLED or
                                                            PYSIDE_INSTALLED)),
                                                   reason='Requires PyQt > 5.9 or PySide2/6')
