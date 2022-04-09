from aviation_gis_tools.angle import (
    AT_LONGITUDE,
    AT_LATITUDE,
    Angle
)
from typing import Union
import re

COORDINATE_COMPACTED = {
    AT_LONGITUDE: {
        'DMSH_COMPACTED': re.compile(r'''(?P<deg>^180|^1[0-7]\d|^0\d{2})
                                         (?P<min>[0-5]\d)
                                         (?P<sec>[0-5]\d\.\d+|[0-5]\d)
                                         (?P<hem>[EW]$)
                                      ''', re.VERBOSE),
        'HDMS_COMPACTED': re.compile(r'''(?P<hem>^[EW])
                                         (?P<deg>180|1[0-7]\d|0\d{2})
                                         (?P<min>[0-5]\d)
                                         (?P<sec>[0-5]\d\.\d+$|[0-5]\d$)          
                                      ''', re.VERBOSE),
        'DMH_COMPACTED': re.compile(r'''(?P<deg>^180|^1[0-7]\d|^0\d{2})
                                        (?P<min>[0-5]\d\.\d+|[0-5]\d)
                                        (?P<hem>[EW]$)
                                    ''', re.VERBOSE),
        'HDM_COMPACTED': re.compile(r'''(?P<hem>^[EW])
                                        (?P<deg>180|1[0-7]\d|0\d{2})
                                        (?P<min>[0-5]\d\.\d+$|[0-5]\d$)
                                    ''', re.VERBOSE)
    },
    AT_LATITUDE: {
        'DMSH_COMPACTED': re.compile(r'''(?P<deg>^90|^[0-8]\d)
                                         (?P<min>[0-5]\d)
                                         (?P<sec>[0-5]\d\.\d+|[0-5]\d)
                                         (?P<hem>[NS]$)
                                    ''', re.VERBOSE),
        'HDMS_COMPACTED': re.compile(r'''(?P<hem>^[NS])
                                         (?P<deg>90|[0-8]\d)
                                         (?P<min>[0-5]\d)
                                         (?P<sec>[0-5]\d\.\d+$|[0-5]\d$)
                                     ''', re.VERBOSE),
        'DMH_COMPACTED': re.compile(r'''(?P<deg>^90|^[0-8]\d)
                                        (?P<min>[0-5]\d\.\d+|[0-5]\d)
                                        (?P<hem>[NS]$)
                                    ''', re.VERBOSE),
        'HDM_COMPACTED': re.compile(r'''(?P<hem>^[NS])
                                         (?P<deg>90|[0-8]\d)
                                         (?P<min>[0-5]\d\.\d+$|[0-5]\d$)
                                    ''', re.VERBOSE)
    }
}


class Coordinate(Angle):

    def __init__(self,
                 coord_src: Union[str, float, int],
                 coord_type: Union[str, float, int],
                 coord_label: str = None) -> None:
        Angle.__init__(self)
        self._coord_src = coord_src
        self._coord_type = coord_type
        self._coord_label = coord_label
        self._coord_dd = Coordinate.convert_compacted_to_dd(self._coord_src, self._coord_type)

    def __str__(self):
        return self._coord_src

    @property
    def coord_dd(self):
        return self._coord_dd

    @property
    def coord_src(self):
        return self._coord_src

    @staticmethod
    def convert_compacted_to_dd(coord_src: str, ang_type: str) -> Union[float, None]:
        """ Converts DMSH or HDMS format into DD format
        :param coord_src: str
        :param ang_type: str
        :return: float: angle in decimal degrees format, if conversion failed (not supported format,
                 error in angle example minutes >= 60, incorrect type - returns None)
        >>> assert Coordinate.convert_compacted_to_dd('1800000E', AT_LONGITUDE) == 180.0
        >>> assert Coordinate.convert_compacted_to_dd('1800000.0W', AT_LONGITUDE) == -180.0
        >>> assert Coordinate.convert_compacted_to_dd('E1800000', AT_LONGITUDE) == 180.0
        >>> assert Coordinate.convert_compacted_to_dd('W1800000.0', AT_LONGITUDE) == -180.0
        >>> assert Coordinate.convert_compacted_to_dd('W0003000.000', AT_LONGITUDE) == -0.5
        >>> assert Coordinate.convert_compacted_to_dd('E1234601.445', AT_LONGITUDE) == 123.76706805555555
        >>> assert Coordinate.convert_compacted_to_dd('E1810000', AT_LONGITUDE) is None
        >>> assert Coordinate.convert_compacted_to_dd('S200000.00', AT_LONGITUDE) is None
        >>> assert Coordinate.convert_compacted_to_dd('900000N', AT_LATITUDE) == 90.0
        >>> assert Coordinate.convert_compacted_to_dd('900000.0S', AT_LATITUDE) == -90.0
        >>> assert Coordinate.convert_compacted_to_dd('234601.445N', AT_LATITUDE) == 23.767068055555555
        >>> assert Coordinate.convert_compacted_to_dd('N900000', AT_LATITUDE) == 90.0
        >>> assert Coordinate.convert_compacted_to_dd('S900000.0', AT_LATITUDE) == -90.0
        >>> assert Coordinate.convert_compacted_to_dd('N003000.000', AT_LATITUDE) == 0.5
        >>> assert Coordinate.convert_compacted_to_dd('S900000.001', AT_LATITUDE) is None
        >>> assert Coordinate.convert_compacted_to_dd('E0900000.0', AT_LATITUDE) is None
        >>> assert Coordinate.convert_compacted_to_dd('18000.00E', AT_LONGITUDE) == 180.0
        >>> assert Coordinate.convert_compacted_to_dd('18000.0000W', AT_LONGITUDE) == -180.0
        >>> assert Coordinate.convert_compacted_to_dd('E04750.222', AT_LONGITUDE) == 47.83703333333333
        >>> assert Coordinate.convert_compacted_to_dd('W18010.000', AT_LONGITUDE) is None
        >>> assert Coordinate.convert_compacted_to_dd('S9010.000', AT_LONGITUDE) is None
        >>> assert Coordinate.convert_compacted_to_dd('9000.00S', AT_LATITUDE) == -90.0
        >>> assert Coordinate.convert_compacted_to_dd('9000.0000N', AT_LATITUDE) == 90.0
        >>> assert Coordinate.convert_compacted_to_dd('S4750.222', AT_LATITUDE) == -47.83703333333333
        >>> assert Coordinate.convert_compacted_to_dd('N9010.000', AT_LATITUDE) is None
        >>> assert Coordinate.convert_compacted_to_dd('E09010.000', AT_LATITUDE) is None
        """
        dd = None

        for coord_type, coord_pattern in COORDINATE_COMPACTED[ang_type].items():
            if coord_pattern.match(coord_src):
                if coord_type in ['DMSH_COMPACTED', 'HDMS_COMPACTED']:
                    dmsh_parts = coord_pattern.search(coord_src)
                    d = int(dmsh_parts.group('deg'))
                    m = int(dmsh_parts.group('min'))
                    s = float(dmsh_parts.group('sec'))
                    h = dmsh_parts.group('hem')
                    dd = Coordinate.dmsh_parts_to_dd((d, m, s, h))
                elif coord_type in ['DMH_COMPACTED', 'HDM_COMPACTED']:
                    dmh_parts = coord_pattern.search(coord_src)
                    d = int(dmh_parts.group('deg'))
                    m = float(dmh_parts.group('min'))
                    h = dmh_parts.group('hem')
                    dd = Coordinate.dmh_parts_to_dd((d, m, h))

        if dd:
            if Coordinate.is_angle_within_range(dd, ang_type):
                return dd

    @staticmethod
    def convert_to_dd(coord_src: Union[str, float, int],
                      coord_type: str,
                      coord_label: str = None) -> Union[float, None]:
        """ Convert coordinate into DD format.
        If source value can't be converted (not supported format, incorrect values) exception will be thrown
        :param coord_src: str, coordinate to be converted
        :param coord_type: str, AT_LONGITUDE or AT_LATITUDE
        :param coord_label: str, label a coordinate,  example: 'Reference latitude', 'Circle center latitude'
        :return: float: coordinate in DD
        """
        if type(coord_src) in [float, int]:
            Coordinate.is_angle_within_range(coord_src, coord_type)

        if not Coordinate.normalize_angle(coord_src):
            if coord_label:
                raise ValueError(f'{coord_label} is empty')
            else:
                raise ValueError(f'{coord_type} is empty')

        return Coordinate.convert_compacted_to_dd(coord_src, coord_type)
