from ..data_slice_widget import SliceWidget
from ..slice_widget import MultiSliceWidgetHelper

from astropy.wcs import WCS
from astropy.wcs.wcsapi import SlicedLowLevelWCS
from numpy.testing import assert_allclose
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

    def test_sliders_show_world_axis_of_data_with_more_world_axes(self):
        # Three pixel axes and four world axes: the latitude pixel axis is
        # sliced away and its world axis stays, as longitude depends on it
        wcs = WCS(naxis=4)
        wcs.wcs.ctype = ['HPLN-TAN', 'HPLT-TAN', 'WAVE', 'STOKES']
        wcs.wcs.cunit = ['arcsec', 'arcsec', 'nm', '']
        wcs.wcs.crval = [0, 0, 630, 1]
        wcs.wcs.crpix = [1, 1, 1, 1]
        wcs.wcs.cdelt = [2, 2, 0.01, 1]
        coords = SlicedLowLevelWCS(wcs, (slice(None), slice(None), 0, slice(None)))
        data = Data(x=arange(120).reshape((4, 5, 6)), coords=coords, label="Cube")

        state = ViewerTestState()
        state.reference_data = data
        state.x_att = data.pixel_component_ids[2]
        state.y_att = data.pixel_component_ids[1]
        state.slices = (0,) * data.ndim

        # Each slider shows the world axis that glue's world component of its
        # axis reads (glue-viz/glue#2573), world_n_dim - 1 - axis
        helper = MultiSliceWidgetHelper(viewer_state=state, layout=QVBoxLayout())
        stokes = helper._sliders[0]
        assert stokes._world_unit == ''
        assert_allclose(stokes._world, [1, 2, 3, 4])

        state.y_att = data.pixel_component_ids[0]
        wavelength = helper._sliders[1]
        assert wavelength._world_unit == 'm'
        assert_allclose(wavelength._world, 6.3e-7 + 1e-11 * arange(5))

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
