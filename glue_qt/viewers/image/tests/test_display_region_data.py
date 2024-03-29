# pylint: disable=I0011,W0613,W0201,W0212,E1101,E1103

import os

import numpy as np
import shapely
from shapely.geometry import MultiPolygon, Polygon, Point

from glue.core.data_region import RegionData
from glue.core.data import Data
from glue.core.component import Component
from glue_qt.utils import combo_as_string, process_events
from glue_qt.app import GlueApplication
from glue.core.fixed_resolution_buffer import ARRAY_CACHE, PIXEL_CACHE
from glue.core.link_helpers import LinkSame

from astropy.wcs import WCS


from ..data_viewer import ImageViewer

DATA = os.path.join(os.path.dirname(__file__), 'data')


class TestRegionScatterViewer(object):

    def setup_method(self, method):

        poly_1 = Polygon([(20, 20), (60, 20), (60, 40), (20, 40)])
        poly_2 = Polygon([(60, 50), (60, 70), (80, 70), (80, 50)])
        poly_3 = Polygon([(10, 10), (15, 10), (15, 15), (10, 15)])
        poly_4 = Polygon([(10, 20), (15, 20), (15, 30), (10, 30), (12, 25)])

        polygons = MultiPolygon([poly_3, poly_4])

        my_geoms = np.array([poly_1, poly_2, polygons])

        representative_points = [s.representative_point() for s in my_geoms]

        cell_number = Component(np.array([1, 2, 3]))

        self.region_data = RegionData(regions=my_geoms,
                                      cell_number=cell_number)

        random_2d_array = np.random.randint(1, 20, size=(100, 100))
        self.data_2d = Data(label='image_data', z=random_2d_array)
        self.catalog = Data(label='catalog', c=[1, 3, 2], d=[4, 3, 3])

        self.application = GlueApplication()

        self.session = self.application.session

        self.hub = self.session.hub

        self.data_collection = self.session.data_collection
        self.data_collection.append(self.region_data)
        self.data_collection.append(self.data_2d)
        self.data_collection.append(self.catalog)

        self.viewer = self.application.new_data_viewer(ImageViewer)

        self.data_collection.register_to_hub(self.hub)
        self.viewer.register_to_hub(self.hub)

        self.options_widget = self.viewer.options_widget()

    def teardown_method(self, method):

        # Properly close viewer and application
        self.viewer.close()
        self.viewer = None
        self.application.close()
        self.application = None

        # Make sure cache is empty
        if len(PIXEL_CACHE) > 0:
            raise Exception("Pixel cache contains {0} elements".format(len(PIXEL_CACHE)))
        if len(ARRAY_CACHE) > 0:
            raise Exception("Array cache contains {0} elements".format(len(ARRAY_CACHE)))

    def test_link_first_then_add(self):

        # Check defaults when we add data

        self.viewer.add_data(self.data_2d)
        link1 = LinkSame(self.region_data.center_x_id, self.data_2d.pixel_component_ids[0])
        link2 = LinkSame(self.region_data.center_y_id, self.data_2d.pixel_component_ids[1])

        self.data_collection.add_link(link1)
        self.data_collection.add_link(link2)
        process_events()

        assert len(self.viewer.state.layers) == 1

        self.viewer.add_data(self.region_data)

        assert len(self.viewer.state.layers) == 2
        assert self.viewer.layers[0].enabled  # image
        assert self.viewer.layers[1].enabled  # regions

    def test_add_first_then_link(self):

        # Check defaults when we add data

        self.viewer.add_data(self.data_2d)

        assert combo_as_string(self.options_widget.ui.combosel_x_att_world) == 'Coordinate components:Pixel Axis 0 [y]:Pixel Axis 1 [x]'
        assert combo_as_string(self.options_widget.ui.combosel_y_att_world) == 'Coordinate components:Pixel Axis 0 [y]:Pixel Axis 1 [x]'

        assert self.viewer.axes.get_xlabel() == 'Pixel Axis 1 [x]'
        assert self.viewer.state.x_att_world is self.data_2d.id['Pixel Axis 1 [x]']
        assert self.viewer.state.x_att is self.data_2d.pixel_component_ids[1]

        assert self.viewer.axes.get_ylabel() == 'Pixel Axis 0 [y]'
        assert self.viewer.state.y_att_world is self.data_2d.id['Pixel Axis 0 [y]']
        assert self.viewer.state.y_att is self.data_2d.pixel_component_ids[0]

        assert not self.viewer.state.x_log
        assert not self.viewer.state.y_log

        assert len(self.viewer.state.layers) == 1

        self.viewer.add_data(self.region_data)

        assert len(self.viewer.state.layers) == 2
        assert self.viewer.layers[0].enabled  # image
        assert not self.viewer.layers[1].enabled  # regions

        process_events()

        link1 = LinkSame(self.region_data.center_x_id, self.data_2d.pixel_component_ids[0])
        link2 = LinkSame(self.region_data.center_y_id, self.data_2d.pixel_component_ids[1])

        self.data_collection.add_link(link1)
        self.data_collection.add_link(link2)
        process_events()

        assert len(self.viewer.state.layers) == 2
        assert self.viewer.layers[0].enabled  # image
        assert self.viewer.layers[1].enabled  # regions

    def test_subset(self):
        self.viewer.add_data(self.data_2d)

        self.viewer.add_data(self.region_data)
        link1 = LinkSame(self.region_data.center_x_id, self.data_2d.pixel_component_ids[0])
        link2 = LinkSame(self.region_data.center_y_id, self.data_2d.pixel_component_ids[1])

        self.data_collection.add_link(link1)
        self.data_collection.add_link(link2)

        self.data_collection.new_subset_group(subset_state=self.region_data.center_x_id > 20)

        process_events()

        assert self.viewer.layers[0].enabled  # image
        assert self.viewer.layers[1].enabled  # scatter
        assert self.viewer.layers[2].enabled  # image subset
        assert self.viewer.layers[3].enabled  # scatter subset


class TestWCSRegionDisplay(object):
    def setup_method(self, method):

        wcs1 = WCS(naxis=2)
        wcs1.wcs.ctype = 'DEC--TAN', 'RA---TAN'
        wcs1.wcs.set()

        self.image1 = Data(label='image1', a=[[3, 3], [2, 2]], b=[[4, 4], [3, 2]],
                            coords=wcs1)
        SHAPELY_CIRCLE_ARRAY = np.array([Point(2.5, 2.5).buffer(1), Point(1, 1).buffer(1)])
        self.region_data = RegionData(label='My Regions',
                                      color=np.array(['red', 'blue']),
                                      area=shapely.area(SHAPELY_CIRCLE_ARRAY),
                                      boundary=SHAPELY_CIRCLE_ARRAY)
        self.application = GlueApplication()

        self.session = self.application.session

        self.hub = self.session.hub

        self.data_collection = self.session.data_collection
        self.data_collection.append(self.image1)
        self.data_collection.append(self.region_data)

        self.viewer = self.application.new_data_viewer(ImageViewer)

        self.data_collection.register_to_hub(self.hub)
        self.viewer.register_to_hub(self.hub)

    def teardown_method(self, method):

        # Properly close viewer and application
        self.viewer.close()
        self.viewer = None
        self.application.close()
        self.application = None

        # Make sure cache is empty
        if len(PIXEL_CACHE) > 0:
            raise Exception("Pixel cache contains {0} elements".format(len(PIXEL_CACHE)))
        if len(ARRAY_CACHE) > 0:
            raise Exception("Array cache contains {0} elements".format(len(ARRAY_CACHE)))

    def test_basics(self):
        self.viewer.add_data(self.image1)

        link1 = LinkSame(self.region_data.center_x_id, self.image1.world_component_ids[0])
        link2 = LinkSame(self.region_data.center_y_id, self.image1.world_component_ids[1])

        self.data_collection.add_link(link1)
        self.data_collection.add_link(link2)

        self.viewer.add_data(self.region_data)

        self.viewer.state._display_world
        assert len(self.viewer.state.layers) == 2
        assert self.viewer.layers[0].enabled
        assert self.viewer.layers[1].enabled
