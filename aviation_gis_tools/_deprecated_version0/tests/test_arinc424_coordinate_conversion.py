import unittest


class DistToLonLatTests(unittest.TestCase):
    def test_is_longitude_dmh(self):
        valid_lon_dmh = ['000E', '001W', '029E', '100E', '179E']

        for lon in valid_lon_dmh:
            self.assertTrue(Arinc424CoordinatesConversion.is_longitude_full_dh(lon))

        invalid_lon_dmh = ['000', '00125W', '02900S', '10022E', '181E']
        for lon in invalid_lon_dmh:
            self.assertFalse(Arinc424CoordinatesConversion.is_longitude_full_dh(lon))

    def test_is_is_latitude_dmh(self):
        valid_lat_dmh = ['00N', '01N', '29S', '90N']

        for lat in valid_lat_dmh:
            self.assertTrue(Arinc424CoordinatesConversion.is_latitude_full_dh(lat))

        invalid_lat_dmh = ['0000', '10E', '2330S', '91N']
        for lat in invalid_lat_dmh:
            self.assertFalse(Arinc424CoordinatesConversion.is_latitude_full_dh(lat))

    def test_get_arinc424_format_pattern(self):
        self.assertEqual(Arinc424CoordinatesConversion.PATTERN_LONGITUDE_LESS_HUNDRED,
                         Arinc424CoordinatesConversion.get_arinc424_format_pattern('099E'))
        self.assertEqual(Arinc424CoordinatesConversion.PATTERN_LONGITUDE_EQUAL_GRATER_HUNDRED,
                         Arinc424CoordinatesConversion.get_arinc424_format_pattern('100W'))
        self.assertEqual(Arinc424CoordinatesConversion.PATTERN_LONGITUDE_EQUAL_GRATER_HUNDRED,
                         Arinc424CoordinatesConversion.get_arinc424_format_pattern('101W'))

    def test_arinc424_to_coordinates(self):
        self.assertEqual('16000W 5000N', Arinc424CoordinatesConversion.arinc424_to_coordinates('50N60'))
        self.assertEqual('06000W 5000N', Arinc424CoordinatesConversion.arinc424_to_coordinates('5060N'))
        self.assertEqual('16000E 5000N', Arinc424CoordinatesConversion.arinc424_to_coordinates('50E60'))
        self.assertEqual('06000E 5000N', Arinc424CoordinatesConversion.arinc424_to_coordinates('5060E'))
        self.assertEqual('16000W 5000S', Arinc424CoordinatesConversion.arinc424_to_coordinates('50W60'))
        self.assertEqual('06000W 5000S', Arinc424CoordinatesConversion.arinc424_to_coordinates('5060W'))
        self.assertEqual('06000E 5000S', Arinc424CoordinatesConversion.arinc424_to_coordinates('5060S'))
        self.assertEqual('16000E 5000S', Arinc424CoordinatesConversion.arinc424_to_coordinates('50S60'))

    def test_coord_to_arinc424(self):
        self.assertEqual('50N60', Arinc424CoordinatesConversion.coord_to_arinc424(lat='50N', lon='160W'))
        self.assertEqual('5060N', Arinc424CoordinatesConversion.coord_to_arinc424(lat='50N', lon='060W'))
        self.assertEqual('50E60', Arinc424CoordinatesConversion.coord_to_arinc424(lat='50N', lon='160E'))
        self.assertEqual('5060E', Arinc424CoordinatesConversion.coord_to_arinc424(lat='50N', lon='060E'))
        self.assertEqual('50W60', Arinc424CoordinatesConversion.coord_to_arinc424(lat='50S', lon='160W'))
        self.assertEqual('5060W', Arinc424CoordinatesConversion.coord_to_arinc424(lat='50S', lon='060W'))
        self.assertEqual('5060S', Arinc424CoordinatesConversion.coord_to_arinc424(lat='50S', lon='060E'))
        self.assertEqual('50S60', Arinc424CoordinatesConversion.coord_to_arinc424(lat='50S', lon='160E'))
