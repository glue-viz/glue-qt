import os

from qtpy import QtWidgets

from echo.qt import autoconnect_callbacks_to_qt
from glue_qt.utils import load_ui


class DendrogramLayerStyleEditor(QtWidgets.QWidget):

    def __init__(self, layer, parent=None):

        super(DendrogramLayerStyleEditor, self).__init__(parent=parent)

        self.ui = load_ui('layer_style_editor.ui', self,
                          directory=os.path.dirname(__file__))

        connect_kwargs = {'alpha': dict(value_range=(0, 1))}

        self._connections = autoconnect_callbacks_to_qt(layer.state, self.ui, connect_kwargs)
