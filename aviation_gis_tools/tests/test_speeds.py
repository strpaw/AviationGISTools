import unittest
from aviation_gis_tools.speeds import *


class SpeedTests(unittest.TestCase):

    def test_speed_to_ms(self):
        self.assertAlmostEqual(1, speed_to_ms(1, SPEED_MS))
        self.assertAlmostEqual(0.2777777777777778, speed_to_ms(1, SPEED_KMH))
        self.assertAlmostEqual(0.5144444444444445, speed_to_ms(1, SPEED_KT))

    def test_speed_ms_to_unit(self):
        self.assertAlmostEqual(1, speed_ms_to_unit(1, SPEED_MS))
        self.assertAlmostEqual(3.6, speed_ms_to_unit(1, SPEED_KMH))
        self.assertAlmostEqual(1.9438444924406046, speed_ms_to_unit(1, SPEED_KT))

    def test_convert_speed(self):
        self.assertAlmostEqual(45.78, convert_speed(45.78, SPEED_MS, SPEED_MS))
        self.assertAlmostEqual(164.808, convert_speed(45.78, SPEED_MS, SPEED_KMH))
        self.assertAlmostEqual(88.98920086393089, convert_speed(45.78, SPEED_MS, SPEED_KT))

        self.assertAlmostEqual(81.94444444444444, convert_speed(295, SPEED_KMH, SPEED_MS))
        self.assertAlmostEqual(295.0, convert_speed(295, SPEED_KMH, SPEED_KMH))
        self.assertAlmostEqual(159.28725701943844, convert_speed(295, SPEED_KMH, SPEED_KT))

        self.assertAlmostEqual(154.33333333333334, convert_speed(300, SPEED_KT, SPEED_MS))
        self.assertAlmostEqual(555.6, convert_speed(300, SPEED_KT, SPEED_KMH))
        self.assertAlmostEqual(300.0, convert_speed(300, SPEED_KT, SPEED_KT))
