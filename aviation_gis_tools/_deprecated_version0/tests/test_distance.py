import unittest
from aviation_gis_tools._deprecated_version0.distance import Distance


class DistanceTests(unittest.TestCase):

    def test_uom_is_not_valid(self):
        d = Distance(1, '')
        self.assertEqual(False, d.check_distance_uom())

        d = Distance(1, 'TEST_UOM')
        self.assertEqual(False, d.check_distance_uom())

    def test_distance_value_is_not_valid(self):
        d = Distance('', UOM_M)
        self.assertEqual(False, d.is_valid)

        d = Distance('456,12,1', UOM_M)
        self.assertEqual(False, d.is_valid)

    def test_distance_values_is_valid(self):
        d = Distance(457, UOM_M)
        self.assertEqual(True, d.is_valid)

        d = Distance('456,12', UOM_M)
        self.assertEqual(True, d.is_valid)

    def test_error_message_is_empty(self):
        d = Distance(1, UOM_M)
        self.assertEqual('', d.err_msg)

        d = Distance(100.66, UOM_NM)
        self.assertEqual('', d.err_msg)

        d = Distance('36,6', UOM_FT)
        self.assertEqual('', d.err_msg)

    def test_error_message_uom_error(self):
        d = Distance(1, '')
        self.assertEqual('Distance UOM error.', d.err_msg)

        d = Distance(100.66, 'TEST_UOM')
        self.assertEqual('Distance UOM error.', d.err_msg)

    def test_error_message_value_error(self):
        d = Distance('', UOM_M)
        self.assertEqual('Distance is required.', d.err_msg)

        d = Distance('10,6,6', UOM_SM)
        self.assertEqual('Distance value error.', d.err_msg)

    def test_error_message_value_and_uom_error(self):
        d = Distance('', '../test')
        self.assertEqual('Distance is required.Distance UOM error.', d.err_msg)

    def test_custom_distance_label_err_msg(self):
        d = Distance(1, '', 'Circle radius')
        self.assertEqual('Circle radius UOM error.', d.err_msg)

        d = Distance(100.66, '', 'Circle sector radius')
        self.assertEqual('Circle sector radius UOM error.', d.err_msg)

        d = Distance('', UOM_M, 'Inner radius')
        self.assertEqual('Inner radius is required.', d.err_msg)

        d = Distance('10,6,6', UOM_SM, 'Outer radius')
        self.assertEqual('Outer radius value error.', d.err_msg)

        d = Distance('', '../test', 'Circle radius')
        self.assertEqual('Circle radius is required.Circle radius UOM error.', d.err_msg)

    def test_convert_dist_to_m(self):
        d = Distance(135.75)
        self.assertEqual(135.75, d.convert_distance_to_meters())

        d = Distance(1.0455, UOM_KM)
        self.assertEqual(1045.5, d.convert_distance_to_meters())

        d = Distance(17.355, UOM_NM)
        self.assertEqual(32141.46, d.convert_distance_to_meters())

        d = Distance(783.2, UOM_FT)
        self.assertAlmostEqual(238.71936, d.convert_distance_to_meters())

        d = Distance(5.8, UOM_SM)
        self.assertEqual(9334.1952, d.convert_distance_to_meters())

    def test_convert_meters_to_uom(self):
        self.assertEqual(1000, Distance.convert_meters_to_uom(1000, UOM_M))
        self.assertEqual(0.45522, Distance.convert_meters_to_uom(455.22, UOM_KM))
        self.assertAlmostEqual(1, Distance.convert_meters_to_uom(1852, UOM_NM))
        self.assertAlmostEqual(841.53543307086600, Distance.convert_meters_to_uom(256.5, UOM_FT))
        self.assertAlmostEqual(4.880994989262710000, Distance.convert_meters_to_uom(7855.2, UOM_SM))

    def test_convert_m_to_uom(self):
        d = Distance(1455)
        self.assertEqual(1455, d.convert_distance_to_uom(UOM_M))
        self.assertEqual(1.455, d.convert_distance_to_uom(UOM_KM))
        self.assertEqual(0.7856371490280778, d.convert_distance_to_uom(UOM_NM))
        self.assertEqual(4773.622047244095, d.convert_distance_to_uom(UOM_FT))
        self.assertEqual(0.9040950847053209, d.convert_distance_to_uom(UOM_SM))

    def test_convert_km_to_uom(self):
        d = Distance(1.455, UOM_KM)
        self.assertEqual(1455, d.convert_distance_to_uom(UOM_M))
        self.assertEqual(1.455, d.convert_distance_to_uom(UOM_KM))
        self.assertAlmostEqual(0.7856371490280778, d.convert_distance_to_uom(UOM_NM))
        self.assertAlmostEqual(4773.622047244095, d.convert_distance_to_uom(UOM_FT))
        self.assertAlmostEqual(0.9040950847053209, d.convert_distance_to_uom(UOM_SM))

    def test_convert_NM_to_uom(self):
        d = Distance(2.79, UOM_NM)
        self.assertEqual(5167.08, d.convert_distance_to_uom(UOM_M))
        self.assertEqual(5.16708, d.convert_distance_to_uom(UOM_KM))
        self.assertEqual(2.79, d.convert_distance_to_uom(UOM_NM))
        self.assertAlmostEqual(16952.3622047244000, d.convert_distance_to_uom(UOM_FT))
        self.assertAlmostEqual(3.21067465998568, d.convert_distance_to_uom(UOM_SM))

    def test_convert_ft_to_uom(self):
        d = Distance(3722.5, UOM_FT)
        self.assertAlmostEqual(1134.6180000000002, d.convert_distance_to_uom(UOM_M))
        self.assertAlmostEqual(1.1346180000000002, d.convert_distance_to_uom(UOM_KM))
        self.assertAlmostEqual(0.6126447084233262, d.convert_distance_to_uom(UOM_NM))
        self.assertEqual(3722.5, d.convert_distance_to_uom(UOM_FT))
        self.assertAlmostEqual(0.7050189393939394, d.convert_distance_to_uom(UOM_SM))

    def test_convert_SM_to_uom(self):
        d = Distance(2.3, UOM_SM)
        self.assertAlmostEqual(3701.4912, d.convert_distance_to_uom(UOM_M))
        self.assertAlmostEqual(3.7014912, d.convert_distance_to_uom(UOM_KM))
        self.assertAlmostEqual(1.9986453563714903, d.convert_distance_to_uom(UOM_NM))
        self.assertEqual(12144.0, d.convert_distance_to_uom(UOM_FT))
        self.assertAlmostEqual(2.3, d.convert_distance_to_uom(UOM_SM))
