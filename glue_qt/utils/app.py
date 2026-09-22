import time
import platform
from qtpy import QtCore, QtGui, QtWidgets, QtQuick, QT6

from glue.config import settings
from glue._settings_helpers import save_settings

__all__ = ['process_events', 'get_qapp', 'fix_tab_widget_fontsize',
           'update_global_font_size', 'default_font_size',
           'toolbar_icon_size']

qapp = None

# The platform default font point size, captured before any custom
# application font is applied. FONT_SIZE = -1/None means "track this".
_default_point_size = None


def _font_size_is_set():
    return settings.FONT_SIZE is not None and settings.FONT_SIZE != -1


def default_font_size():
    """
    The default application font point size, before any FONT_SIZE override.
    """
    if _default_point_size is not None:
        return _default_point_size
    return QtGui.QFont().pointSize()


def toolbar_icon_size(widget):
    """
    The platform toolbar icon size, capped at 24 px, as a QSize.
    """
    size = min(widget.style().pixelMetric(QtWidgets.QStyle.PM_ToolBarIconSize), 24)
    return QtCore.QSize(size, size)


def _fix_mac_app_name():
    # A Qt application launched from a plain Python interpreter shows
    # "python" as the macOS menu-bar application name: the name comes from
    # the Python framework bundle's CFBundleName, which no Qt API can
    # change. Update it through Cocoa before the QApplication (and with it
    # the native menu bar) is created.
    try:
        from Foundation import NSBundle
    except ImportError:
        return
    bundle = NSBundle.mainBundle()
    info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
    if info is not None:
        info['CFBundleName'] = 'glue'


def process_events(wait=None):
    app = get_qapp()
    if wait is None:
        app.processEvents()
    else:
        start = time.time()
        while time.time() - start < wait:
            app.processEvents()


def get_qapp(icon_path=None):

    global qapp, _default_point_size

    qapp = QtWidgets.QApplication.instance()

    if qapp is None:

        if platform.system() == 'Darwin':
            _fix_mac_app_name()

        # NOTE: plugins that need WebEngine may complain that QtWebEngineWidgets
        # needs to be imported before QApplication is constructed, but this can
        # cause segmentation faults to crop up under certain conditions, so we
        # don't do it here and instead ask that the plugins do it in their
        # main __init__.py (which should get executed before glue is launched).

        # NOTE: the following setting is needed to make sure we can use
        # WebEngine at the same time as the OpenGL widget, at least on MacOS X.
        # See https://bugreports.qt.io/browse/QTBUG-122886 for more details.
        if QT6:
            QtQuick.QQuickWindow.setGraphicsApi(QtQuick.QSGRendererInterface.GraphicsApi.OpenGL)

        qapp = QtWidgets.QApplication(['glue'])
        qapp.setApplicationName('glue')
        qapp.setQuitOnLastWindowClosed(True)

        if icon_path is not None:
            qapp.setWindowIcon(QtGui.QIcon(icon_path))

        # Remember the platform default before any override so the -1
        # ("use default") setting can always get back to it.
        _default_point_size = qapp.font().pointSize()

        # Older versions saved the derived default as if it were a user
        # override. Migrate that value back to the default sentinel once.
        if _default_point_size == settings.FONT_SIZE:
            settings.FONT_SIZE = -1
            save_settings()

        if _font_size_is_set():
            font = qapp.font()
            font.setPointSize(int(settings.FONT_SIZE))
            qapp.setFont(font)

    elif _default_point_size is None:
        # A host (e.g. IPython) created the application: its font is the
        # default, and QFont() would track any override applied later
        _default_point_size = qapp.font().pointSize()

    # Make sure we use high resolution icons for HDPI displays.
    try:
        qapp.setAttribute(QtCore.AA_UseHighDpiPixmaps)
    except AttributeError:  # PyQt6/PySide6 don't have this setting as it is default
        pass

    return qapp


def fix_tab_widget_fontsize(tab_widget):
    """
    Because of a bug in Qt5, tab titles on MacOS X don't pick up a custom
    application font. Only needed when FONT_SIZE overrides the default.
    """
    if platform.system() == 'Darwin' and not QT6 and _font_size_is_set():
        app_font = get_qapp().font()
        tab_widget.setStyleSheet('font-size: {0}pt'.format(app_font.pointSize()))


def update_global_font_size():
    """Updates the global font size through the current UI backend
    """
    if qapp is None:
        get_qapp()

    point_size = settings.FONT_SIZE if _font_size_is_set() else default_font_size()
    font = qapp.font()
    font.setPointSize(int(point_size))
    qapp.setFont(font)
