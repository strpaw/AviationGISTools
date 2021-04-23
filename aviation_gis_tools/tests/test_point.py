import unittest
from aviation_gis_tools.point import *


class PointTests(unittest.TestCase):

    def test_check_point_valid_data(self):
        point_data = [
            ('1234601.445E', 123.76706805555555, '453000.000S', -45.5, 'Circle center'),
            ('E17701', 177.016666666666666666, 'N7701', 77.016666666666666666, 'Circle center')
        ]

        for lon_src, lon_dd, lat_src, lat_dd, point_name in point_data:
            p = Point(lon_src, lat_src, point_name)
            self.assertEqual("", p.err_msg)
            self.assertAlmostEqual(lon_dd, p.lon.ang_dd)
            self.assertAlmostEqual(lat_dd, p.lat.ang_dd)

    def test_check_point_invalid_data(self):
        point_data = [
            ('1234601.445S', 123.76706805555555, '456000.000', -45.5, 'Circle center'),
            ('E17760', 177.016666666666666666, 'N 7701', 77.016666666666666666, 'Circle center')
        ]

        for lon_src, lon_dd, lat_src, lat_dd, point_name in point_data:
            p = Point(lon_src, lat_src, point_name)
            self.assertEqual("Circle center longitude error or not supported "
                             "format!Circle center latitude error or not supported format!", p.err_msg)
            self.assertIsNone(p.lon.ang_dd)
            self.assertIsNone(p.lat.ang_dd)
