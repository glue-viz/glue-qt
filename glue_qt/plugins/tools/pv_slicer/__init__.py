from .pv_slicer import *  # noqa


def setup():
    from glue_qt.viewers.image.qt import ImageViewer
    from glue_qt.plugins.tools.pv_slicer.qt import PVSlicerMode  # noqa
    ImageViewer.tools.append('slice')
