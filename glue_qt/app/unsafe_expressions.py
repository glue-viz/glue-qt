from qtpy import QtWidgets
from qtpy.QtCore import Qt

from glue.core.state import find_unsafe_expressions

__all__ = ['UnsafeExpressionsDialog', 'review_unsafe_expressions']


class UnsafeExpressionsDialog(QtWidgets.QDialog):
    """
    A dialog that lists the expressions in a session file that use something
    that glue does not allow in expressions by default, and lets the user
    choose which of these to allow.

    After the dialog has been closed, the ``allowed`` attribute is the list
    of expressions the user chose to allow (which can be empty), or `None`
    if the user cancelled.

    Parameters
    ----------
    expressions : list of dict
        The expressions, as returned by
        :func:`glue.core.state.find_unsafe_expressions`.
    """

    def __init__(self, expressions, parent=None):

        super().__init__(parent=parent)

        self.setWindowTitle("Potentially unsafe expressions")

        self.expressions = expressions
        self.allowed = None

        layout = QtWidgets.QVBoxLayout(self)

        if len(expressions) == 1:
            intro = "This session file contains an expression"
        else:
            intro = f"This session file contains {len(expressions)} expressions"

        label = QtWidgets.QLabel(
            f"<b>{intro} that glue cannot verify as safe.</b><br><br>"
            "Expressions that define attributes can normally only use a "
            "restricted set of functions. The expressions below use something "
            "else, and could run arbitrary code on your computer if you allow "
            "them, so only do so if you trust the source of this file and "
            "have checked the expressions.<br><br>"
            "The attributes for expressions that are not allowed will be "
            "empty (filled with NaN values).")
        label.setWordWrap(True)
        layout.addWidget(label)

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(["Allow", "Attribute", "Expression", "Reason"])
        self.tree.setRootIsDecorated(False)
        for expression in expressions:
            item = QtWidgets.QTreeWidgetItem(["", expression['label'] or "",
                                              expression['rendered'], expression['reason']])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Unchecked)
            for column in (2, 3):
                item.setToolTip(column, item.text(column))
            self.tree.addTopLevelItem(item)
        for column in range(4):
            self.tree.resizeColumnToContents(column)
        layout.addWidget(self.tree)

        self.button_box = QtWidgets.QDialogButtonBox()
        self.button_disallow_all = self.button_box.addButton(
            "Disallow all", QtWidgets.QDialogButtonBox.AcceptRole)
        self.button_allow_selected = self.button_box.addButton(
            "Allow selected", QtWidgets.QDialogButtonBox.ActionRole)
        self.button_allow_all = self.button_box.addButton(
            "Allow all", QtWidgets.QDialogButtonBox.ActionRole)
        self.button_cancel = self.button_box.addButton(QtWidgets.QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)

        # Disallowing everything is the default, so that nothing is allowed
        # if the user presses enter without reading the message.
        self.button_disallow_all.setDefault(True)
        self.button_disallow_all.setAutoDefault(True)
        for button in (self.button_allow_selected, self.button_allow_all, self.button_cancel):
            button.setAutoDefault(False)

        self.button_disallow_all.clicked.connect(self.disallow_all)
        self.button_allow_selected.clicked.connect(self.allow_selected)
        self.button_allow_all.clicked.connect(self.allow_all)
        self.button_cancel.clicked.connect(self.reject)

        self.tree.itemChanged.connect(self._update_buttons)
        self._update_buttons()

        self.resize(800, 400)

    def _selected(self):
        return [expression['expression']
                for index, expression in enumerate(self.expressions)
                if self.tree.topLevelItem(index).checkState(0) == Qt.Checked]

    def _update_buttons(self, *args):
        self.button_allow_selected.setEnabled(len(self._selected()) > 0)

    def disallow_all(self):
        self.allowed = []
        self.accept()

    def allow_selected(self):
        self.allowed = self._selected()
        self.accept()

    def allow_all(self):
        self.allowed = [expression['expression'] for expression in self.expressions]
        self.accept()

    def reject(self):
        self.allowed = None
        super().reject()


def review_unsafe_expressions(path, parent=None):
    """
    Check whether a session file contains expressions that glue does not
    evaluate by default, and if so ask the user which of these to allow.

    Parameters
    ----------
    path : str
        The session file.

    Returns
    -------
    allowed : list of str or None
        The expressions the user chose to allow, which is an empty list if
        there are no such expressions in the session file or if the user
        chose not to allow any of them, or `None` if the user cancelled.
    """
    expressions = find_unsafe_expressions(path)
    if len(expressions) == 0:
        return []
    dialog = UnsafeExpressionsDialog(expressions, parent=parent)
    dialog.exec_()
    return dialog.allowed
