import numpy as np

from astropy.time import Time
from astropy.wcs.wcsapi import HighLevelWCSWrapper

from glue.core.coordinates import LegacyCoordinates
from glue.core.coordinate_helpers import world_axis
from glue_qt.viewers.common.data_slice_widget import SliceWidget
from glue.viewers.image.state import AggregateSlice
from glue.utils.decorators import avoid_circular

__all__ = ['MultiSliceWidgetHelper', 'world_axis_times']


def world_axis_times(wcs, data, *, pixel_axis=None, world_axis=None):
    """
    Find the times along a pixel dimension whose world axis is a time axis.

    Parameters
    ----------
    wcs : APE 14 low-level WCS
        The coordinates of the data.
    data : `~glue.core.data.Data`
        The data to compute the coordinate axis for (this is used to
        determine the size of the axis).
    pixel_axis : `int`
        The pixel axis along which to compute the times, in coordinate order.
    world_axis : `int`
        The world axis to compute.

    Returns
    -------
    times, scale : `~numpy.ndarray`, `str`
        The times as ``datetime64`` values, and the name of their time scale
        (for example ``'UTC'``) to show as the unit; or `None` if the world
        axis is not a time axis or the WCS cannot represent it as
        `~astropy.time.Time` objects, in which case the numeric world values
        should be used instead.

    Notes
    -----
    As for :func:`~glue.core.coordinate_helpers.world_axis`, the pixel
    positions along all other axes are at the center of the data.
    """
    if wcs.world_axis_physical_types[world_axis] != 'time':
        return None
    numpy_axis = wcs.pixel_n_dim - 1 - pixel_axis
    n = data.shape[numpy_axis]
    pixel = [np.arange(n) if i == numpy_axis else np.repeat((size - 1) / 2, n)
             for i, size in enumerate(data.shape)]
    components = wcs.world_axis_object_components
    # astropy returns one high-level object per key, in order of first appearance
    keys = list(dict.fromkeys(component[0] for component in components))
    try:
        objects = HighLevelWCSWrapper(wcs).pixel_to_world(*pixel[::-1])
        if not isinstance(objects, (list, tuple)):
            objects = [objects]
        times = objects[keys.index(components[world_axis][0])]
        if not isinstance(times, Time):
            return None
        return times.to_value('datetime64'), times.scale.upper()
    except Exception:
        # Anything the WCS cannot do at the high level falls back to numbers
        return None


class MultiSliceWidgetHelper(object):

    def __init__(self, viewer_state=None, layout=None):

        self.viewer_state = viewer_state

        self.layout = layout
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(0, 3, 0, 3)

        self.viewer_state.add_callback('x_att', self.sync_sliders_from_state)
        self.viewer_state.add_callback('y_att', self.sync_sliders_from_state)
        if hasattr(self.viewer_state, 'z_att'):
            self.viewer_state.add_callback('z_att', self.sync_sliders_from_state)
        self.viewer_state.add_callback('slices', self.sync_sliders_from_state)
        self.viewer_state.add_callback('reference_data', self.sync_sliders_from_state)

        self._sliders = []

        self._reference_data = None
        self._x_att = None
        self._y_att = None
        self._z_att = None

        self.sync_sliders_from_state()

    @property
    def data(self):
        return self.viewer_state.reference_data

    def _clear(self):

        for _ in range(self.layout.count()):
            self.layout.takeAt(0)

        for s in self._sliders:
            if s is not None:
                s.close()

        self._sliders = []

    @avoid_circular
    def sync_state_from_sliders(self, *args):
        slices = []
        for i, slider in enumerate(self._sliders):
            if slider is not None:
                slices.append(slider.state.slice_center)
            else:
                slices.append(self.viewer_state.slices[i])
        self.viewer_state.slices = tuple(slices)

    @avoid_circular
    def sync_sliders_from_state(self, *args):

        if self.data is None or \
           self.viewer_state.x_att is None or \
           self.viewer_state.y_att is None or \
           (hasattr(self.viewer_state, "z_att") and self.viewer_state.z_att is None):
            return

        if any((self.viewer_state.x_att is self.viewer_state.y_att,
                self.viewer_state.x_att is getattr(self.viewer_state, "z_att", None),
                self.viewer_state.y_att is getattr(self.viewer_state, "z_att", None))):
            return

        # Update sliders if needed

        if (self.viewer_state.reference_data is not self._reference_data or
            self.viewer_state.x_att is not self._x_att or
            self.viewer_state.y_att is not self._y_att or
            (hasattr(self.viewer_state, "z_att") and self.viewer_state.z_att is not self._z_att)):

            self._reference_data = self.viewer_state.reference_data
            self._x_att = self.viewer_state.x_att
            self._y_att = self.viewer_state.y_att
            self._z_att = getattr(self.viewer_state, "z_att", None)

            self._clear()

            for i in range(self.data.ndim):

                if i == self.viewer_state.x_att.axis or \
                   i == self.viewer_state.y_att.axis or \
                   (hasattr(self.viewer_state, "z_att") and i == self.viewer_state.z_att.axis):
                    self._sliders.append(None)
                    continue

                # TODO: For now we simply pass a single set of world coordinates,
                # but we will need to generalize this in future. We deliberately
                # check the type of data.coords here since we want to treat
                # subclasses differently.
                if getattr(self.data, 'coords') is not None and type(self.data.coords) is not LegacyCoordinates:
                    world_axis_index = self.data.ndim - 1 - i
                    world = world_axis(self.data.coords, self.data,
                                       pixel_axis=world_axis_index,
                                       world_axis=world_axis_index)
                    world_unit = self.data.coords.world_axis_units[world_axis_index]
                    times = world_axis_times(self.data.coords, self.data,
                                             pixel_axis=world_axis_index,
                                             world_axis=world_axis_index)
                    if times is not None:
                        world, world_unit = times
                    # Warn if the world value shown depends on other pixel axes
                    # (which are held at their center), not if other world axes
                    # happen to depend on this pixel axis
                    correlated = self.data.coords.axis_correlation_matrix[world_axis_index]
                    world_warning = not (correlated[world_axis_index] and correlated.sum() == 1)
                    world_label = self.data.world_component_ids[i].label
                else:
                    world = None
                    world_unit = None
                    world_warning = False
                    world_label = self.data.pixel_component_ids[i].label

                if self.data.shape[i] > 1:
                    slider = SliceWidget(world_label,
                                         hi=self.data.shape[i] - 1, world=world,
                                         world_unit=world_unit, world_warning=world_warning)

                    self.slider_state = slider.state
                    self.slider_state.add_callback('slice_center', self.sync_state_from_sliders)
                    self._sliders.append(slider)
                    self.layout.addWidget(slider)
                else:
                    self._sliders.append(None)

        for i in range(self.data.ndim):
            if self._sliders[i] is not None:
                if isinstance(self.viewer_state.slices[i], AggregateSlice):
                    self._sliders[i].state.slice_center = self.viewer_state.slices[i].center
                else:
                    self._sliders[i].state.slice_center = self.viewer_state.slices[i]


if __name__ == "__main__":

    from glue.core import Data
    from glue_qt.utils import get_qapp
    from echo import CallbackProperty
    from glue.core.state_objects import State

    app = get_qapp()

    class FakeViewerState(State):
        x_att = CallbackProperty()
        y_att = CallbackProperty()
        reference_data = CallbackProperty()
        slices = CallbackProperty()

    viewer_state = FakeViewerState()

    data = Data(x=np.random.random((3, 50, 20, 5, 3)))

    viewer_state.reference_data = data
    viewer_state.x_att = data.pixel_component_ids[0]
    viewer_state.y_att = data.pixel_component_ids[3]
    viewer_state.slices = [0] * 5

    widget = MultiSliceWidgetHelper(viewer_state)
    widget.show()

    app.exec_()
