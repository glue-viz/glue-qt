import json

import numpy as np
import pytest
from numpy.testing import assert_equal

from qtpy.QtCore import Qt

from glue.core import Data, ComponentID
from glue.core.parse import ParsedCommand, ParsedComponentLink

from ..application import GlueApplication
from ..unsafe_expressions import UnsafeExpressionsDialog, review_unsafe_expressions


EXPRESSIONS = [dict(expression="{id1} + __import__('math').sqrt(4)",
                    rendered="{x} + __import__('math').sqrt(4)",
                    label='y',
                    reason='Name __import__ is not allowed in expressions'),
               dict(expression="some_function({id1})",
                    rendered="some_function({x})",
                    label='z',
                    reason="name 'some_function' is not defined")]


def make_session(tmp_path, unsafe=True):
    """
    Write a session file with a derived attribute, optionally modifying the
    expression so that it uses something that is harmless but which is not
    allowed in expressions by default.
    """

    data = Data(x=[1, 2, 3], label='data')
    link = ParsedComponentLink(ComponentID('y'),
                               ParsedCommand('{x} + 1', {'x': data.id['x']}))
    data.add_component_link(link)

    app = GlueApplication()
    app.data_collection.append(data)
    filename = str(tmp_path / 'session.glu')
    app.save_session(filename, include_data=True)
    app.close()

    if unsafe:

        with open(filename) as f:
            session = json.load(f)

        def modify(item):
            if isinstance(item, dict):
                if isinstance(item.get('cmd'), str):
                    item['cmd'] = "__import__('math').sqrt(4) + " + item['cmd']
                for value in item.values():
                    modify(value)
            elif isinstance(item, list):
                for value in item:
                    modify(value)

        modify(session)

        with open(filename, 'w') as f:
            json.dump(session, f)

    return filename


def patch_dialog(monkeypatch, action):
    """
    Make the dialog call ``action`` instead of waiting for user input, and
    return the list that the dialogs that are shown are added to.
    """

    dialogs = []

    def exec_(dialog):
        dialogs.append(dialog)
        action(dialog)

    monkeypatch.setattr(UnsafeExpressionsDialog, 'exec_', exec_)

    return dialogs


class TestUnsafeExpressionsDialog:

    def setup_method(self, method):
        self.dialog = UnsafeExpressionsDialog(EXPRESSIONS)

    def teardown_method(self, method):
        self.dialog.close()

    def test_contents(self):
        tree = self.dialog.tree
        assert tree.topLevelItemCount() == 2
        item = tree.topLevelItem(0)
        assert item.checkState(0) == Qt.Unchecked
        assert [item.text(column) for column in range(1, 4)] == [
            'y', "{x} + __import__('math').sqrt(4)",
            'Name __import__ is not allowed in expressions']

    def test_default_is_disallow_all(self):
        assert self.dialog.button_disallow_all.isDefault()
        assert not self.dialog.button_allow_all.isDefault()
        assert not self.dialog.button_allow_selected.isDefault()
        assert self.dialog.allowed is None

    def test_disallow_all(self):
        self.dialog.tree.topLevelItem(0).setCheckState(0, Qt.Checked)
        self.dialog.button_disallow_all.click()
        assert self.dialog.allowed == []

    def test_allow_selected(self):
        assert not self.dialog.button_allow_selected.isEnabled()
        self.dialog.tree.topLevelItem(1).setCheckState(0, Qt.Checked)
        assert self.dialog.button_allow_selected.isEnabled()
        self.dialog.button_allow_selected.click()
        # The expressions as stored in the session file are returned
        assert self.dialog.allowed == ["some_function({id1})"]

    def test_allow_all(self):
        self.dialog.button_allow_all.click()
        assert self.dialog.allowed == [expression['expression'] for expression in EXPRESSIONS]

    def test_cancel(self):
        self.dialog.tree.topLevelItem(0).setCheckState(0, Qt.Checked)
        self.dialog.button_cancel.click()
        assert self.dialog.allowed is None


def test_review_no_unsafe_expressions(tmp_path, monkeypatch):
    filename = make_session(tmp_path, unsafe=False)
    dialogs = patch_dialog(monkeypatch, lambda dialog: dialog.allow_all())
    assert review_unsafe_expressions(filename) == []
    assert dialogs == []


def test_review_unsafe_expressions(tmp_path, monkeypatch):
    filename = make_session(tmp_path)
    dialogs = patch_dialog(monkeypatch, lambda dialog: dialog.allow_all())
    allowed = review_unsafe_expressions(filename)
    assert len(dialogs) == 1
    assert dialogs[0].expressions[0]['label'] == 'y'
    assert dialogs[0].expressions[0]['rendered'] == "__import__('math').sqrt(4) + {x} + 1"
    assert allowed == [dialogs[0].expressions[0]['expression']]


class TestRestoreSession:

    def setup_method(self, method):
        self.app = GlueApplication()

    def teardown_method(self, method):
        self.app.close()

    def test_no_unsafe_expressions(self, tmp_path, monkeypatch):
        filename = make_session(tmp_path, unsafe=False)
        dialogs = patch_dialog(monkeypatch, lambda dialog: dialog.reject())
        app = self.app.restore_session_and_close(filename, warn=False)
        assert dialogs == []
        assert_equal(app.data_collection[0]['y'], [2, 3, 4])
        app.close()

    @pytest.mark.filterwarnings('ignore:The expression')
    def test_disallow(self, tmp_path, monkeypatch):
        filename = make_session(tmp_path)
        dialogs = patch_dialog(monkeypatch, lambda dialog: dialog.disallow_all())
        app = self.app.restore_session_and_close(filename, warn=False)
        assert len(dialogs) == 1
        assert_equal(app.data_collection[0]['y'], [np.nan, np.nan, np.nan])
        app.close()

    def test_allow(self, tmp_path, monkeypatch):
        filename = make_session(tmp_path)
        dialogs = patch_dialog(monkeypatch, lambda dialog: dialog.allow_all())
        app = self.app.restore_session_and_close(filename, warn=False)
        assert len(dialogs) == 1
        assert_equal(app.data_collection[0]['y'], [4, 5, 6])
        app.close()

    def test_cancel(self, tmp_path, monkeypatch):
        filename = make_session(tmp_path)
        dialogs = patch_dialog(monkeypatch, lambda dialog: dialog.reject())
        assert self.app.restore_session_and_close(filename, warn=False) is None
        assert len(dialogs) == 1
        # The existing application is unaffected
        assert len(self.app.data_collection) == 0


def test_restore_session_allowed_expressions(tmp_path):
    filename = make_session(tmp_path)
    with pytest.warns(UserWarning, match='will not be evaluated'):
        app = GlueApplication.restore_session(filename, show=False)
    assert_equal(app.data_collection[0]['y'], [np.nan, np.nan, np.nan])
    app.close()
