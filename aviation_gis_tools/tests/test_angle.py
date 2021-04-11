import unittest
from aviation_gis_tools.angle import *


class AngleTests(unittest.TestCase):

    def test_dd_to_dms_parts(self):
        self.assertEqual(Angle.get_dms_parts(0), (0, 0, 0.000))
        self.assertEqual(Angle.get_dms_parts(-1), (1, 0, 0.000))
        self.assertEqual(Angle.get_dms_parts(10), (10, 0, 0.000))
        self.assertEqual(Angle.get_dms_parts(45.5), (45, 30, 0.000))
        self.assertEqual(Angle.get_dms_parts(1.0169444444444400), (1, 1, 1.0))
        self.assertEqual(Angle.get_dms_parts(100.1694444444444000), (100, 10, 10.000))
        self.assertEqual(Angle.get_dms_parts(-120.3388888888889000), (120, 20, 20.000))
        self.assertEqual(Angle.get_dms_parts(145.9589599661111, prec=6), (145, 57, 32.255878))

    def test_convert_dd_to_dms_longitude(self):
        self.assertEqual('E145 57 32.256',
                         Angle.convert_dd_to_dms(145.9589599661111000, AT_LONGITUDE, dms_format=AF_HDMS_SPACE_SEP))
        self.assertEqual('W145-57-32.256',
                         Angle.convert_dd_to_dms(-145.9589599661111000, AT_LONGITUDE, dms_format=AF_HDMS_HYPHEN_SEP))
        self.assertEqual('145 57 32.26E',
                         Angle.convert_dd_to_dms(145.9589599661111000, AT_LONGITUDE, dms_format=AF_DMSH_SPACE_SEP, prec=2))
        self.assertEqual('145-57-32.3E',
                         Angle.convert_dd_to_dms(145.9589599661111000, AT_LONGITUDE, dms_format=AF_DMSH_HYPHEN_SEP, prec=1))

    def test_convert_dd_to_dms_latitude(self):
        self.assertEqual('N45 57 32.256',
                         Angle.convert_dd_to_dms(45.9589599661111000, AT_LATITUDE, dms_format=AF_HDMS_SPACE_SEP))
        self.assertEqual('S45-57-32.256',
                         Angle.convert_dd_to_dms(-45.9589599661111000, AT_LATITUDE, dms_format=AF_HDMS_HYPHEN_SEP))
        self.assertEqual('45 57 32.26N',
                         Angle.convert_dd_to_dms(45.9589599661111000, AT_LATITUDE, dms_format=AF_DMSH_SPACE_SEP, prec=2))
        self.assertEqual('45-57-32.3S',
                         Angle.convert_dd_to_dms(-45.9589599661111000, AT_LATITUDE, dms_format=AF_DMSH_HYPHEN_SEP, prec=1))

    def test_normalize_angle(self):
        self.assertEqual('32 44 56.77N', Angle.normalize_angle(' 32 44 56.77N'))
        self.assertEqual('32 44 56.77N', Angle.normalize_angle('32 44 56.77N       '))
        self.assertEqual('32 44 56.77N', Angle.normalize_angle('32 44 56,77N'))
        self.assertEqual('32 44 56.77N', Angle.normalize_angle('32 44 56.77n'))
        self.assertEqual('32 44 56.77N', Angle.normalize_angle('32   44     56.77n'))
        self.assertEqual('32 - 44 - 56.77N', Angle.normalize_angle('32   - 44   -  56.77n'))

    def test_dmsh_parts_to_dd(self):
        self.assertEqual(None, Angle.dmsh_parts_to_dd((100, 61, 59, 'W')))
        self.assertEqual(None, Angle.dmsh_parts_to_dd((100, 0, 60, 'E')))
        self.assertEqual(None, Angle.dmsh_parts_to_dd((100, -1, 0, 'S')))
        self.assertEqual(None, Angle.dmsh_parts_to_dd((100, 5, 10, 'A')))
        self.assertEqual(100.59555555555555, Angle.dmsh_parts_to_dd((100, 35, 44, 'N')))
        self.assertEqual(-100.59555555555555, Angle.dmsh_parts_to_dd((100, 35, 44, 'W')))
