"""
Jesse Averbukh
October 12, 2017
The file where keyboard shortcuts are created. In the future, many of these
values will be populated using a GUI.
"""

from qtpy import QtCore
from glue_qt.config import keyboard_shortcut
from glue.config import viewer_tool
from glue_qt.viewers.scatter.data_viewer import ScatterViewer
from glue_qt.viewers.histogram.data_viewer import HistogramViewer
from glue_qt.viewers.image.data_viewer import ImageViewer
from glue_qt.viewers.table.data_viewer import DataTableModel


def check_duplicate_shortcut(key_shortcut):
    """
    Checks to make sure that a key_shortcut is not already used within the
    glue application somewhere else.
    This will become simpler with the implementation of a GUI
    """
    list_of_shortcuts = []
    for k in viewer_tool.__iter__():
        list_of_shortcuts.append(viewer_tool.members[k].shortcut)

    if key_shortcut in list_of_shortcuts:
        return True
    return False


@keyboard_shortcut(QtCore.Key_Tab, [ImageViewer, HistogramViewer, ScatterViewer, DataTableModel])
def cycle_through_windows(session):
    """
    Cycle through all active windows within the current tab
    """
    if check_duplicate_shortcut("tab"):
        return

    return session.application.current_tab.activateNextSubWindow()


@keyboard_shortcut(QtCore.Key_Backspace, [ImageViewer, HistogramViewer, ScatterViewer, DataTableModel])
def delete_current_window(session):
    """
    Deletes the currently active window
    """
    if check_duplicate_shortcut("backspace"):
        return

    return session.application._viewer_in_focus.close(warn=True)
