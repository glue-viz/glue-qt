"""
Qt-specific bindings for the path slicer tool.

The data model (one trace per Enter; create or update individually)
and the matplotlib overlay drawing live in
:mod:`glue.plugins.tools.path_slicer.matplotlib_mode`. This module
adds the Qt dropdown menu on the slice tool's toolbar button: each
menu rebuilds itself with the current traces on ``aboutToShow``;
hovering an entry previews the corresponding path on the source
viewer (alpha bump on the overlay artist); selecting commits the
choice as the next-Enter target.
"""

from qtpy import QtCore, QtWidgets

from glue.config import viewer_tool
from glue.plugins.tools.path_slicer.matplotlib_mode import (
    BasePathSlicerCrosshairMode, BasePathSlicerMode)

from glue_qt.viewers.image import ImageViewer


__all__ = ['PathSlicerMode', 'PathSlicerCrosshairMode']


@viewer_tool
class PathSlicerMode(BasePathSlicerMode):

    tool_id = 'slice'
    slice_viewer_cls = ImageViewer

    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        # The toolbar's button isn't created until after Tool.__init__
        # returns (the toolbar builds the action + widget around it),
        # so defer the menu wiring.
        QtCore.QTimer.singleShot(0, self._install_dropdown)

    def _install_dropdown(self):
        toolbar = self.viewer.toolbar
        action = toolbar.actions.get(self.tool_id)
        if action is None:
            return
        button = toolbar.widgetForAction(action)
        if button is None:
            return
        self._menu = _TargetMenu(self, parent=button)
        button.setMenu(self._menu)
        # MenuButtonPopup: clicking the icon activates the tool with
        # the current target; clicking the arrow shows the menu.
        button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)


class _TargetMenu(QtWidgets.QMenu):
    """Dynamic popup menu that rebuilds with the tool's current traces
    on every ``aboutToShow``. Hovering an entry calls
    ``tool.hover_preview`` for a non-committing highlight; selecting
    one calls ``tool.set_target``."""

    def __init__(self, tool, parent=None):
        super().__init__(parent)
        self._tool = tool
        self.aboutToShow.connect(self._rebuild)
        self.aboutToHide.connect(self._tool._refresh_overlays)

    def _rebuild(self):
        self.clear()
        for label, target in self._tool.menu_entries():
            action = self.addAction(label)
            if target is self._tool._target_trace:
                action.setCheckable(True)
                action.setChecked(True)
            action.triggered.connect(
                lambda _checked=False, t=target: self._tool.set_target(t))
            action.hovered.connect(
                lambda t=target: self._tool.hover_preview(t))


@viewer_tool
class PathSlicerCrosshairMode(BasePathSlicerCrosshairMode):
    tool_id = 'path:crosshair'


def setup():
    ImageViewer.tools.append('slice')
    ImageViewer.tools.append('path:crosshair')
