# pylint: disable=I0011,W0613,W0201,W0212,E1101,E1103

import pytest
from itertools import product
from glue.config import viewer_tool
from glue_qt.viewers.common.data_viewer import DataViewer
from glue.viewers.common.tool import SimpleToolMenu, Tool
from glue_qt.viewers.common.toolbar import BasicToolbar
from glue.core.tests.util import simple_session

from qtpy.QtWidgets import QToolButton


@viewer_tool
class ExampleTool1(Tool):

    tool_id = 'TEST1'
    tool_tip = 'tes1'
    icon = 'glue_square'
    shortcut = 'A'


@viewer_tool
class ExampleTool2(Tool):

    tool_id = 'TEST2'
    tool_tip = 'tes2'
    icon = 'glue_square'
    shortcut = 'A'


class ExampleViewer2(DataViewer):

    _toolbar_cls = BasicToolbar
    tools = ['TEST1', 'TEST2']

    def __init__(self, session, parent=None):
        super(ExampleViewer2, self).__init__(session, parent=parent)


@viewer_tool
class ExampleTool3(SimpleToolMenu):

    tool_id = "TEST3"
    tool_tip = 'tes3'
    icon = 'glue_square'
    shortcut = '3'


@viewer_tool
class ExampleTool3A(Tool):

    tool_id = 'TEST3A'
    tool_tip = 'tes3a'
    icon = 'glue_square'
    shortcut = 'C'


@viewer_tool
class ExampleTool3B(Tool):

    tool_id = 'TEST3B'
    tool_tip = 'tes3b'
    icon = 'glue_square'
    shortcut = 'D'


class ExampleViewer3(DataViewer):

    _toolbar_cls = BasicToolbar
    inherit_tools = False
    tools = ['TEST3']
    subtools = {'TEST3': ['TEST3A', 'TEST3B']}

    def __init__(self, session, parent=None):
        super(ExampleViewer3, self).__init__(session, parent=parent)


def test_duplicate_shortcut():
    session = simple_session()
    expected_warning = ("Tools 'TEST1' and 'TEST2' have the same "
                        r"shortcut \('A'\). Ignoring shortcut for 'TEST2'")
    with pytest.warns(UserWarning, match=expected_warning):
        ExampleViewer2(session)


def test_subtool_enabled():
    session = simple_session()
    viewer = ExampleViewer3(session)
    tool = viewer.toolbar.tools["TEST3"]
    subtool_a, subtool_b = tool.subtools

    toolbar = viewer.toolbar
    # The first tool button is for the drag box. We only have one tool, so grab the next one
    tool_button = [child for child in toolbar.children() if isinstance(child, QToolButton)][1]
    menu = tool_button.menu()
    action_a, action_b = menu.actions()

    for enabled_a, enabled_b in product((False, True), repeat=2):
        subtool_a.enabled = enabled_a
        subtool_b.enabled = enabled_b
        assert action_a.isEnabled() == enabled_a
        assert action_a.isVisible() == enabled_a
        assert action_b.isEnabled() == enabled_b
        assert action_b.isVisible() == enabled_b
