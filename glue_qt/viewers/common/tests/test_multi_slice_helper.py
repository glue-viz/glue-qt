from ..data_slice_widget import SliceWidget
from ..slice_widget import MultiSliceWidgetHelper, world_axis_times

from astropy.wcs import WCS

from echo import CallbackProperty, HasCallbackProperties
from glue.core import Data
from numpy import arange
from qtpy.QtWidgets import QVBoxLayout


class ViewerTestState(HasCallbackProperties):
    x_att = CallbackProperty()
    y_att = CallbackProperty()
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

    def test_time_axis_slider_shows_times(self):

        wcs = WCS(naxis=3)
        wcs.wcs.ctype = ['RA---TAN', 'DEC--TAN', 'TIME']
        wcs.wcs.cunit = ['deg', 'deg', 's']
        wcs.wcs.crval = [10, 20, 0]
        wcs.wcs.crpix = [1, 1, 1]
        wcs.wcs.cdelt = [0.1, 0.1, 60]
        # The pointing drifts with time (as for a solar image sequence), so
        # RA depends on the time pixel axis while time depends only on itself
        wcs.wcs.pc = [[1, 0, 0.001], [0, 1, 0], [0, 0, 1]]
        wcs.wcs.mjdref = [59462.0, 0.0]
        wcs.wcs.timesys = 'UTC'
        data = Data(x=arange(24).reshape((2, 3, 4)), coords=wcs, label="Cube")

        assert world_axis_times(wcs, data, pixel_axis=0, world_axis=0) is None
        times, scale = world_axis_times(wcs, data, pixel_axis=2, world_axis=2)
        assert scale == 'UTC'
        assert list(times.astype('datetime64[s]').astype(str)) == ['2021-09-05T00:00:00', '2021-09-05T00:01:00']

        state = ViewerTestState()
        state.reference_data = data
        state.x_att = data.pixel_component_ids[2]
        state.y_att = data.pixel_component_ids[1]
        state.slices = (0,) * data.ndim

        helper = MultiSliceWidgetHelper(viewer_state=state, layout=QVBoxLayout())
        slider = helper._sliders[0]
        assert slider.state.use_world  # the time shown is exact, so no warning
        assert slider.state.slider_label == '2021-09-05T00:00:00'
        assert slider.state.slider_unit == 'UTC'
        slider.state.slice_center = 1
        assert slider.state.slider_label == '2021-09-05T00:01:00'
        assert state.slices == (1, 0, 0)
