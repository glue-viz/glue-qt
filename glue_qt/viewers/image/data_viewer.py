from glue_qt.viewers.matplotlib.data_viewer import MatplotlibDataViewer
from glue_qt.viewers.scatter.layer_style_editor import ScatterLayerStyleEditor, ScatterRegionLayerStyleEditor
from glue.viewers.scatter.layer_artist import ScatterLayerArtist, ScatterRegionLayerArtist
from glue_qt.viewers.image.layer_style_editor import ImageLayerStyleEditor
from glue_qt.viewers.image.layer_style_editor_subset import ImageLayerSubsetStyleEditor
from glue.viewers.image.layer_artist import ImageLayerArtist, ImageSubsetLayerArtist
from glue_qt.viewers.image.options_widget import ImageOptionsWidget
from glue_qt.viewers.image.mouse_mode import RoiClickAndDragMode
from glue.viewers.image.state import ImageViewerState
from glue.utils import defer_draw, decorate_all_methods

# Import the mouse mode to make sure it gets registered
from glue_qt.viewers.image.contrast_mouse_mode import ContrastBiasMode  # noqa
from glue_qt.viewers.image.profile_viewer_tool import ProfileViewerTool  # noqa
from glue_qt.viewers.image.pixel_selection_mode import PixelSelectionTool  # noqa

from glue.viewers.image.viewer import MatplotlibImageMixin

__all__ = ['ImageViewer']


@decorate_all_methods(defer_draw)
class ImageViewer(MatplotlibImageMixin, MatplotlibDataViewer):

    LABEL = '2D Image'
    _default_mouse_mode_cls = RoiClickAndDragMode
    _layer_style_widget_cls = {ImageLayerArtist: ImageLayerStyleEditor,
                               ImageSubsetLayerArtist: ImageLayerSubsetStyleEditor,
                               ScatterLayerArtist: ScatterLayerStyleEditor,
                               ScatterRegionLayerArtist: ScatterRegionLayerStyleEditor}
    _state_cls = ImageViewerState
    _options_cls = ImageOptionsWidget

    allow_duplicate_data = True

    # NOTE: _data_artist_cls and _subset_artist_cls are not defined - instead
    #       we override get_data_layer_artist and get_subset_layer_artist for
    #       more advanced logic.

    tools = ['select:rectangle', 'select:xrange',
             'select:yrange', 'select:circle',
             'select:polygon', 'image:point_selection', 'image:contrast_bias',
             'profile-viewer']

    def __init__(self, session, parent=None, state=None):
        MatplotlibDataViewer.__init__(self, session, wcs=True, parent=parent, state=state)
        MatplotlibImageMixin.setup_callbacks(self)

    def closeEvent(self, *args):
        super(ImageViewer, self).closeEvent(*args)
        if self.axes._composite_image is not None:
            self.axes._composite_image.remove()
            self.axes._composite_image = None
