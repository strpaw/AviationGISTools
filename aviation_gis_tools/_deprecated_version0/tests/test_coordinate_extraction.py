import unittest


class CoordinatePairExtractionTests(unittest.TestCase):

    def test_get_coordinate_example_dmsh_comp(self):

        coord_extractor = CoordinatePairExtraction(coord_sequence=SEQUENCE_LAT_LON,
                                                   coord_format=DMSH_COMP,
                                                   coord_sep=COORD_PAIR_SEP_SPACE)
        sample_lon = coord_extractor.get_coordinate_example(example_longitude)
        sample_lat = coord_extractor.get_coordinate_example(example_latitude)
        self.assertEqual('0133738.21E', sample_lon)
        self.assertEqual('745632.55N', sample_lat)

    def test_get_coordinate_example_hdms_comp(self):

        coord_extractor = CoordinatePairExtraction(coord_sequence=SEQUENCE_LAT_LON,
                                                   coord_format=HDMS_COMP,
                                                   coord_sep=COORD_PAIR_SEP_SPACE)
        sample_lon = coord_extractor.get_coordinate_example(example_longitude)
        sample_lat = coord_extractor.get_coordinate_example(example_latitude)
        self.assertEqual('E0133738.21', sample_lon)
        self.assertEqual('N745632.55', sample_lat)

    def test_get_coordinates_pair_example(self):
        settings = [
            (SEQUENCE_LON_LAT, DMSH_COMP, COORD_PAIR_SEP_NONE, '0133738.21E745632.55N'),
            (SEQUENCE_LON_LAT, DMSH_COMP, COORD_PAIR_SEP_SPACE, '0133738.21E 745632.55N'),
            (SEQUENCE_LON_LAT, DMSH_COMP, COORD_PAIR_SEP_HYPHEN, '0133738.21E-745632.55N'),
            (SEQUENCE_LON_LAT, DMSH_COMP, COORD_PAIR_SEP_SLASH, '0133738.21E/745632.55N'),
            (SEQUENCE_LON_LAT, DMSH_COMP, COORD_PAIR_SEP_BACKSLASH, r'0133738.21E\745632.55N'),
            (SEQUENCE_LAT_LON, HDMS_SEP, COORD_PAIR_SEP_NONE, 'N 74 56 32.55E 013 37 38.21'),
            (SEQUENCE_LAT_LON, HDMS_SEP, COORD_PAIR_SEP_SPACE, 'N 74 56 32.55 E 013 37 38.21'),
            (SEQUENCE_LAT_LON, HDMS_SEP, COORD_PAIR_SEP_HYPHEN, 'N 74 56 32.55-E 013 37 38.21'),
            (SEQUENCE_LAT_LON, HDMS_SEP, COORD_PAIR_SEP_SLASH, 'N 74 56 32.55/E 013 37 38.21'),
            (SEQUENCE_LAT_LON, HDMS_SEP, COORD_PAIR_SEP_BACKSLASH, r'N 74 56 32.55\E 013 37 38.21'),
        ]

        for coord_seq, coord_format, coord_sep, coord_example in settings:
            coord_extractor = CoordinatePairExtraction(coord_sequence=coord_seq,
                                                       coord_format=coord_format,
                                                       coord_sep=coord_sep)
            example_pair = coord_extractor.get_coordinates_pair_example()
            self.assertEqual(coord_example, example_pair)

    def test_extract_coordinates_lonlat_dmsh_comp(self):
        coordinates = [
            ('0300108E', '512824.111N'), ('0300126E', '512943N'),  ('0300612.7889E', '512901N'),
            ('0301202.445E', '512913.4556N'), ('0302034E', '512325.988N'), ('0301735E', '512220N')
        ]

        plain_texts = {
            COORD_PAIR_SEP_NONE: """ 0300108E512824.111N  0300126E512943N 
                0300612.7889E512901N   0301202.445E512913.4556N 
                0302034E512325.988N   0301735E512220N """,
            COORD_PAIR_SEP_SPACE: """ 0300108E 512824.111N  0300126E 512943N
                0300612.7889E 512901N   0301202.445E 512913.4556N
                0302034E 512325.988N   0301735E 512220N """,
            COORD_PAIR_SEP_HYPHEN: """ 0300108E-512824.111N  0300126E-512943N
                0300612.7889E-512901N   0301202.445E-512913.4556N
                0302034E-512325.988N   0301735E-512220N """,
            COORD_PAIR_SEP_SLASH: """ 0300108E/512824.111N  0300126E/512943N
                0300612.7889E/512901N   0301202.445E/512913.4556N
                0302034E/512325.988N   0301735E/512220N """,
            COORD_PAIR_SEP_BACKSLASH: r"""0300108E\512824.111N  0300126E\512943N
                0300612.7889E\512901N   0301202.445E\512913.4556N
                0302034E\512325.988N   0301735E\512220N """
        }

        for key, value in plain_texts.items():
            coord_extractor = CoordinatePairExtraction(SEQUENCE_LON_LAT, DMSH_COMP, key)
            extracted_coordinates = coord_extractor.extract_coordinates(value)
            self.assertEqual(coordinates, extracted_coordinates)

    def test_extract_coordinates_latlon_dmsh_comp(self):

        coordinates = [
            ('512942N', '0183840E'), ('513410N', '0183538E'), ('522454.3N', '0165114.3E'),
            ('514038N', '0184547E'), ('522458.0N',  '0165055.4E'), ('514312N', '0185425E')
        ]

        plain_texts = {
            COORD_PAIR_SEP_NONE: """512942N0183840E
                513410N0183538E 522454.3N0165114.3E,
                514038N0184547E 522458.0N0165055.4E,
                514312N0185425E """,
            COORD_PAIR_SEP_SPACE: """512942N 0183840E
                513410N 0183538E 522454.3N 0165114.3E,
                514038N 0184547E 522458.0N 0165055.4E,
                514312N 0185425E""",
            COORD_PAIR_SEP_HYPHEN: """512942N-0183840E
                513410N-0183538E 522454.3N-0165114.3E,
                514038N-0184547E 522458.0N-0165055.4E,
                514312N-0185425E""",
            COORD_PAIR_SEP_SLASH: """512942N/0183840E
                513410N/0183538E 522454.3N/0165114.3E,
                514038N/0184547E 522458.0N/0165055.4E,
                514312N/0185425E""",
            COORD_PAIR_SEP_BACKSLASH: r"""512942N\0183840E
                513410N\0183538E 522454.3N\0165114.3E,
                514038N\0184547E 522458.0N\0165055.4E,
                514312N\0185425E"""
        }

        for key, value in plain_texts.items():
            coord_extractor = CoordinatePairExtraction(SEQUENCE_LAT_LON, DMSH_COMP, key)
            extracted_coordinates = coord_extractor.extract_coordinates(value)
            self.assertEqual(coordinates, extracted_coordinates)

    def test_extract_coordinates_lonlat_dmsh_sep(self):
        coordinates = [
            ('030 01 08 E', '51 28 24.111 N'), ('030 01 26 E', '51 29 43 N'),  ('030 06 12.7889 E', '51 29 01 N'),
            ('030 12 02.445 E', '51 29 13.4556 N'), ('030 20 34 E', '51 23 25.988 N'), ('030 17 35 E', '51 22 20 N')
        ]

        plain_texts = {
            COORD_PAIR_SEP_NONE: """ 030 01 08 E51 28 24.111 N  030 01 26 E51 29 43 N 
                030 06 12.7889 E51 29 01 N   030 12 02.445 E51 29 13.4556 N 
                030 20 34 E51 23 25.988 N   030 17 35 E51 22 20 N """,
            COORD_PAIR_SEP_SPACE: """ 030 01 08 E 51 28 24.111 N  030 01 26 E 51 29 43 N 
                030 06 12.7889 E 51 29 01 N   030 12 02.445 E 51 29 13.4556 N 
                030 20 34 E 51 23 25.988 N   030 17 35 E 51 22 20 N """,
            COORD_PAIR_SEP_HYPHEN: """ 030 01 08 E-51 28 24.111 N  030 01 26 E-51 29 43 N 
                030 06 12.7889 E-51 29 01 N   030 12 02.445 E-51 29 13.4556 N 
                030 20 34 E-51 23 25.988 N   030 17 35 E-51 22 20 N """,
            COORD_PAIR_SEP_SLASH: """ 030 01 08 E/51 28 24.111 N  030 01 26 E/51 29 43 N 
                030 06 12.7889 E/51 29 01 N   030 12 02.445 E/51 29 13.4556 N 
                030 20 34 E/51 23 25.988 N   030 17 35 E/51 22 20 N """,
            COORD_PAIR_SEP_BACKSLASH: r""" 030 01 08 E\51 28 24.111 N  030 01 26 E\51 29 43 N 
                030 06 12.7889 E\51 29 01 N   030 12 02.445 E\51 29 13.4556 N 
                030 20 34 E\51 23 25.988 N   030 17 35 E\51 22 20 N """,
        }

        for key, value in plain_texts.items():
            coord_extractor = CoordinatePairExtraction(SEQUENCE_LON_LAT, DMSH_SEP, key)
            extracted_coordinates = coord_extractor.extract_coordinates(value)
            self.assertEqual(coordinates, extracted_coordinates)

    def test_extract_coordinates_latlon_dmsh_sep(self):
        coordinates = [
            ('51 28 24.111 N', '030 01 08 E'), ('51 29 43 N', '030 01 26 E'),  ('51 29 01 N', '030 06 12.7889 E'),
            ('51 29 13.4556 N', '030 12 02.445 E', ), ('51 23 25.988 N', '030 20 34 E', ), ('51 22 20 N', '030 17 35 E')
        ]

        plain_texts = {
            COORD_PAIR_SEP_NONE: """ 51 28 24.111 N030 01 08 E  51 29 43 N030 01 26 E 
                51 29 01 N030 06 12.7889 E   51 29 13.4556 N030 12 02.445 E 
                51 23 25.988 N030 20 34 E   51 22 20 N030 17 35 E """,
            COORD_PAIR_SEP_SPACE: """ 51 28 24.111 N 030 01 08 E  51 29 43 N 030 01 26 E
                51 29 01 N 030 06 12.7889 E   51 29 13.4556 N 030 12 02.445 E
                51 23 25.988 N 030 20 34 E   51 22 20 N 030 17 35 E """,
            COORD_PAIR_SEP_HYPHEN: """ 51 28 24.111 N-030 01 08 E  51 29 43 N-030 01 26 E
                51 29 01 N-030 06 12.7889 E   51 29 13.4556 N-030 12 02.445 E
                51 23 25.988 N-030 20 34 E   51 22 20 N-030 17 35 E """,
            COORD_PAIR_SEP_SLASH: """ 51 28 24.111 N/030 01 08 E  51 29 43 N/030 01 26 E
                51 29 01 N/030 06 12.7889 E   51 29 13.4556 N/030 12 02.445 E
                51 23 25.988 N/030 20 34 E   51 22 20 N/030 17 35 E """,
            COORD_PAIR_SEP_BACKSLASH: r""" 51 28 24.111 N\030 01 08 E  51 29 43 N\030 01 26 E
                51 29 01 N\030 06 12.7889 E   51 29 13.4556 N\030 12 02.445 E
                51 23 25.988 N\030 20 34 E   51 22 20 N\030 17 35 E """,
        }

        for key, value in plain_texts.items():
            coord_extractor = CoordinatePairExtraction(SEQUENCE_LAT_LON, DMSH_SEP, key)
            extracted_coordinates = coord_extractor.extract_coordinates(value)
            self.assertEqual(coordinates, extracted_coordinates)
