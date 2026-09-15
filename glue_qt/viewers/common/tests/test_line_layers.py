import numpy as np
from numpy.testing import assert_allclose

from glue.core import Data
from glue.core.link_helpers import LinkSame
from glue.viewers.matplotlib.line_layers import (VerticalLineLayerArtist,
                                                 HorizontalLineLayerArtist,
                                                 add_vertical_lines,
                                                 add_horizontal_lines)

from glue_qt.app import GlueApplication
from glue_qt.viewers.scatter import ScatterViewer
from glue_qt.viewers.profile import ProfileViewer
from glue_qt.viewers.common.line_layer_style_editor import LineLayerStyleEditor


def assert_positions(artist, expected, horizontal=False):
    segments = artist.line_collection.get_segments()
    index = 1 if horizontal else 0
    assert_allclose([s[0][index] for s in segments], expected)


def make_app():
    app = GlueApplication()
    data = Data(x=[1., 2., 3., 4.], y=[4., 5., 6., 7.], label='data')
    lines = Data(position=[1., 3., 2., 3.], label='lines')
    app.data_collection.append(data)
    app.data_collection.append(lines)
    app.data_collection.add_link(LinkSame(lines.id['position'], data.id['x']))
    app.data_collection.add_link(LinkSame(lines.id['position'], data.id['y']))
    return app, data, lines


def test_scatter_viewer_line_layers():

    app, data, lines = make_app()

    viewer = app.new_data_viewer(ScatterViewer)
    viewer.add_data(data)

    vartist = add_vertical_lines(viewer, lines)
    hartist = add_horizontal_lines(viewer, lines)

    assert vartist.enabled and hartist.enabled
    assert_positions(vartist, [1, 2, 3])
    assert_positions(hartist, [1, 2, 3], horizontal=True)

    # The line layer style editor is set up and syncs in both directions
    editor = viewer._view.layout_style_widgets[vartist]
    assert isinstance(editor, LineLayerStyleEditor)

    editor.ui.value_linewidth.setValue(4)
    assert vartist.state.linewidth == 4
    assert vartist.line_collection.get_linewidth()[0] == 4

    vartist.state.linestyle = 'dashed'
    assert editor.ui.combosel_linestyle.currentIndex() == 1

    viewer.close()
    app.close()


def test_profile_viewer_line_layers():

    app = GlueApplication()
    spectrum = Data(flux=np.random.random(10), label='spectrum')
    lines = Data(position=[1., 3., 2., 3.], label='lines')
    app.data_collection.append(spectrum)
    app.data_collection.append(lines)
    app.data_collection.add_link(LinkSame(lines.id['position'], spectrum.pixel_component_ids[0]))

    viewer = app.new_data_viewer(ProfileViewer)
    viewer.add_data(spectrum)

    artist = add_vertical_lines(viewer, lines)
    assert artist.enabled
    assert_positions(artist, [1, 2, 3])

    editor = viewer._view.layout_style_widgets[artist]
    assert isinstance(editor, LineLayerStyleEditor)

    viewer.close()
    app.close()


def test_session_round_trip(tmpdir):

    # Line layers survive a session save and restore with the correct layer
    # artist classes since these are stored in the session file

    session_file = tmpdir.join('line_layers.glu').strpath

    app, data, lines = make_app()

    viewer = app.new_data_viewer(ScatterViewer)
    viewer.add_data(data)
    vartist = add_vertical_lines(viewer, lines)
    add_horizontal_lines(viewer, lines)
    vartist.state.linewidth = 5
    vartist.state.linestyle = 'dotted'

    app.save_session(session_file, include_data=True)
    viewer.close()
    app.close()

    app2 = GlueApplication.restore_session(session_file)
    viewer2 = app2.viewers[0][0]

    assert len(viewer2.layers) == 3
    vline2, hline2 = viewer2.layers[1], viewer2.layers[2]
    assert isinstance(vline2, VerticalLineLayerArtist)
    assert isinstance(hline2, HorizontalLineLayerArtist)
    assert vline2.enabled and hline2.enabled
    assert_positions(vline2, [1, 2, 3])
    assert_positions(hline2, [1, 2, 3], horizontal=True)
    assert vline2.state.linewidth == 5
    assert vline2.state.linestyle == 'dotted'

    # The restored layers also get their style editors
    assert isinstance(viewer2._view.layout_style_widgets[vline2], LineLayerStyleEditor)

    viewer2.close()
    app2.close()
