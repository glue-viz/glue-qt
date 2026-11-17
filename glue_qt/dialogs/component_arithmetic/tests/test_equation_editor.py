import pytest

from qtpy import QtTest
from qtpy.QtCore import Qt
from glue.core import Data

from ..equation_editor import EquationEditorDialog


class TestEquationEditor:

    def setup_method(self, method):
        self.data = Data(x=[1, 2, 3], y=[3, 4, 5])
        self.dialog = EquationEditorDialog(label='z', data=self.data, equation='')

    def test_empty(self):
        assert not self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == ''

    @pytest.mark.parametrize('expression', ['1', '1 + {x}', '1 * np.sin({y}) + {x}'])
    def test_valid_cases(self, expression):
        self.dialog.expression.insertPlainText(expression)
        assert self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == 'Valid expression'
        self.dialog.ui.button_ok.click()
        assert self.dialog._get_raw_command() == expression

    def test_invalid_syntax(self):
        self.dialog.expression.insertPlainText('1 + {x')
        assert not self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == 'Incomplete or invalid syntax'

    def test_unknown_component(self):
        self.dialog.expression.insertPlainText('1 + {z}')
        assert not self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == 'Invalid component: z'

    def test_undefined_name(self):
        self.dialog.expression.insertPlainText('1 + {x} + abc')
        assert not self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == "name 'abc' is not defined"

    def test_insert_component(self):
        self.dialog.expression.insertPlainText('1 + ')
        self.dialog.button_insert.click()
        assert self.dialog.ui.label_status.text() == 'Valid expression'
        self.dialog.ui.button_ok.click()
        assert self.dialog._get_raw_command() == '1 + {Pixel Axis 0 [x]}'

    def test_nolabel(self):
        self.dialog.ui.text_label.setText('')
        self.dialog.expression.insertPlainText('1 + {x}')
        assert not self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == 'Attribute name not set'

    def test_typing(self):

        # This ensures that the code that highlights syntax gets called,
        # and also ensures we can test undoing.

        chars = (Qt.Key_1, Qt.Key_Space, Qt.Key_Plus, Qt.Key_Space,
                 Qt.Key_BraceLeft, Qt.Key_X, Qt.Key_BraceRight)

        for char in chars:
            QtTest.QTest.keyClick(self.dialog.expression, char)

        assert self.dialog.expression.toPlainText() == '1 + {x}'

        QtTest.QTest.keyClick(self.dialog.expression, Qt.Key_Z, Qt.ControlModifier)

        assert self.dialog.expression.toPlainText() == '1 + {x'

        for i in range(4):
            QtTest.QTest.keyClick(self.dialog.expression, Qt.Key_Z, Qt.ControlModifier)

        assert self.dialog.expression.toPlainText() == '1 '

    def test_cancel(self):
        self.dialog.expression.insertPlainText('1 + {x}')
        assert self.dialog.ui.label_status.text() == 'Valid expression'
        self.dialog.ui.button_cancel.click()
        assert self.dialog.final_expression is None

    def test_not_allowed_by_default(self):

        # Expressions that use something that is not allowed by default can
        # only be accepted once the user has explicitly allowed this.

        checkbox = self.dialog.ui.checkbox_unrestricted
        assert checkbox.isHidden()

        self.dialog.expression.insertPlainText('np.vectorize(abs)({x})')
        assert not self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == 'numpy.vectorize is not allowed in expressions'
        assert not checkbox.isHidden()
        assert not checkbox.isChecked()
        assert self.dialog._get_parsed_command().restricted

        checkbox.setChecked(True)
        assert self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == 'Valid expression'
        assert not self.dialog._get_parsed_command().restricted

        # The choice only applies to the expression for which it was made

        self.dialog.expression.insertPlainText(' + np.vectorize(abs)({y})')
        assert not self.dialog.ui.button_ok.isEnabled()
        assert not checkbox.isHidden()
        assert not checkbox.isChecked()
        assert self.dialog._get_parsed_command().restricted

        checkbox.setChecked(True)
        self.dialog.ui.button_ok.click()
        parsed = self.dialog.get_final_label_and_parsed_command()[1]
        assert not parsed.restricted

        # The checkbox is not shown for expressions that do not need it

        self.dialog.expression.clear()
        self.dialog.expression.insertPlainText('{x} + 1')
        assert self.dialog.ui.button_ok.isEnabled()
        assert checkbox.isHidden()
        assert self.dialog._get_parsed_command().restricted

    def test_not_allowed_by_default_builtin(self):
        # Builtin functions that are not available by default can be allowed
        # but names that do not exist at all cannot.
        self.dialog.expression.insertPlainText("{x} + eval('1 + 1')")
        assert not self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == "name 'eval' is not defined"
        assert not self.dialog.ui.checkbox_unrestricted.isHidden()
        self.dialog.ui.checkbox_unrestricted.setChecked(True)
        assert self.dialog.ui.button_ok.isEnabled()

    def test_not_allowed_not_called_before_allowed(self, tmp_path):
        # Nothing that is not allowed by default should be called until the
        # user has ticked the checkbox.
        filename = tmp_path / 'called'
        self.dialog.expression.insertPlainText(f"{{x}} + open({str(filename)!r}, 'w').write('a')")
        assert not self.dialog.ui.button_ok.isEnabled()
        assert not filename.exists()
        self.dialog.ui.checkbox_unrestricted.setChecked(True)
        assert self.dialog.ui.button_ok.isEnabled()
        assert filename.exists()

    def test_allowed_but_invalid(self):
        # Allowing an expression does not help if it is otherwise invalid
        self.dialog.expression.insertPlainText('np.vectorize(abs)({x}) + abc')
        self.dialog.ui.checkbox_unrestricted.setChecked(True)
        assert not self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == "name 'abc' is not defined"

    def test_initially_allowed(self):
        # When editing an expression that was already allowed, the checkbox
        # should already be ticked.
        dialog = EquationEditorDialog(label='z', data=self.data, restricted=False,
                                      equation='np.vectorize(abs)({x})')
        assert dialog.ui.checkbox_unrestricted.isChecked()
        assert not dialog.ui.checkbox_unrestricted.isHidden()
        assert dialog.ui.button_ok.isEnabled()
        assert not dialog._get_parsed_command().restricted

    @pytest.mark.parametrize(('expression', 'status'),
                             [('(lambda v: v)({x})', 'Lambda is not allowed in expressions'),
                              ('missing_function({x})', "name 'missing_function' is not defined")])
    def test_cannot_be_allowed(self, expression, status):
        # The checkbox is not shown for expressions that would not work even
        # if they were allowed.
        self.dialog.expression.insertPlainText(expression)
        assert not self.dialog.ui.button_ok.isEnabled()
        assert self.dialog.ui.label_status.text() == status
        assert self.dialog.ui.checkbox_unrestricted.isHidden()
