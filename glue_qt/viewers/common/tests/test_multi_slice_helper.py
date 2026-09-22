from ..data_slice_widget import SliceWidget
from ..slice_widget import MultiSliceWidgetHelper

from echo import CallbackProperty, HasCallbackProperties
from glue.core import Data
from numpy import arange
from qtpy.QtWidgets import QVBoxLayout


class ViewerTestState(HasCallbackProperties):
    x_att = CallbackProperty()
    y_att = CallbackProperty()
    reference_data = CallbackProperty()
    slices = CallbackProperty()


class ProfileLikeTestState(HasCallbackProperties):
    x_att = CallbackProperty()
    x_att_pixel = CallbackProperty()
    reference_data = CallbackProperty()
    slices = CallbackProperty()


class TestMultiSliceWidgetHelper(object):

    def test_no_slider_if_flat(self):
        x = arange(72).reshape((6, 4, 1, 3))
        data = Data(x=x, label="Flat Cube")

        state = ViewerTestState()
        state.reference_data = data
        state.x_att = data.pixel_component_ids[0]
        state.y_att = data.pixel_component_ids[1]
        state.slices = (0,) * data.ndim

        layout = QVBoxLayout()

        helper = MultiSliceWidgetHelper(viewer_state=state, layout=layout)
        assert helper._sliders[2] is None
        assert isinstance(helper._sliders[3], SliceWidget)

    def test_state_without_y_att(self):

        # The profile viewer state has no y_att, and the pixel axis shown on
        # the x axis is given by x_att_pixel

        x = arange(24).reshape((3, 4, 2))
        data = Data(x=x, label="Cube")

        state = ProfileLikeTestState()
        state.reference_data = data
        state.x_att = data.pixel_component_ids[0]
        state.x_att_pixel = data.pixel_component_ids[0]
        state.slices = (0,) * data.ndim

        layout = QVBoxLayout()

        helper = MultiSliceWidgetHelper(viewer_state=state, layout=layout)
        assert helper._sliders[0] is None
        assert isinstance(helper._sliders[1], SliceWidget)
        assert isinstance(helper._sliders[2], SliceWidget)

        # Moving a slider updates the state
        helper._sliders[1].state.slice_center = 2
        assert state.slices == (0, 2, 0)
