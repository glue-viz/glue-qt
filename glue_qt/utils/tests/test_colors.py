from unittest.mock import MagicMock

from echo import CallbackProperty
from glue.config import colormaps
from qtpy import QtGui

from ..colors import qt_to_mpl_color, QColorBox, connect_color, QColormapCombo, connect_colormap_widget, QColormapWidget


def test_colors():
    assert qt_to_mpl_color(QtGui.QColor(255, 0, 0)) == '#ff0000'
    assert qt_to_mpl_color(QtGui.QColor(255, 255, 255)) == '#ffffff'


# TODO: add a test for the other way around

# TODO: add a test for cmap2pixmap

# TODO: add a test for tint_pixmap

def test_color_box():

    func = MagicMock()

    label = QColorBox()
    label.resize(100, 100)
    label.colorChanged.connect(func)
    label.setColor('#472822')

    assert func.call_count == 1


def test_connect_color():

    class FakeClass(object):
        color = CallbackProperty()

    c = FakeClass()

    label = QColorBox()

    connect_color(c, 'color', label)

    label.setColor('#472822')

    assert c.color == '#472822'

    c.color = '#012345'

    assert label.color() == '#012345'


def test_colormap_combo():

    combo = QColormapCombo()


def test_colormap_widget():

    widget = QColormapWidget()


def test_colormap_widget_value():

    class FakeClass(object):
        cmap = CallbackProperty()

    c = FakeClass()
    widget = QColormapWidget()

    connect_colormap_widget(c, 'cmap', widget)

    cmap0 = colormaps.members[0][1]

    widget.set(0, True)
    assert c.cmap == cmap0.reversed()

    cmap1 = colormaps.members[1][1]
    widget.set(1, True)
    assert c.cmap == cmap1.reversed()

    widget.set(1, False)
    assert c.cmap == cmap1

    c.cmap = cmap0
    assert widget.cmap_combo.currentIndex() == 0
    assert not widget.cmap_button.isChecked()
    assert widget.value() == cmap0

    c.cmap = cmap1.reversed()
    assert widget.cmap_combo.currentIndex() == 1
    assert widget.cmap_button.isChecked()
    assert widget.value() == cmap1.reversed()
