"""
coordinate_extraction.py module provides functionality to extracts coordinates from plain text.
"""
# -*- coding: utf-8 -*-
import re
from collections import namedtuple

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
_sample_coordinate = namedtuple('sample_coordinate', 'deg min sec hem')

example_latitude = _sample_coordinate(deg='74', min='56', sec='32.55', hem='N')
example_longitude = _sample_coordinate(deg='013', min='37', sec='38.21', hem='E')


class CoordinatePairExtraction:

    COORD_PAIR_PATTERNS = {
        DMSH_COMP: _coord_pair(r'\d{7}\.\d+[EW]|\d{7}[EW]', r'\d{6}\.\d+[NS]|\d{6}[NS]'),
        HDMS_COMP: _coord_pair(r'[EW]\d{7}\.\d+|[EW]\d{7}', r'[NS]\d{6}\.\d+|[NS]\d{6}'),
        DMSH_SEP: _coord_pair(r'''\d{1,3}\W\d{1,2}\W\d{1,2}\.\d+\W{1,2}[EW]|\d{1,3}\W\d{1,2}\W\d{1,2}\W{1,2}[EW]''',
                              r'''\d{1,2}\W\d{2}\W\d{1,2}\.\d+\W{1,2}[NS]|\d{1,2}\W\d{1,2}\W\d{1,2}\W{1,2}[NS]'''),
        HDMS_SEP: _coord_pair(r'''[EW]\d{1,3}\W\d{1,2}\W\d{1,2}\.\d+\W{1,2}|[EW]\d{1,3}\W\d{1,2}\W\d{1,2}\{1,2}W''',
                              r'''[NS]\d{1,2}\W\d{2}\W\d{1,2}\.\d+\W{1,2}|[NS]\d{1,2}\W\d{1,2}\W\d{1,2}\W{1,2}''')
    }

    def __init__(self, coord_sequence, coord_format, coord_sep):
        """
        :param coord_sequence: str, constant that defines longitude and latitude sequence in coordinate pair,
                            e.g. SEQUENCE_LON_LAT.
        :param coord_format: str, constant that defines format of coordinate, e.g. DMSH_COMP.
        :param coord_sep: str, defines separator between longitude and latitude, e.g. COORD_PAIR_SEP_SPACE.
        """
        self.coord_sequence = coord_sequence
        self.coord_format = coord_format
        self.coord_sep = coord_sep
        self.coordinates_pair_regex = None
        self.set_coordinates_pair_regex()

    def get_coordinate_example(self, sample_coordinate):
        """ Return formatted example of coordinate.
        :param sample_coordinate: _coord_pair, coordinate to format
        :return str: formatted coordinate
        """
        example = ''
        if self.coord_format == DMSH_COMP:
            example = ''.join(sample_coordinate)
        elif self.coord_format == HDMS_COMP:
            example = ''.join(sample_coordinate)
            example = example[-1] + example[:-1]
        elif self.coord_format == DMSH_SEP:
            example = ' '.join(sample_coordinate)
        elif self.coord_format == HDMS_SEP:
            example = ' '.join(sample_coordinate)
            example = example[-1] + ' ' + example[:-1].strip()
        return example

    def get_coordinates_pair_example(self):
        """ Return formatted example of coordinates pair """
        example = ''
        lon = self.get_coordinate_example(example_longitude)
        lat = self.get_coordinate_example(example_latitude)

        if self.coord_sequence == SEQUENCE_LON_LAT:
            example = '{lon}{sep}{lat}'.format(lon=lon, sep=self.coord_sep, lat=lat)
        elif self.coord_sequence == SEQUENCE_LAT_LON:
            example = '{lat}{sep}{lon}'.format(lon=lon, sep=self.coord_sep, lat=lat)
        return example

    def set_coordinates_pair_regex(self):
        """ Creates regular expression string based coordinates order, coordinates format and separator
        between longitude and latitude. """
        regex_str = ''
        lon_pattern, lat_pattern = CoordinatePairExtraction.COORD_PAIR_PATTERNS.get(self.coord_format)

        if self.coord_sequence == SEQUENCE_LON_LAT:
            regex_str = r'(?P<lon>' + lon_pattern + ')' + \
                        re.escape(self.coord_sep) + \
                        '(?P<lat>' + lat_pattern + ')'
        elif self.coord_sequence == SEQUENCE_LAT_LON:
            regex_str = r'(?P<lat>' + lat_pattern + ')' +\
                        re.escape(self.coord_sep) +\
                        '(?P<lon>' + lon_pattern + ')'
        if regex_str:
            self.coordinates_pair_regex = re.compile(regex_str)

    @staticmethod
    def remove_new_line_character(plain_text):
        """ Create 'continuous' string without new lines characters. It is for case when one coordinate
        (longitude, latitude) might be in two lines.
        :param plain_text: str, text from which coordinates are extracted.
        :return: shape_str: str, string without new line character
        """
        normalized = ''
        for line in plain_text:
            normalized += line.strip('\n')
        return normalized

    def extract_coordinates(self, plain_text):
        """ Get list of coordinate pairs from plain text.
        :param plain_text: str, text from which coordinates are extracted.
        :return: coordinate_pairs: list of tuples with extracted coordinate pairs.
                Note: longitude latitude sequence is the same as in self.coord_sequence attribute.
         """
        normalized_text = self.remove_new_line_character(plain_text)
        coordinate_pairs = re.findall(self.coordinates_pair_regex, normalized_text)
        return coordinate_pairs
