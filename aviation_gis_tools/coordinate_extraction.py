# -*- coding: utf-8 -*-
"""
Extract coordinates from plain text.
"""
import re
from collections import namedtuple

_sample_coordinate = namedtuple('sample_coordinate', 'deg min sec hem')

_EXAMPLE_LONGITUDE = _sample_coordinate(deg='013', min='37', sec='38.21', hem='E')
_EXAMPLE_LATITUDE = _sample_coordinate(deg='74', min='56', sec='32.55', hem='N')

# Longitude, latitude sequence
SEQUENCE_LON_LAT = 'SEQUENCE_LON_LAT'
SEQUENCE_LAT_LON = 'SEQUENCE_LAT_LON'

# Coordinate format constants
DMSH_COMP = 'DMSH_COMP'
HDMS_COMP = 'HDMS_COMP'
DMSH_SEP = 'DMSH_SEP'
HDMS_SEP = 'HDMS_SEP'

# Longitude, latitude separators separates latitude and longitude in pair, not pairs!
COORD_PAIR_SEP_NONE = r''  # Longitude and latitude not separated
COORD_PAIR_SEP_SPACE = r' '
COORD_PAIR_SEP_HYPHEN = r'-'
COORD_PAIR_SEP_SLASH = r'/'
COORD_PAIR_SEP_BACKSLASH = '\\'

_coord_pair = namedtuple('coord_pair', 'lon lat')

_DMSH_COMPACTED_LON = r'\d{7}\.\d+[EW]|\d{7}[EW]'
_DMSH_COMPACTED_LAT = r'\d{6}\.\d+[NS]|\d{6}[NS]'
_HDMS_COMPACTED_LON = r'[EW]\d{7}\.\d+|[EW]\d{7}'
_HDMS_COMPACTED_LAT = r'[NS]\d{6}\.\d+|[NS]\d{6}'


COORD_PAIR_PATTERNS = {
    DMSH_COMP: _coord_pair(_DMSH_COMPACTED_LON, _DMSH_COMPACTED_LAT),
    HDMS_COMP: _coord_pair(_HDMS_COMPACTED_LON, _HDMS_COMPACTED_LAT),
    DMSH_SEP: _coord_pair(r'''\d{1,3}\W\d{1,2}\W\d{1,2}\.\d+\W{1,2}[EW]|\d{1,3}\W\d{1,2}\W\d{1,2}\W{1,2}[EW]''',
                          r'''\d{1,2}\W\d{2}\W\d{1,2}\.\d+\W{1,2}[NS]|\d{1,2}\W\d{1,2}\W\d{1,2}\W{1,2}[NS]'''),
    HDMS_SEP: _coord_pair(r'''[EW]\d{1,3}\W\d{1,2}\W\d{1,2}\.\d+\W{1,2}|[EW]\d{1,3}\W\d{1,2}\W\d{1,2}\{1,2}W''',
                          r'''[NS]\d{1,2}\W\d{2}\W\d{1,2}\.\d+\W{1,2}|[NS]\d{1,2}\W\d{1,2}\W\d{1,2}\W{1,2}''')
}


class CoordinateExtraction:

    def __init__(self,
                 sequence: str = SEQUENCE_LON_LAT,
                 angle_format: str = DMSH_COMP,
                 sep: str = COORD_PAIR_SEP_SPACE) -> None:
        self._sequence = sequence
        self._angle_format = angle_format
        self._sep = sep
        self._coordinates_pair_regex = self.get_coordinates_pair_regex()

    def get_coordinate_example(self, sample_coordinate: _sample_coordinate) -> str:
        """ Return formatted example of coordinate.
        :param sample_coordinate: _coord_pair, coordinate to format
        :return str: formatted coordinate
        >>> longitude = _sample_coordinate(deg='013', min='37', sec='38.21', hem='E')

        >>> ce = CoordinateExtraction()
        >>> assert ce.get_coordinate_example(longitude) == '0133738.21E'

        >>> ce = CoordinateExtraction(angle_format=HDMS_COMP)
        >>> assert ce.get_coordinate_example(longitude) == 'E0133738.21'

        >>> ce = CoordinateExtraction(angle_format=DMSH_SEP)
        >>> assert ce.get_coordinate_example(longitude) == '013 37 38.21 E'

        >>> ce = CoordinateExtraction(angle_format=HDMS_SEP)
        >>> assert ce.get_coordinate_example(longitude) == 'E 013 37 38.21'
        """
        if self._angle_format == DMSH_COMP:
            return ''.join(sample_coordinate)
        elif self._angle_format == HDMS_COMP:
            return sample_coordinate.hem + ''.join(sample_coordinate[:-1])
        elif self._angle_format == DMSH_SEP:
            return ' '.join(sample_coordinate)
        elif self._angle_format == HDMS_SEP:
            return sample_coordinate.hem + ' ' + ' '.join(sample_coordinate[:-1])

    def get_coordinates_pair_example(self):
        """ Return formatted example of coordinates pair """
        lon = self.get_coordinate_example(_EXAMPLE_LONGITUDE)
        lat = self.get_coordinate_example(_EXAMPLE_LATITUDE)

        if self._sequence == SEQUENCE_LON_LAT:
            return '{lon}{sep}{lat}'.format(lon=lon, sep=self._sep, lat=lat)
        elif self._sequence == SEQUENCE_LAT_LON:
            return '{lat}{sep}{lon}'.format(lon=lon, sep=self._sep, lat=lat)

    def get_coordinates_pair_regex(self):
        """ Creates regular expression string based coordinates order, coordinates format and separator
        between longitude and latitude.
        >>> ce = CoordinateExtraction()
        >>> assert ce.get_coordinates_pair_regex().match('1203030E 404020S')
        >>> assert not ce.get_coordinates_pair_regex().match('404020S 1203030E')

        >>> ce = CoordinateExtraction(sequence=SEQUENCE_LAT_LON, sep=COORD_PAIR_SEP_HYPHEN)
        >>> assert ce.get_coordinates_pair_regex().match('404020N-1203030W')
        >>> assert not ce.get_coordinates_pair_regex().match('404020N 1203030W')
        >>> assert not ce.get_coordinates_pair_regex().match('404020N1203030W')
        >>> assert not ce.get_coordinates_pair_regex().match('404020S 1203030E')
        >>> assert not ce.get_coordinates_pair_regex().match('404020S 1203030S')
        >>> assert not ce.get_coordinates_pair_regex().match('404020E 1203030W')
        """
        regex_str = ''
        lon_pattern, lat_pattern = COORD_PAIR_PATTERNS.get(self._angle_format)

        if self._sequence == SEQUENCE_LON_LAT:
            regex_str = r'(?P<lon>' + lon_pattern + ')' + \
                        re.escape(self._sep) + \
                        '(?P<lat>' + lat_pattern + ')'
        elif self._sequence == SEQUENCE_LAT_LON:
            regex_str = r'(?P<lat>' + lat_pattern + ')' +\
                        re.escape(self._sep) +\
                        '(?P<lon>' + lon_pattern + ')'
        if regex_str:
            return re.compile(regex_str)

    @staticmethod
    def _remove_new_line_character(source_text: str) -> str:
        """
        >>> text = '''Line1
        ... Line2
        ... Line3'''
        >>> assert CoordinateExtraction._remove_new_line_character(text) == 'Line1Line2Line3'
        """
        return source_text.replace('\n', '')

    def extract_coordinates(self, plain_text):
        """ Get list of coordinate pairs from plain text.
        :param plain_text: str, text from which coordinates are extracted.
        :return: coordinate_pairs: list of tuples with extracted coordinate pairs.
                Note: longitude latitude sequence is the same as in self.coord_sequence attribute.
        >>> plain_text_lon_lat_pair_no_sep =  '''0300108E512824.111N  0300126E512943N
        ... 0300612.7889E512901N   0301202.445E512913.4556N
        ... 0302034E512325.988N   0301735E512220N '''
        >>> ce = CoordinateExtraction(SEQUENCE_LON_LAT, DMSH_COMP, COORD_PAIR_SEP_NONE)
        >>> ce.extract_coordinates(plain_text_lon_lat_pair_no_sep)  # doctest: +NORMALIZE_WHITESPACE
        [('0300108E', '512824.111N'), ('0300126E', '512943N'),  ('0300612.7889E', '512901N'),
        ('0301202.445E', '512913.4556N'), ('0302034E', '512325.988N'), ('0301735E', '512220N')]

         >>> plain_text_lon_lat_pair_sep_hyphen = '''0300108E-512824.111N  0300126E-512943N
         ... 0300612.7889E-512901N   0301202.445E-512913.4556N
         ... 0302034E-512325.988N   0301735E-512220N '''
         >>> ce = CoordinateExtraction(SEQUENCE_LON_LAT, DMSH_COMP, COORD_PAIR_SEP_HYPHEN)
         >>> ce.extract_coordinates(plain_text_lon_lat_pair_sep_hyphen)  # doctest: +NORMALIZE_WHITESPACE
         [('0300108E', '512824.111N'), ('0300126E', '512943N'),  ('0300612.7889E', '512901N'),
         ('0301202.445E', '512913.4556N'), ('0302034E', '512325.988N'), ('0301735E', '512220N')]
         """
        normalized_text = self._remove_new_line_character(plain_text)
        return re.findall(self._coordinates_pair_regex, normalized_text)
