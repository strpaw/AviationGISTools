from typing import Dict, Tuple
import re

ARINC424_LONGITUDE_LESS_100: str = 'ARINC424_LONGITUDE_LESS_100'
ARINC424_LONGITUDE_EQUAL_GRATER_100: str = 'ARINC424_LONGITUDE_EQUAL_GRATER_100'

ARINC424_COORDINATE_FORMATS = {
    ARINC424_LONGITUDE_LESS_100: '{lat}{lon}{designator}',
    ARINC424_LONGITUDE_EQUAL_GRATER_100: '{lat}{designator}{lon}'
}

ARINC424_REGEXES = {
    ARINC424_LONGITUDE_LESS_100: re.compile(r'''(?P<lat>90|[0-8]\d)
                                                (?P<lon>80|[0-7]\d)
                                                (?P<designator>[NSEW])
                                         ''', re.VERBOSE),
    ARINC424_LONGITUDE_EQUAL_GRATER_100: re.compile(r'''(?P<lat>\d{2})
                                                        (?P<designator>[NSEW])
                                                        (?P<lon>\d{2})
                                                     ''', re.VERBOSE)
}

QUADRANT_DESIGNATOR_MAP: Dict[str, str] = {
    'NW': 'N',
    'NE': 'E',
    'SW': 'W',
    'SE': 'S'
}

DESIGNATOR_QUADRANT_MAP: Dict[str, tuple] = {
    'N': ('W', 'N'),
    'E': ('E', 'N'),
    'W': ('W', 'S'),
    'S': ('E', 'S')
}

REGEX_LONGITUDE_FULL_DEGREES = re.compile(r'''^(180|1[0-7]\d|0\d{2})[EW]$''')
REGEX_LATITUDE_FULL_DEGREES = re.compile(r'''^(90|[0-8]\d)[NS]$''')


class Arinc424ShorthandsCoordinate:

    @staticmethod
    def is_longitude_full_degrees(lon: str) -> bool:
        """
        >>> a424 = Arinc424ShorthandsCoordinate()
        >>> assert a424.is_longitude_full_degrees('000E')
        >>> assert a424.is_longitude_full_degrees('001E')
        >>> assert a424.is_longitude_full_degrees('090W')
        >>> assert a424.is_longitude_full_degrees('100W')
        >>> assert a424.is_longitude_full_degrees('180W')
        >>> assert not a424.is_longitude_full_degrees('181W')
        >>> assert not a424.is_longitude_full_degrees('110.1W')
        >>> assert not a424.is_longitude_full_degrees('E100')
        >>> assert not a424.is_longitude_full_degrees('110.1W')
        >>> assert not a424.is_longitude_full_degrees('E100')
        >>> assert isinstance(a424.is_longitude_full_degrees('E100'), bool)
        >>> assert isinstance(a424.is_longitude_full_degrees('100E'), bool)
        """
        return bool(REGEX_LONGITUDE_FULL_DEGREES.match(lon))

    @staticmethod
    def is_latitude_full_degrees(lat: str) -> bool:
        """
        >>> a424 = Arinc424ShorthandsCoordinate()
        >>> assert a424.is_latitude_full_degrees('00N')
        >>> assert a424.is_latitude_full_degrees('01N')
        >>> assert a424.is_latitude_full_degrees('90S')
        >>> assert not a424.is_latitude_full_degrees('91S')
        >>> assert not a424.is_latitude_full_degrees('10.1N')
        >>> assert not a424.is_latitude_full_degrees('N10')
        >>> assert not a424.is_latitude_full_degrees('E10')
        >>> assert isinstance(a424.is_latitude_full_degrees('E10'), bool)
        >>> assert isinstance(a424.is_latitude_full_degrees('10N'), bool)
        """
        return bool(REGEX_LATITUDE_FULL_DEGREES.match(lat))

    @staticmethod
    def _get_arinc424_format(lon: str) -> str:
        """ Get ARINC424 format pattern based on longitude value
        :param lon: str, longitude in full degrees DH format
        :return:
        >>> a424 = Arinc424ShorthandsCoordinate()
        >>> assert a424._get_arinc424_format('100E') == '{lat}{designator}{lon}'
        >>> assert a424._get_arinc424_format('090E') == '{lat}{lon}{designator}'
        >>> assert isinstance(a424._get_arinc424_format('100E'), str)
        >>> assert isinstance(a424._get_arinc424_format('090E'), str)
        """
        if int(lon[:3]) < 100:
            return ARINC424_COORDINATE_FORMATS[ARINC424_LONGITUDE_LESS_100]
        else:
            return ARINC424_COORDINATE_FORMATS[ARINC424_LONGITUDE_EQUAL_GRATER_100]

    @staticmethod
    def _get_quadrant(lon: str, lat: str) -> str:
        return lat[-1] + lon[-1]

    @staticmethod
    def encode_to_arinc424(lon: str, lat: str) -> str:
        """
        >>> assert Arinc424ShorthandsCoordinate.encode_to_arinc424(lon='160W', lat='50N') == '50N60'
        >>> assert Arinc424ShorthandsCoordinate.encode_to_arinc424(lon='060W', lat='50N') == '5060N'
        >>> assert Arinc424ShorthandsCoordinate.encode_to_arinc424(lon='160E', lat='50N') == '50E60'
        >>> assert Arinc424ShorthandsCoordinate.encode_to_arinc424(lon='060E', lat='50N') == '5060E'
        >>> assert Arinc424ShorthandsCoordinate.encode_to_arinc424(lon='160W', lat='50S') == '50W60'
        >>> assert Arinc424ShorthandsCoordinate.encode_to_arinc424(lon='060W', lat='50S') == '5060W'
        >>> assert Arinc424ShorthandsCoordinate.encode_to_arinc424(lon='060E', lat='50S') == '5060S'
        """
        if Arinc424ShorthandsCoordinate.is_longitude_full_degrees(lon) and \
           Arinc424ShorthandsCoordinate.is_latitude_full_degrees(lat):
            quadrant = Arinc424ShorthandsCoordinate._get_quadrant(lon, lat)
            a424_format = Arinc424ShorthandsCoordinate._get_arinc424_format(lon)
            designator = QUADRANT_DESIGNATOR_MAP[quadrant]
            return a424_format.format(lon=lon[1:3], lat=lat[:2], designator=designator)

    @staticmethod
    def decode_arinc424(arinc424: str) -> Tuple[str, str]:
        """
        >>> assert Arinc424ShorthandsCoordinate.decode_arinc424('50N60') == ('160W', '50N')
        >>> assert Arinc424ShorthandsCoordinate.decode_arinc424('5060N') == ('060W', '50N')
        >>> assert Arinc424ShorthandsCoordinate.decode_arinc424('50E60') == ('160E', '50N')
        >>> assert Arinc424ShorthandsCoordinate.decode_arinc424('5060E') == ('060E', '50N')
        >>> assert Arinc424ShorthandsCoordinate.decode_arinc424('50W60') == ('160W', '50S')
        >>> assert Arinc424ShorthandsCoordinate.decode_arinc424('5060W') == ('060W', '50S')
        >>> assert Arinc424ShorthandsCoordinate.decode_arinc424('5060S') == ('060E', '50S')
        >>> assert Arinc424ShorthandsCoordinate.decode_arinc424('50S60') == ('160E', '50S')
        """
        for rgx_name, rgx in ARINC424_REGEXES.items():
            if rgx.match(arinc424):
                groups = rgx.search(arinc424)
                designator = groups.group('designator')
                lat = groups.group('lat')
                lon = groups.group('lon')

                lon_desi, lat_desi = DESIGNATOR_QUADRANT_MAP[designator]
                if rgx_name == ARINC424_LONGITUDE_LESS_100:
                    return f"0{lon}{lon_desi}", f"{lat}{lat_desi}"
                elif rgx_name == ARINC424_LONGITUDE_EQUAL_GRATER_100:
                    return f"1{lon}{lon_desi}", f"{lat}{lat_desi}"
