"""
Support for conversion among full degrees coordinates and ARINC424 "shorthand system".
"""

import re


class Arinc424CoordinatesConversion:

    ARINC424_LETTERS = {
        'NW': 'N',
        'NE': 'E',
        'SW': 'W',
        'SE': 'S'
    }

    HEMISPHERES = {
        'N': ('W', 'N'),
        'E': ('E', 'N'),
        'W': ('W', 'S'),
        'S': ('E', 'S')
    }

    # Templates for ARINC424 shorthand coordinates
    PATTERN_LONGITUDE_LESS_HUNDRED = '{lat}{lon}{letter}'
    PATTERN_LONGITUDE_EQUAL_GRATER_HUNDRED = '{lat}{letter}{lon}'

    # Regular expression  for longitude and latitude in full degrees with hemisphere suffix format
    REGEX_LONGITUDE_DH_FULL_DEGREES = re.compile(r'''^(180|1[0-7]\d|0\d{2})[EW]$''')
    REGEX_LATITUDE_DH_FULL_DEGREES = re.compile(r'''^(90|[0-8]\d)[NS]$''')

    # Regular expression for shorthand coordinates pair in ARINC424 system - full degrees
    REGEXES_ARINC424 = {
        'LONGITUDE_LESS_HUNDRED': re.compile(r'''(?P<lat>\d{2})  # First two of latitude
                                                 (?P<lon>\d{2})  # Second and third of longitude
                                                 (?P<letter>[NSEW])  # Letter designator 
                                             ''', re.VERBOSE),
        'LONGITUDE_EQUAL_GRATER_HUNDRED': re.compile(r'''(?P<lat>\d{2})  # First two of latitude
                                                         (?P<letter>[NSEW])  # Letter designator 
                                                         (?P<lon>\d{2})  # Second and third of longitude
                                                      ''', re.VERBOSE)
    }

    @staticmethod
    def is_longitude_full_dh(lon):
        """ Check if longitude is in full DH format.
        :param lon: str, longitude in DMH format, e.g. 135E
        :return: bool:
        """
        return bool(Arinc424CoordinatesConversion.REGEX_LONGITUDE_DH_FULL_DEGREES.match(lon))

    @staticmethod
    def is_latitude_full_dh(lat):
        """ Check if latitude is in full DH format.
        :param lat: str, longitude in DMH format, e.g. 35N
        :return: bool:
        """
        return bool(Arinc424CoordinatesConversion.REGEX_LATITUDE_DH_FULL_DEGREES.match(lat))

    @staticmethod
    def get_hemispheres_from_coord_pair(lon, lat):
        """ Get hemisphere characters from longitude and latitude
        :param lon: str, longitude in DMH format
        :param lat: str, latitude in DMH format
        :return: str: hemisphere characters from lon and lat
        """
        lon_hem = lon[-1]
        lat_hem = lat[-1]
        return lat_hem + lon_hem

    @staticmethod
    def get_arinc424_format_pattern(lon):
        """ Get ARINC424 format pattern based on longitude value.
        :param lon: str, longitude in full degrees DH format
        :return:
        """
        lon_int = int(lon[:3])
        if lon_int < 100:
            return Arinc424CoordinatesConversion.PATTERN_LONGITUDE_LESS_HUNDRED
        else:
            return Arinc424CoordinatesConversion.PATTERN_LONGITUDE_EQUAL_GRATER_HUNDRED

    @staticmethod
    def coord_to_arinc424(lon, lat):
        """ Convert full degrees coordinates to ARINC424 format.
        :param lon: str, longitude in DMH format
        :param lat: str, latitude in DMH format
        :return: str: full degrees coordinates in ARINC424 format
        """
        if Arinc424CoordinatesConversion.is_longitude_full_dh(lon) and \
           Arinc424CoordinatesConversion.is_latitude_full_dh(lat):
            hems = Arinc424CoordinatesConversion.get_hemispheres_from_coord_pair(lon, lat)
            arinc424_letter = Arinc424CoordinatesConversion.ARINC424_LETTERS[hems]
            arinc424_format = Arinc424CoordinatesConversion.get_arinc424_format_pattern(lon)
            lon = lon[1:3]
            lat = lat[:2]
            return arinc424_format.format(lat=lat, lon=lon, letter=arinc424_letter)

    @staticmethod
    def is_lon_lat_arinc424_code_within_range(lon, lat):
        """ Check if longitude and latitude parts of ARINC424 code are within range.
        :param lon: str, longitude part from ARINC424 code
        :param lat: str, latitude part from ARINC424 code
        :return: bool:
        """
        msg = ''
        is_within_range = True

        if int(lon) > 80:
            is_within_range = False
            msg = 'Longitude part can\'t be grater the 80. '

        if int(lat) > 90:
            is_within_range = False
            msg += 'Latitude part can\'t be grater the 90.'

        if not is_within_range:
            print(msg)

        return is_within_range

    @staticmethod
    def arinc424_to_coordinates(arinc424):
        """ Convert from ARINC424 shorthand format to DM format
        :param arinc424: str, coordinates in ARINC424 shorthand code
        :return: str, coordinates in DMH format, e.g.: 16000W 5000N
        """
        for regex in Arinc424CoordinatesConversion.REGEXES_ARINC424:
            if Arinc424CoordinatesConversion.REGEXES_ARINC424.get(regex).match(arinc424):
                groups = Arinc424CoordinatesConversion.REGEXES_ARINC424.get(regex).search(arinc424)
                letter = groups.group('letter')
                lat = groups.group('lat')
                lon = groups.group('lon')

                if Arinc424CoordinatesConversion.is_lon_lat_arinc424_code_within_range(lon, lat):
                    lon_hem, lat_hem = Arinc424CoordinatesConversion.HEMISPHERES[letter]
                    if regex == 'LONGITUDE_LESS_HUNDRED':
                        return '0{}00{} {}00{}'.format(lon, lon_hem, lat, lat_hem)
                    elif regex == 'LONGITUDE_EQUAL_GRATER_HUNDRED':
                        return '1{}00{} {}00{}'.format(lon, lon_hem, lat, lat_hem)
