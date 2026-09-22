import platform
from unittest.mock import MagicMock

import pytest

from glue_qt.utils import app


def test_migrate_saved_default_font(monkeypatch):
    qapp = MagicMock()
    qapp.font.return_value.pointSize.return_value = 13

    application = MagicMock()
    application.instance.return_value = None
    application.return_value = qapp

    settings = MagicMock(FONT_SIZE=13)
    save_settings = MagicMock()

    monkeypatch.setattr(app, 'qapp', None)
    monkeypatch.setattr(app, '_default_point_size', None)
    monkeypatch.setattr(app, 'QT6', False)
    monkeypatch.setattr(app.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(app.QtWidgets, 'QApplication', application)
    monkeypatch.setattr(app, 'settings', settings)
    monkeypatch.setattr(app, 'save_settings', save_settings)

    app.get_qapp()

    assert settings.FONT_SIZE == -1
    save_settings.assert_called_once_with()
    qapp.setFont.assert_not_called()


def test_qt6_uses_native_tab_font(monkeypatch):
    tab_widget = MagicMock()
    settings = MagicMock(FONT_SIZE=13)

    monkeypatch.setattr(app, 'QT6', True)
    monkeypatch.setattr(app.platform, 'system', lambda: 'Darwin')
    monkeypatch.setattr(app, 'settings', settings)

    app.fix_tab_widget_fontsize(tab_widget)

    tab_widget.setStyleSheet.assert_not_called()


@pytest.mark.skipif(platform.system() != 'Darwin', reason='macOS only')
def test_mac_bundle_name():
    # get_qapp rewrites the main bundle's CFBundleName (the macOS menu-bar
    # title) through pyobjc before creating the QApplication
    NSBundle = pytest.importorskip('Foundation').NSBundle
    app.get_qapp()
    bundle = NSBundle.mainBundle()
    info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
    assert info['CFBundleName'] == 'glue'
