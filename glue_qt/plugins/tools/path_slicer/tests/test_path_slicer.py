from unittest.mock import MagicMock

import numpy as np

from glue.core import Data
from glue.core.coordinates import IdentityCoordinates
from glue.plugins.tools.path_slicer.path_sliced_data import PathSlicedData

from glue_qt.app import GlueApplication
from glue_qt.viewers.image import ImageViewer

from .. import PathSlicerMode, PathSlicerCrosshairMode


class TestPathSlicerMode:

    def setup_method(self, method):
        self.cube = Data(label='cube',
                         x=np.arange(1000).reshape((5, 10, 20)),
                         coords=IdentityCoordinates(n_dim=3))
        self.app = GlueApplication()
        self.dc = self.app.data_collection
        self.dc.append(self.cube)
        self.viewer = self.app.new_data_viewer(ImageViewer, data=self.cube)

    def teardown_method(self, method):
        self.viewer.close()
        self.viewer = None
        self.app.close()
        self.app = None

    def test_extract_callback_creates_path_sliced_data(self):
        self.viewer.toolbar.active_tool = 'slice'
        tool = self.viewer.toolbar.active_tool
        assert isinstance(tool, PathSlicerMode)

        # Stub the ROI to feed a known vertex list to _extract_callback.
        roi = MagicMock()
        roi.to_polygon.return_value = ([1, 10, 12], [2, 13, 14])
        mode = MagicMock()
        mode.roi.return_value = roi

        tool._extract_callback(mode)

        # The data collection should now hold the cube and one path slice.
        slices = [d for d in self.dc if isinstance(d, PathSlicedData)]
        assert len(slices) == 1
        assert slices[0].original_data is self.cube
        # parent_viewer is wired up so PathSlicerCrosshairMode can find
        # its way back to the cube viewer.
        assert slices[0].parent_viewer is self.viewer

    def test_re_extracting_updates_existing_slice_in_place(self):
        self.viewer.toolbar.active_tool = 'slice'
        tool = self.viewer.toolbar.active_tool

        roi = MagicMock()
        roi.to_polygon.return_value = ([1, 10, 12], [2, 13, 14])
        mode = MagicMock()
        mode.roi.return_value = roi
        tool._extract_callback(mode)
        first_slice = [d for d in self.dc if isinstance(d, PathSlicedData)][0]
        first_x = first_slice.x.copy()

        # Re-trace -- there must still be a single slice and its x must have
        # been replaced (not appended-to or recreated).
        roi.to_polygon.return_value = ([0, 5, 15], [0, 4, 12])
        tool._extract_callback(mode)
        slices = [d for d in self.dc if isinstance(d, PathSlicedData)]
        assert len(slices) == 1
        assert slices[0] is first_slice
        assert not np.array_equal(first_x, slices[0].x)

    def test_crosshair_disabled_without_path_sliced_reference_data(self):
        # The crosshair tool only makes sense when the viewer's reference
        # data is a PathSlicedData with a known parent_viewer; on a plain
        # cube viewer it should be disabled.
        mode = PathSlicerCrosshairMode(self.viewer)
        assert mode.enabled is False
        assert mode.data is None

    def test_crosshair_enabled_on_slice_viewer(self):
        # Push a PathSlicedData through the slice tool, then verify the
        # crosshair tool reports as enabled when constructed against the
        # slice viewer (which the slice tool opened).
        self.viewer.toolbar.active_tool = 'slice'
        tool = self.viewer.toolbar.active_tool
        roi = MagicMock()
        roi.to_polygon.return_value = ([1, 10, 12], [2, 13, 14])
        mode = MagicMock()
        mode.roi.return_value = roi
        tool._extract_callback(mode)

        slice_viewer = tool._slice_viewer
        assert slice_viewer is not None
        crosshair = PathSlicerCrosshairMode(slice_viewer)
        assert crosshair.enabled is True
        assert isinstance(crosshair.data, PathSlicedData)

    def test_crosshair_action_hidden_on_cube_viewer(self):
        # The crosshair tool only makes sense over a slice viewer; the
        # toolbar must hide the action when the tool reports as disabled
        # at registration time (not just on subsequent changes).
        action = self.viewer.toolbar.actions['path:crosshair']
        assert action.isVisible() is False
        assert self.viewer.toolbar.tools['path:crosshair'].enabled is False

    # ------------------------------------------------------------------
    # Multi-path dropdown
    # ------------------------------------------------------------------

    def _trace(self, tool, vx, vy):
        roi = MagicMock()
        roi.to_polygon.return_value = (list(vx), list(vy))
        mode = MagicMock()
        mode.roi.return_value = roi
        tool._extract_callback(mode)

    def test_create_new_after_trace_extends_path_list(self):
        # First trace creates path 1; user picks "Create new" from the
        # menu; second trace creates path 2.
        self.viewer.toolbar.active_tool = 'slice'
        tool = self.viewer.toolbar.active_tool

        self._trace(tool, [1, 10, 12], [2, 13, 14])
        assert len(tool._traces) == 1
        # After a trace, _target_trace points at the most recent trace
        # (so consecutive Enters keep updating the same path).
        assert tool._target_trace is tool._traces[0]

        # User picks "Create new path" from the dropdown.
        tool.set_target(None)
        self._trace(tool, [0, 5, 15], [0, 4, 12])
        assert len(tool._traces) == 2
        # Now the most recently created trace is the target.
        assert tool._target_trace is tool._traces[1]

        slices = [d for d in self.dc if isinstance(d, PathSlicedData)]
        assert len(slices) == 2

    def test_create_new_opens_a_fresh_slice_viewer_each_time(self):
        # "Create new path" should open its own slice viewer; selecting
        # an existing path from the dropdown and re-tracing must NOT
        # open another one (the existing viewer's layer just refreshes).
        self.viewer.toolbar.active_tool = 'slice'
        tool = self.viewer.toolbar.active_tool

        self._trace(tool, [1, 10, 12], [2, 13, 14])
        assert len(tool._slice_viewers) == 1
        first_slice_viewer = tool._slice_viewers[0]

        tool.set_target(None)
        self._trace(tool, [0, 5, 15], [0, 4, 12])
        # A second slice viewer was opened for the new path.
        assert len(tool._slice_viewers) == 2
        assert tool._slice_viewers[0] is first_slice_viewer
        assert tool._slice_viewers[1] is not first_slice_viewer

        # Updating an existing path must not open a third.
        tool.set_target(tool._traces[0])
        self._trace(tool, [3, 7, 11], [4, 8, 12])
        assert len(tool._slice_viewers) == 2

    def test_creating_new_does_not_disturb_previous_path(self):
        # Regression: an earlier prototype routed the slice-viewer side
        # through ``open_or_update_slice_viewer`` from path_slicer.common,
        # whose ``find_existing_path_slice`` returned the first
        # PathSlicedData over the cube and overwrote it -- so creating
        # path 2 silently corrupted path 1.
        self.viewer.toolbar.active_tool = 'slice'
        tool = self.viewer.toolbar.active_tool
        self._trace(tool, [1, 10, 12], [2, 13, 14])
        first_x = tool._traces[0][0].x.copy()
        first_y = tool._traces[0][0].y.copy()

        tool.set_target(None)
        self._trace(tool, [0, 5, 15], [0, 4, 12])

        # Path 1 must still have its original vertices.
        assert np.array_equal(tool._traces[0][0].x, first_x)
        assert np.array_equal(tool._traces[0][0].y, first_y)

    def test_menu_entries_reflect_current_traces(self):
        self.viewer.toolbar.active_tool = 'slice'
        tool = self.viewer.toolbar.active_tool

        # Empty path list -> only "Create new path".
        entries = tool.menu_entries()
        assert [label for label, _ in entries] == ['Create new path']

        # After two traces, the menu lists both as update candidates.
        self._trace(tool, [1, 10, 12], [2, 13, 14])
        tool.set_target(None)
        self._trace(tool, [0, 5, 15], [0, 4, 12])

        labels = [label for label, _ in tool.menu_entries()]
        assert labels == [
            'Create new path', 'Update path 1', 'Update path 2']
        targets = [target for _, target in tool.menu_entries()]
        assert targets[0] is None
        assert targets[1] is tool._traces[0]
        assert targets[2] is tool._traces[1]

    def test_set_target_to_existing_trace_then_re_extract_updates_that_one(self):
        self.viewer.toolbar.active_tool = 'slice'
        tool = self.viewer.toolbar.active_tool

        self._trace(tool, [1, 10, 12], [2, 13, 14])
        first_trace = tool._traces[0]
        first_x = first_trace[0].x.copy()

        tool.set_target(None)
        self._trace(tool, [0, 5, 15], [0, 4, 12])
        second_trace = tool._traces[1]

        # User selects "Update path 1" and re-traces -- the first slice
        # is refreshed while the second is left alone.
        tool.set_target(first_trace)
        second_x_before = second_trace[0].x.copy()
        self._trace(tool, [3, 7, 11], [4, 8, 12])

        assert not np.array_equal(first_x, first_trace[0].x)
        assert np.array_equal(second_x_before, second_trace[0].x)
        # Still just two PathSlicedData -- nothing new was created.
        slices = [d for d in self.dc if isinstance(d, PathSlicedData)]
        assert len(slices) == 2

    def test_overlays_show_one_line_per_trace_with_active_opaque(self):
        # The on-source-viewer overlay should have one Line2D per trace,
        # the active trace at alpha=1.0 and the others faded.
        self.viewer.toolbar.active_tool = 'slice'
        tool = self.viewer.toolbar.active_tool

        self._trace(tool, [1, 10, 12], [2, 13, 14])
        tool.set_target(None)
        self._trace(tool, [0, 5, 15], [0, 4, 12])
        # Two overlays now exist (one per trace).
        assert len(tool._overlays) == 2
        # The active one is the second trace (set just above by the
        # post-trace "newest is the target" rule).
        active_line = tool._overlays[id(tool._traces[1])]
        other_line = tool._overlays[id(tool._traces[0])]
        assert active_line.get_alpha() > other_line.get_alpha()
