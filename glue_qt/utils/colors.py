import numpy as np
from matplotlib.colors import ColorConverter

from glue import config
from qtpy import QtCore, QtWidgets, QtGui
from echo import add_callback
from glue.utils import nonpartial
from glue_qt.utils.widget_properties import WidgetProperty

from matplotlib import cm

__all__ = ['mpl_to_qt_color', 'qt_to_mpl_color', 'cmap2pixmap',
           'tint_pixmap', 'QColorBox', 'ColorProperty', 'connect_color',
           'QColormapCombo']


def mpl_to_qt_color(color, alpha=None):
    """
    Convert a matplotlib color string into a Qt QColor object

    Parameters
    ----------
    color : str
       A color specification that matplotlib understands
    alpha : float
        Optional opacity. Float in range [0,1]

    Returns
    -------
    qcolor : ``QColor``
        A QColor object representing the converted color
    """
    if color in [None, 'none', 'None']:
        return QtGui.QColor(0, 0, 0, 0)

    cc = ColorConverter()
    r, g, b, a = cc.to_rgba(color)
    if alpha is not None:
        a = alpha
    return QtGui.QColor(int(r * 255), int(g * 255), int(b * 255), int(a * 255))


def qt_to_mpl_color(qcolor):
    """
    Convert a QColor object into a string that matplotlib understands

    Note: This ignores opacity

    Parameters
    ----------
    qcolor : ``QColor``
        The Qt color

    Returns
    -------
    color : str
        A hex string describing that color
    """
    hexid = qcolor.name()
    return str(hexid)


def cmap2pixmap(cmap, steps=50, size=(100, 100)):
    """
    Convert a matplotlib colormap into a QPixmap

    Parameters
    ----------
    cmap : :class:`matplotlib.colors.Colormap`
        The colormap to use
    steps : int
        The number of color steps in the output. Default=50

    Returns
    -------
    pixmap : ``QPixmap``
        The QPixmap instance
    """
    sm = cm.ScalarMappable(cmap=cmap)
    sm.norm.vmin = 0.0
    sm.norm.vmax = 1.0
    inds = np.linspace(0, 1, steps)
    rgbas = sm.to_rgba(inds)
    rgbas = [QtGui.QColor(int(r * 255), int(g * 255),
                          int(b * 255), int(a * 255)).rgba() for r, g, b, a in rgbas]
    im = QtGui.QImage(steps, 1, QtGui.QImage.Format_Indexed8)
    im.setColorTable(rgbas)
    for i in range(steps):
        im.setPixel(i, 0, i)
    im = im.scaled(*size)
    pm = QtGui.QPixmap.fromImage(im)
    return pm


def tint_pixmap(bm, color):
    """
    Re-color a monochrome pixmap object using `color`

    Parameters
    ----------
    bm : ``QBitmap``
        The Pixmap object
    color : ``QColor``
        The Qt color

    Returns
    -------
    pixmap : ``QPixmap``
        The new pixmap
    """
    if bm.depth() != 1:
        raise TypeError("Input pixmap must have a depth of 1: %i" % bm.depth())

    image = bm.toImage()
    image.setColor(1, color.rgba())
    image.setColor(0, QtGui.QColor(0, 0, 0, 0).rgba())

    result = QtGui.QPixmap.fromImage(image)
    return result


class ColorProperty(WidgetProperty):

    def getter(self, widget):
        return widget.color()

    def setter(self, widget, value):
        widget.setColor(value)


def connect_color(client, prop, widget):

    def update_widget(text):
        widget.setColor(text)

    def update_prop():
        setattr(client, prop, widget.color())

    add_callback(client, prop, update_widget)
    widget.colorChanged.connect(nonpartial(update_prop))
    update_widget(getattr(client, prop))


from echo.qt.autoconnect import HANDLERS
HANDLERS['color'] = connect_color


class QColorBox(QtWidgets.QLabel):

    mousePressed = QtCore.Signal()
    colorChanged = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(QColorBox, self).__init__(*args, **kwargs)
        self.mousePressed.connect(nonpartial(self.query_color))
        self.colorChanged.connect(nonpartial(self.on_color_change))
        self.setColor("#000000")

    def mousePressEvent(self, event):
        self.mousePressed.emit()
        event.accept()

    def query_color(self):
        color = QtWidgets.QColorDialog.getColor(self._qcolor, parent=self)
        if color.isValid():
            self.setColor(qt_to_mpl_color(color))

    def setColor(self, color):
        self._color = color
        self.colorChanged.emit()

    def color(self):
        return self._color

    def on_color_change(self):
        self._qcolor = mpl_to_qt_color(self.color())
        image = QtGui.QImage(70, 22, QtGui.QImage.Format_RGB32)
        try:
            image.fill(self._qcolor)
        except TypeError:
            # PySide and old versions of PyQt require a RGBA integer
            image.fill(self._qcolor.rgba())
        pixmap = QtGui.QPixmap.fromImage(image)
        self.setPixmap(pixmap)


from echo.qt.connect import UserDataWrapper


class QColormapCombo(QtWidgets.QComboBox):

    def __init__(self, *args, **kwargs):
        super(QColormapCombo, self).__init__(*args, **kwargs)
        for label, cmap in config.colormaps:
            self.addItem(label, userData=UserDataWrapper(cmap))
        self._update_icons()

    def refresh_options(self, colormaps=None):
        if colormaps is None:
            self.clear()
            for label, cmap in config.colormaps:
                self.addItem(label, userData=UserDataWrapper(cmap))
            self._update_icons()
        else:
            self.clear()
            for label, cmap in colormaps:
                self.addItem(label, userData=UserDataWrapper(cmap))
            self._update_icons()

    def _update_icons(self):
        self.setIconSize(QtCore.QSize(self.width(), 15))
        for index in range(self.count()):
            cmap = self.itemData(index).data
            icon = QtGui.QIcon(cmap2pixmap(cmap, size=(self.width(), 15), steps=200))
            self.setItemIcon(index, icon)

    def resizeEvent(self, *args, **kwargs):
        super(QColormapCombo, self).resizeEvent(*args, **kwargs)
        self._update_icons()


class QColormapWidget(QtWidgets.QWidget):

    changed = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(QColormapWidget, self).__init__(*args, **kwargs)
        layout = QtWidgets.QHBoxLayout()
        self.cmap_combo = QColormapCombo()
        self.cmap_button = QtWidgets.QPushButton(text="⇄")
        self.cmap_button.setCheckable(True)
        self.cmap_button.setMaximumWidth(25)
        self.cmap_button.adjustSize()
        layout.addWidget(self.cmap_combo)
        layout.addWidget(self.cmap_button)
        self.setLayout(layout)

        self.cmap_button.toggled.connect(self._update_from_checkbox)
        self.cmap_combo.currentIndexChanged.connect(self._update_from_combo)

    def value(self):
        return self.itemData(self.cmap_combo.currentIndex(), reverse=self.cmap_button.isChecked()).data

    def isChecked(self):
        return self.cmap_button.isChecked()

    def _update_from_checkbox(self, value):
        self.changed.emit()

    def _update_from_combo(self, index):
        self.cmap_combo.setCurrentIndex(index)

    def set(self, index, reverse):
        with QtCore.QSignalBlocker(self.cmap_combo), QtCore.QSignalBlocker(self.cmap_button):
            self.cmap_combo.setCurrentIndex(index)
            self.cmap_button.setChecked(reverse)
        self.changed.emit()

    def count(self):
        return self.cmap_combo.count()

    def itemData(self, index, reverse=False):
        wrapper = self.cmap_combo.itemData(index)
        data = wrapper.data
        if reverse:
            data = data.reversed()
        return UserDataWrapper(data=data)


def _find_cmap_combo_data(widget, value):
    """
    Returns the index in a combo box where itemData == value

    Raises a ValueError if data is not found
    """
    # Here we check that the result is True, because some classes may overload
    # == and return other kinds of objects whether true or false.
    for idx in range(widget.count()):
        if (item_data := widget.itemData(idx)) is not None:
            if isinstance(item_data, UserDataWrapper):
                data = item_data.data
            else:
                data = item_data
            if data is value or (data == value) is True:
                return idx, False 
            data = data.reversed()
            if data is value or (data == value) is True:
                return idx, True
    else:
        raise ValueError("%s not found in combo box" % (value,))


def connect_color_combo(client, prop, widget):

    def update_widget(item):
        try:
            idx, reverse = _find_cmap_combo_data(widget, item)
        except ValueError:
            if item is None:
                idx, reverse = -1, False
            else:
                raise
        widget.set(idx, reverse)

    def update_prop():
        setattr(client, prop, widget.value())

    add_callback(client, prop, update_widget)
    widget.changed.connect(nonpartial(update_prop))
    update_widget(getattr(client, prop))


HANDLERS['cmap'] = connect_color_combo

if __name__ == "__main__":

    from glue_qt.utils import get_qapp

    app = get_qapp()

    label = QColorBox()
    label.resize(100, 100)
    label.show()
    label.raise_()
    app.exec_()
