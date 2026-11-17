import os
import re
from collections import deque, OrderedDict

from qtpy import QtWidgets, QtCore
from qtpy.QtCore import Qt

from echo import SelectionCallbackProperty
from echo.qt import connect_combo_selection
from glue.core.parse import InvalidTagError, ParsedCommand, TAG_RE
from glue.core.safe_expression import UnsafeExpressionError, build_namespace
from glue_qt.utils import load_ui, CompletionTextEdit

__all__ = ['EquationEditorDialog']


class ColorizedCompletionTextEdit(CompletionTextEdit):

    updated = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(ColorizedCompletionTextEdit, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignLeft)
        self.setUndoRedoEnabled(False)
        self._undo_stack = deque(maxlen=100)
        self._redo_stack = deque(maxlen=100)

    def insertPlainText(self, *args):
        super(ColorizedCompletionTextEdit, self).insertPlainText(*args)
        self.reformat_text()
        self.updated.emit()
        self.setAlignment(Qt.AlignLeft)

    def keyReleaseEvent(self, event):
        super(ColorizedCompletionTextEdit, self).keyReleaseEvent(event)
        self.reformat_text()
        self.updated.emit()

    def keyPressEvent(self, event):
        super(ColorizedCompletionTextEdit, self).keyPressEvent(event)
        # NOTE: We use == here instead of & for the modifiers because we don't
        # want to catch e.g. control-shift-z or other combinations.
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:
            if len(self._undo_stack) > 1:
                self._undo_stack.pop()
                self.setHtml(self._undo_stack[-1])
                text = self.toPlainText()
                tc = self.textCursor()
                tc.setPosition(len(text))
                self.setTextCursor(tc)
                self._cache = self._undo_stack[-1]
                self.updated.emit()

    def reformat_text(self):

        # If the text hasn't changed, no need to reformat
        if self.toPlainText() == getattr(self, '_cache', None):
            return

        # Here every time a key is released, we re-colorize the expression.
        # We show valid components in blue, and invalid ones in red. We
        # recognized components because they contain a ":" which is not valid
        # Python syntax (except if one considers lambda functions, but we can
        # probably ignore that here)
        text = self.toPlainText()

        # We need to be careful with < and > otherwise they get erased
        text = text.replace('<', '&lt;').replace('>', '&gt;')

        def format_components(m):
            component = m.group(0)
            if component in self.word_list:
                return "<font color='#0072B2'><b>" + component + "</b></font>"
            else:
                return "<font color='#D55E00'><b>" + component + "</b></font>"

        html = TAG_RE.sub(format_components, text)

        tc = self.textCursor()
        pos = tc.position()

        self._undo_stack.append(html)
        self.setHtml(html)

        # Sometimes the HTML gets rid of double spaces so we have to make
        # sure the position isn't greater than the text length.
        text = self.toPlainText()
        pos = min(pos, len(text))

        tc.setPosition(pos)
        self.setTextCursor(tc)

        self._cache = self.toPlainText()


class EquationEditorDialog(QtWidgets.QDialog):

    tip_text = ("<b>Note:</b> Attribute names in the expression should be surrounded "
                "by {{ }} brackets (e.g. {{{example}}}), and you can use "
                "Numpy functions using np.&lt;function&gt;, as well as any "
                "other function defined in your config.py file.<br><br>"
                "<b>Example expressions:</b><br><br>"
                "  - Subtract 10 from '{example}': {{{example}}} - 10<br>"
                "  - Scale '{example}' to [0:1]: ({{{example}}} - np.min({{{example}}})) / np.ptp({{{example}}})<br>"
                "  - Multiply '{example}' by pi: {{{example}}} * np.pi<br>"
                "  - Use masking: {{{example}}} * ({{{example}}} &lt; 1)<br>")

    placeholder_text = ("Type any mathematical expression here - "
                        "you can include attribute names from the "
                        "drop-down below by selecting them and "
                        "clicking 'Insert'. See below for examples "
                        "of valid expressions")

    attribute = SelectionCallbackProperty()

    def __init__(self, label=None, data=None, equation=None, references=None,
                 restricted=True, parent=None):

        super(EquationEditorDialog, self).__init__(parent=parent)

        self.ui = load_ui('equation_editor.ui', self,
                          directory=os.path.dirname(__file__))

        # Get mapping from label to component ID
        if references is not None:
            self.references = references
        elif data is not None:
            self.references = OrderedDict()
            for cid in data.coordinate_components + data.main_components:
                self.references[cid.label] = cid

        example = sorted(self.references, key=len)[0]

        self.ui.text_label.setPlaceholderText("New attribute name")
        self.ui.expression.setPlaceholderText(self.placeholder_text.format(example=example))

        self.ui.label.setText(self.tip_text.format(example=example))

        if label is not None:
            self.ui.text_label.setText(label)

        self.ui.text_label.textChanged.connect(self._update_status)

        # Populate component combo
        EquationEditorDialog.attribute.set_choices(self, list(self.references))
        self._connection = connect_combo_selection(self, 'attribute', self.ui.combosel_component)

        # Set up labels for auto-completion
        labels = ['{' + l + '}' for l in self.references]
        self.ui.expression.set_word_list(labels)

        if equation is not None:
            self.ui.expression.insertPlainText(equation)

        # The checkbox to allow the expression to use things that are not
        # allowed by default is only shown when the expression needs it, and
        # only applies to the expression for which it was ticked.
        self._unrestricted_command = None
        self.ui.checkbox_unrestricted.hide()
        if not restricted:
            self._unrestricted_command = self._get_raw_command()
            self.ui.checkbox_unrestricted.setChecked(True)
        self.ui.checkbox_unrestricted.toggled.connect(self._unrestricted_toggled)

        self.ui.button_ok.clicked.connect(self.accept)
        self.ui.button_cancel.clicked.connect(self.reject)

        self.ui.button_insert.clicked.connect(self._insert_component)

        self.ui.expression.updated.connect(self._update_status)
        self._update_status()

    def _insert_component(self):
        label = self.attribute
        self.expression.insertPlainText('{' + label + '}')

    def _unrestricted_toggled(self, checked):
        self._unrestricted_command = self._get_raw_command() if checked else None
        self._update_status()

    @property
    def _unrestricted(self):
        return (self.ui.checkbox_unrestricted.isChecked() and
                self._unrestricted_command == self._get_raw_command())

    def _can_be_allowed(self, exc):
        # Whether an error from evaluating the expression is due to the
        # expression using something that is not allowed by default but
        # that would be available if the user chooses to allow it.
        if isinstance(exc, UnsafeExpressionError):
            return True
        if isinstance(exc, NameError):
            from glue import env
            match = re.match(r"name '(\w+)' is not defined", str(exc))
            name = exc.name or (match.group(1) if match else None)
            return name in build_namespace(env, restricted=False)
        return False

    def _set_status(self, text, color=None, ok=False, can_be_allowed=False):
        self.ui.label_status.setStyleSheet('' if color is None else f'color: {color}')
        self.ui.label_status.setText(text)
        self.ui.button_ok.setEnabled(ok)
        self.ui.checkbox_unrestricted.setVisible(can_be_allowed)

    def _update_status(self):

        # The choice to allow an expression only applies to the expression
        # for which it was made, so we reset it if the expression changes.
        if self.ui.checkbox_unrestricted.isChecked() and not self._unrestricted:
            self.ui.checkbox_unrestricted.blockSignals(True)
            self.ui.checkbox_unrestricted.setChecked(False)
            self.ui.checkbox_unrestricted.blockSignals(False)
            self._unrestricted_command = None

        state = self.ui.text_label.text(), self._get_raw_command(), self._unrestricted

        # If nothing has changed, no need to check again
        if getattr(self, '_cache', None) == state:
            return

        self._cache = state

        if self._get_raw_command() == "":
            self._set_status("")
            return

        try:
            # We always first check the expression with only what is allowed
            # by default, so that nothing else is called unless the user has
            # explicitly chosen to allow this.
            ParsedCommand(self._get_raw_command(), self.references).evaluate_test()
        except SyntaxError:
            self._set_status("Incomplete or invalid syntax", color='red')
            return
        except InvalidTagError as exc:
            self._set_status("Invalid component: {0}".format(exc.tag), color='red')
            return
        except Exception as exc:
            if not self._can_be_allowed(exc):
                self._set_status(str(exc), color='red')
                return
            if not self._unrestricted:
                self._set_status(str(exc), color='darkorange', can_be_allowed=True)
                return
            try:
                self._get_parsed_command().evaluate_test()
            except Exception as exc:
                self._set_status(str(exc), color='red', can_be_allowed=True)
                return
            can_be_allowed = True
        else:
            can_be_allowed = False

        if self.ui.text_label.text() == "":
            self._set_status("Attribute name not set", color='red', can_be_allowed=can_be_allowed)
        else:
            self._set_status("Valid expression", color='green', ok=True, can_be_allowed=can_be_allowed)

    def _get_raw_command(self):
        return str(self.ui.expression.toPlainText())

    def _get_parsed_command(self):
        expression = self._get_raw_command()
        parsed = ParsedCommand(expression, self.references)
        parsed.restricted = not self._unrestricted
        return parsed

    def get_final_label_and_parsed_command(self):
        return self.ui.text_label.text(), self._get_parsed_command()

    def accept(self):
        self.final_expression = self._get_parsed_command()._cmd
        super(EquationEditorDialog, self).accept()

    def reject(self):
        self.final_expression = None
        super(EquationEditorDialog, self).reject()


if __name__ == "__main__":  # pragma: nocover

    from glue_qt.utils import get_qapp

    app = get_qapp()

    from glue.core.data import Data
    d = Data(label='test1', x=[1, 2, 3], y=[2, 3, 4], z=[3, 4, 5])
    widget = EquationEditorDialog(data=d, equation='')
    widget.exec_()
