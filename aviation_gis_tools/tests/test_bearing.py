import unittest
from aviation_gis_tools.bearing import *


class BearingTests(unittest.TestCase):

    def test_is_coordinate_within_range(self):
        self.assertEqual(Bearing.is_within_range(-0.1), False)
        self.assertEqual(Bearing.is_within_range(360.1), False)
        self.assertEqual(Bearing.is_within_range(0), True)
        self.assertEqual(Bearing.is_within_range(0.1), True)
        self.assertEqual(Bearing.is_within_range(359.9), True)
        self.assertEqual(Bearing.is_within_range(360.), True)

    def test_convert_compacted_dms_to_dd_valid_bearing(self):
        bearings = [
            ('0000000', 0),
            ('1800000.000', 180),
            ('0453000.000', 45.5),
            ('0003000.000', 0.5),
            ('1234601.445', 123.76706805555555),
            ('3600000.0', 360)
        ]

        for brng_dms, brng_dd in bearings:
            self.assertAlmostEqual(brng_dd, Bearing.convert_compacted_dms_to_dd(brng_src=brng_dms,
                                                                                pattern=BEARING_COMPACTED["DMS_COMPACTED"]))

    def test_convert_compacted_dms_to_dd_invalid_bearing(self):
        bearings = [
            '12333411.17',
            '12333.55',
            '0000000E',
            '1806000.000',
            '04560.000',
            '3610000.000',
            '1234661.445',
            '3600000.01'
        ]

        for brng in bearings:
            self.assertIsNone(Bearing.convert_compacted_dms_to_dd(brng_src=brng,
                                                                  pattern=BEARING_COMPACTED["DMS_COMPACTED"]))

    def test_convert_compacted_dm_to_dd_valid_bearing(self):
        bearings = [
            ('00000', 0),
            ('18000.000', 180),
            ('04530.000', 45.5),
            ('00030.000', 0.5),
            ('12346.445', 123.7740833333333333),
            ('36000.0', 360)
        ]

        for brng_dm, brng_dd in bearings:
            self.assertAlmostEqual(brng_dd, Bearing.convert_compacted_dm_to_dd(brng_src=brng_dm,
                                                                               pattern=BEARING_COMPACTED["DM_COMPACTED"]))

    def test_convert_compacted_dm_to_dd_invalid_bearing(self):
        bearings = [
            '0000000E',
            '18060.000',
            '04560.000',
            '36100.000',
            '12361.445',
            '36000.01',
            '1231.55'
        ]

        for brng in bearings:
            self.assertIsNone(Bearing.convert_compacted_dm_to_dd(brng_src=brng,
                                                                 pattern=BEARING_COMPACTED["DM_COMPACTED"]))

    def test_bearing_err_msg(self):
        b = Bearing('1234601.445')
        self.assertEqual('', b.err_msg)

        b = Bearing('12346.445')
        self.assertEqual('', b.err_msg)

        b = Bearing('12366.445')
        self.assertEqual('Bearing value error or format not supported.', b.err_msg)

        b = Bearing(' ')
        self.assertEqual('Bearing is required.', b.err_msg)

        b = Bearing('   ', "From bearing")
        self.assertEqual('From bearing is required.', b.err_msg)

        b = Bearing('12366.445', "To bearing")
        self.assertEqual('To bearing value error or format not supported.', b.err_msg)