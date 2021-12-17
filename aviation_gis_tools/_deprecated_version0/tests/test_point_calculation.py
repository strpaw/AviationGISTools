import unittest


class PointTests(unittest.TestCase):

    def test_check_point_valid_data(self):
        ref_point = [
            ('Circle center', '1234601.445E', 123.76706805555555, '453000.000S', -45.5),
            ('Circle center', 'E17701', 177.016666666666666666, 'N7701', 77.016666666666666666, )
        ]

        for ref_id, ref_lon_src, ref_lon_dd, ref_lat_src, ref_lat_dd in ref_point:
            p = PointCalculation(ref_id, ref_lon_src, ref_lat_src)
            self.assertEqual("", p.ref_err)
            self.assertAlmostEqual(ref_lon_dd, p.ref_lon.ang_dd)
            self.assertAlmostEqual(ref_lat_dd, p.ref_lat.ang_dd)

    def test_check_point_invalid_data(self):
        ref_point = [
            ('Circle center', '1234601.445S', 123.76706805555555, '456000.000', -45.5),
            ('Circle center', 'E17760', 177.016666666666666666, 'N 7701', 77.016666666666666666),
            ('', 'E17760', 177.016666666666666666, 'N 7701', 77.016666666666666666)
        ]

        for ref_id, ref_lon_src, ref_lon_dd, ref_lat_src, ref_lat_dd in ref_point:
            p = PointCalculation(ref_id, ref_lon_src, ref_lat_src)

            if ref_id.strip() != "":
                self.assertEqual("{0} longitude error or not supported "
                                 "format!{0} latitude error or not supported format!".format(p.ref_id), p.ref_err)
            else:
                self.assertEqual("Reference point id required!{0} longitude error or not supported "
                                 "format!{0} latitude error or not supported format!".format(p.ref_id), p.ref_err)
            self.assertIsNone(p.ref_lon.ang_dd)
            self.assertIsNone(p.ref_lat.ang_dd)
