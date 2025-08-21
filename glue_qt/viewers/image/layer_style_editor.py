import os

from qtpy import QtWidgets

from echo.qt import autoconnect_callbacks_to_qt
from glue_qt.utils import load_ui


class ImageLayerStyleEditor(QtWidgets.QWidget):

    def __init__(self, layer, parent=None):

        super(ImageLayerStyleEditor, self).__init__(parent=parent)

        self.ui = load_ui('layer_style_editor.ui', self,
                          directory=os.path.dirname(__file__))

        connect_kwargs = {'alpha': dict(value_range=(0, 1)),
                          'contrast': dict(value_range=(0.1, 10), log=True),
                          'bias': dict(value_range=(1.5, -0.5))}

        self._connections = autoconnect_callbacks_to_qt(layer.state, self.ui, connect_kwargs)

        layer._viewer_state.add_callback('color_mode', self._update_color_mode)

        self._update_color_mode(layer._viewer_state.color_mode)

        self.ui.bool_global_sync.setToolTip('Whether to sync the color and transparency with other viewers')

    def _update_color_mode(self, color_mode):
        if color_mode == 'Colormaps':
            self.ui.color_color.hide()
            self.ui.cmap_cmap.show()
        else:
            self.ui.color_color.show()
            self.ui.cmap_cmap.hide()
