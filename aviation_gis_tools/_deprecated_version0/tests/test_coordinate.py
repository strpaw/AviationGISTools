import unittest


class CoordinateTests(unittest.TestCase):

    def test_is_coordinate_within_range(self):
        self.assertEqual(Coordinate.is_coordinate_within_range(-180.1, AT_LONGITUDE), False)
        self.assertEqual(Coordinate.is_coordinate_within_range(-180, AT_LONGITUDE), True)
        self.assertEqual(Coordinate.is_coordinate_within_range(180, AT_LONGITUDE), True)
        self.assertEqual(Coordinate.is_coordinate_within_range(180.1, AT_LONGITUDE), False)

        self.assertEqual(Coordinate.is_coordinate_within_range(-90.1, AT_LATITUDE), False)
        self.assertEqual(Coordinate.is_coordinate_within_range(-90, AT_LATITUDE), True)
        self.assertEqual(Coordinate.is_coordinate_within_range(90, AT_LATITUDE), True)
        self.assertEqual(Coordinate.is_coordinate_within_range(90.1, AT_LATITUDE), False)

    def test_convert_compacted_to_dd_valid_coordinates(self):
        longitudes = [
            ('1800000E', 180),
            ('1800000.0W', -180),
            ('0453000.000E', 45.5),
            ('0003000.000W', -0.5),
            ('1234601.445E', 123.76706805555555),
            ('E1800000', 180),
            ('W1800000.0', -180),
            ('E0453000.000', 45.5),
            ('W0003000.000', -0.5),
            ('E1234601.445', 123.76706805555555),
            ('E10030.000', 100.5),
            ('W00100.000', -1.0),
            ('02533.41E', 25.5568333333333333),
            ('12533W', -125.55),
            ('E17701', 177.016666666666666666)
        ]

        for lon_dmsh, lon_dd in longitudes:
            self.assertAlmostEqual(lon_dd, Coordinate.convert_compacted_to_dd(lon_dmsh, AT_LONGITUDE))

        latitudes = [
            ('900000N', 90),
            ('900000.0S', -90),
            ('453000.000S', -45.5),
            ('003000.000N', 0.5),
            ('234601.445N', 23.76706805555555),
            ('N900000', 90),
            ('S900000.0', -90),
            ('S453000.000', -45.5),
            ('N003000.000', 0.5),
            ('N234601.445', 23.76706805555555),
            ('N1030.000', 10.5),
            ('S0100.000', -1.0),
            ('2533.41S', -25.5568333333333333),
            ('2533.41N', 25.5568333333333333),
            ('2533S', -25.55),
            ('N7701', 77.016666666666666666)
        ]

        for lat_dmsh, lat_dd in latitudes:
            self.assertAlmostEqual(lat_dd, Coordinate.convert_compacted_to_dd(lat_dmsh, AT_LATITUDE))

    def test_convert_compacted_to_dd_invalid_coordinates(self):
        longitudes = [
            'S1800000',
            '1800000.1E',
            'E0456000.000',
            'W01002545.000',
            'E1002560.445'
            'W12060.000',
            '12020.55'
        ]

        for lon in longitudes:
            self.assertIsNone(Coordinate.convert_compacted_to_dd(lon, AT_LONGITUDE))

        latitudes = [
            'E900000'
            'S910000.0'
            'S0453000.000'
            'N003060.000'
            'N236101.445',
            'E2099.00',
            '0160S'
        ]

        for lat in latitudes:
            self.assertIsNone(Coordinate.convert_compacted_to_dd(lat, AT_LATITUDE))

    def test_validate_coordinate_empty_coordinate_source(self):

        c = Coordinate("", AT_LONGITUDE)
        self.assertEqual("Longitude is required!", c.err_msg)
        self.assertEqual(None, c.ang_dd)

        c = Coordinate("", AT_LONGITUDE, "Circle center longitude")
        self.assertEqual("Circle center longitude is required!", c.err_msg)
        self.assertEqual(None, c.ang_dd)

        c = Coordinate("", AT_LATITUDE)
        self.assertEqual("Latitude is required!", c.err_msg)
        self.assertEqual(None, c.ang_dd)

        c = Coordinate("", AT_LATITUDE, "Reference  latitude")
        self.assertEqual("Reference  latitude is required!", c.err_msg)
        self.assertEqual(None, c.ang_dd)

    def test_validate_coordinate(self):
        longitudes = [
            ('1800000E', 180),
            ('1800000.0W', -180),
            ('0453000.000E', 45.5),
            ('0003000.000W', -0.5),
            ('1234601.445E', 123.76706805555555),
            ('E1800000', 180),
            ('W1800000.0', -180),
            ('E0453000.000', 45.5),
            ('W0003000.000', -0.5),
            ('E1234601.445', 123.76706805555555)
        ]

        for lon_src, lon_dd in longitudes:
            c = Coordinate(lon_src, AT_LONGITUDE)
            self.assertAlmostEqual(lon_dd, c.ang_dd)
            self.assertEqual("", c.err_msg)

        latitudes = [
            ('900000N', 90),
            ('900000.0S', -90),
            ('453000.000S', -45.5),
            ('003000.000N', 0.5),
            ('234601.445N', 23.76706805555555),
            ('N900000', 90),
            ('S900000.0', -90),
            ('S453000.000', -45.5),
            ('N003000.000', 0.5),
            ('N234601.445', 23.76706805555555)
        ]
        for lat_src, lon_dd in latitudes:
            c = Coordinate(lat_src, AT_LATITUDE)
            self.assertAlmostEqual(lon_dd, c.ang_dd)
            self.assertEqual("", c.err_msg)
