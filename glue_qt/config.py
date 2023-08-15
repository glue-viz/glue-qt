from collections import namedtuple

from glue.config import Registry, DictRegistry


__all__ = ['QtClientRegistry',
           'LayerActionRegistry', 'qt_client',
           'preference_panes', 'PreferencePanesRegistry',
           'layer_action',
           'StartupActionRegistry', 'startup_action', 'QtFixedLayoutTabRegistry',
           'qt_fixed_layout_tab', 'KeyboardShortcut', 'keyboard_shortcut']


class MenubarPluginRegistry(Registry):
    """
    Stores menubar plugins.

    The members property is a list of menubar plugins, each represented as a
    ``(label, function)`` tuple. The ``function`` should take two items which
    are a reference to the session and to the data collection respectively.
    """

    def add(self, label, function):
        """
        Add a new menubar plugin
        :param label: Short label for the plugin
        :type label: str

        :param function: function
        :type function: function()
        """
        self.members.append((label, function))

    def __call__(self, label):
        def adder(func):
            self.add(label, func)
            return func
        return adder


class PreferencePanesRegistry(DictRegistry):
    """
    Stores preference panes

    The members property is a list of tuples of Qt widget classes that can have
    their own tab in the preferences window.
    """

    def add(self, label, widget_cls):
        self._members[label] = widget_cls

    def __iter__(self):
        for label in self._members:
            yield label, self._members[label]


class QtClientRegistry(Registry):
    """
    Stores QT widgets to visualize data.

    The members property is a list of Qt widget classes

    New widgets can be registered via::

        @qt_client
        class CustomWidget(QMainWindow):
            ...
    """


class QtFixedLayoutTabRegistry(Registry):
    """
    Stores Qt pre-defined tabs (non-MDI)

    New widgets can be registered via::

        @qt_fixed_layout_tab
        class CustomTab(QWidget):
            ...
    """


class StartupActionRegistry(DictRegistry):

    def add(self, startup_name, startup_function):
        """
        Add a startup function to the registry. This is a function that will
        get called once glue has been started and any data loaded, and can
        be used to set up specific layouts and create links.

        Startup actions are triggered by either specifying comma-separated names
        of actions on the command-line::

            glue --startup=mystartupaction

        or by passing an iterable of startup action names to the ``startup``
        keyword of ``GlueApplication``.

        The startup function will be given the session object and the data
        collection object.
        """
        if startup_name in self.members:
            raise ValueError("A startup action with the name '{0}' already exists".format(startup_name))
        else:
            self.members[startup_name] = startup_function

    def __call__(self, name):
        def adder(func):
            self.add(name, func)
            return func
        return adder


class LayerActionRegistry(Registry):
    """
    Stores custom menu actions available when the user select one or more
    datasets, subset group, or subset in the data collection view.

    This members property is a list of named tuples with the following
    attributes:

    * ``label``: the user-facing name of the action
    * ``tooltip``: the text that appears when hovering with the mouse over the action
    * ``callback``: the function to call when the action is triggered
    * ``icon``: an icon image to use for the layer action
    * ``single``: whether to show this action only when selecting single layers (default: `False`)
    * ``data``: if ``single`` is `True` whether to only show the action when selecting a dataset
    * ``subset_group``: if ``single`` is `True` whether to only show the action when selecting a subset group
    * ``subset``: if ``single`` is `True` whether to only show the action when selecting a subset

    The callback function is called with two arguments. If ``single`` is
    `True`, the first argument is the selected layer, otherwise it is the list
    of selected layers. The second argument is the
    `~glue.core.data_collection.DataCollection` object.
    """
    item = namedtuple('LayerAction', 'label tooltip callback icon single data subset_group, subset')

    def __call__(self, label, callback=None, tooltip=None, icon=None, single=False,
                 data=False, subset_group=False, subset=False):

        # Backward-compatibility
        if callback is not None:
            self.add(self.item(label, tooltip, callback, icon, True,
                               False, False, True))
            return True

        def adder(func):
            self.add(self.item(label, tooltip, func, icon, single,
                               data, subset_group, subset))
            return func
        return adder


class BooleanSetting(object):

    def __init__(self, default=True):
        self.state = default

    def __call__(self, state=None):
        if state not in [None, True, False]:
            raise ValueError("Invalid True/False setting: %s" % state)

        if state is not None:
            self.state = state

        return self.state


class KeyboardShortcut(DictRegistry):
    """
    Stores keyboard shortcuts.
    The members property is a dictionary within a dictionary of keyboard
    shortcuts, which is represented as (viewer,(keybind,function)). The
    ``function`` should take one item, which is a reference to the session.
    """

    def add(self, valid_viewers, keybind, function):
        """
        Add a new keyboard shortcut

        Parameters
        ----------
        arg1: list
            list of viewers where event can be fired
        arg2: Qt.Key
            type of key event
        arg3: function()
            function to be run that corresponds with key
        """
        if valid_viewers:
            for viewer in valid_viewers:
                if viewer in self.members:
                    if keybind in self.members[viewer]:
                        raise ValueError("Keyboard shortcut '{0}' already registered in {1}".format(keybind, viewer))
                    else:
                        self.members[viewer][keybind] = function
                else:
                    self.members[viewer] = {keybind: function}
        else:
            if None in self.members:
                if keybind in self.members[None]:
                    raise ValueError("Keyboard shortcut '{0}' already registered in {1}".format(keybind, None))
                else:
                    self.members[None][keybind] = function
            else:
                self.members[None] = {keybind: function}

    def __call__(self, keybind, valid_viewers):
        def adder(func):
            self.add(valid_viewers, keybind, func)
            return func
        return adder


qt_client = QtClientRegistry()
qt_fixed_layout_tab = QtFixedLayoutTabRegistry()
startup_action = StartupActionRegistry()
preference_panes = PreferencePanesRegistry()
menubar_plugin = MenubarPluginRegistry()
layer_action = LayerActionRegistry()
keyboard_shortcut = KeyboardShortcut()
