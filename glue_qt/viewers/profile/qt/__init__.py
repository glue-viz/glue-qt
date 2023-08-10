from .data_viewer import ProfileViewer  # noqa


def setup():
    from glue_qt.config import qt_client
    qt_client.add(ProfileViewer)
