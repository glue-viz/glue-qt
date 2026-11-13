import numpy as np

from ..data_slice_widget import SliceWidget


class TestSliceWidget(object):

    def test_slice_center(self):
        s = SliceWidget(lo=0, hi=10)
        assert s.state.slice_center == 5

    def test_browse_slice(self):
        s = SliceWidget(lo=0, hi=10)
        assert s.state.slice_center == 5
        s.button_prev.click()
        assert s.state.slice_center == 4
        s.button_next.click()
        s.button_next.click()
        assert s.state.slice_center == 6
        s.button_first.click()
        assert s.state.slice_center == 0
        s.button_prev.click()
        assert s.state.slice_center == 10
        s.button_next.click()
        assert s.state.slice_center == 0
        s.button_last.click()
        assert s.state.slice_center == 10
        s.button_next.click()
        assert s.state.slice_center == 0
        s.button_prev.click()
        assert s.state.slice_center == 10
        s.button_prev.click()
        assert s.state.slice_center == 9

    def test_slice_world(self):

        s = SliceWidget(lo=0, hi=5, world=[1, 3, 5, 5.5, 8, 12])

        # Check switching between world and pixel coordinates
        s.state.slice_center = 0
        assert s.state.slider_label == '1.0'
        s.state.use_world = False
        assert s.state.slider_label == '0'
        s.state.slice_center = 3
        assert s.state.slider_label == '3'
        s.state.use_world = True
        assert s.state.slider_label == '5.5'

        # Round to nearest
        s.state.slider_label = '11'
        assert s.state.slice_center == 5
        assert s.state.slider_label == '12.0'

        # Make sure out of bound values work
        s.state.slider_label = '20'
        assert s.state.slice_center == 5
        assert s.state.slider_label == '12.0'
        s.state.slider_label = '-10'
        assert s.state.slice_center == 0
        assert s.state.slider_label == '1.0'

        # And disable world and try and set by pixel
        s.state.use_world = False
        s.state.slider_label = '4'
        assert s.state.slice_center == 4
        assert s.state.slider_label == '4'

    def test_slice_world_datetime(self):

        world = np.array(['2021-09-05T00:18:47.390', '2021-09-05T00:19:00', '2021-09-05T00:19:12.610'],
                         dtype='datetime64[ns]')
        s = SliceWidget(lo=0, hi=2, world=world, world_unit='UTC')

        s.state.slice_center = 0
        assert s.state.slider_label == '2021-09-05T00:18:47.390'
        assert s.state.slider_unit == 'UTC'

        # Typed times round to the nearest slice
        s.state.slider_label = '2021-09-05T00:19:10'
        assert s.state.slice_center == 2
        assert s.state.slider_label == '2021-09-05T00:19:12.610'

        s.state.use_world = False
        assert s.state.slider_label == '2'
        assert s.state.slider_unit == ''

        # Whole seconds are shown without milliseconds
        s = SliceWidget(lo=0, hi=1, world=world[1:2].repeat(2) + np.array([0, 60]).astype('timedelta64[s]'))
        assert s.state.slider_label == '2021-09-05T00:19:00'
