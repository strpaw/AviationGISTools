from math import fabs
from typing import Tuple, Union
import re

# Angle types
AT_LONGITUDE = 'AT_LONGITUDE'
AT_LATITUDE = 'AT_LATITUDE'
AT_BEARING = 'AT_BEARING'

# Angle formats
AF_DMSH_SPACE_SEP = 'AF_DMSH_SPACE_SEP'  # e.g.: 55 22 43.47N
AF_DMSH_HYPHEN_SEP = 'AF_DMSH_HYPHEN_SEP'  # e.g.: 55-2-43.47N
AF_HDMS_SPACE_SEP = 'AF_HDMS_SPACE_SEP'  # e.g.: N55 22 43.47
AF_HDMS_HYPHEN_SEP = 'AF_HDMS_HYPHEN_SEP'  # e.g.: N55-22-43.47

# Angle string representation formats
ANGLE_FORMAT_PATTERNS = {
    AT_LONGITUDE: {
        AF_DMSH_SPACE_SEP: '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}{h}',
        AF_DMSH_HYPHEN_SEP: '{d:03d}-{m:02d}-{s:0{sec_length}.{sec_prec}f}{h}',
        AF_HDMS_SPACE_SEP: '{h}{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_HDMS_HYPHEN_SEP: '{h}{d:03d}-{m:02d}-{s:0{sec_length}.{sec_prec}f}',
    },
    AT_LATITUDE: {
        AF_DMSH_SPACE_SEP: '{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}{h}',
        AF_DMSH_HYPHEN_SEP: '{d:02d}-{m:02d}-{s:0{sec_length}.{sec_prec}f}{h}',
        AF_HDMS_SPACE_SEP: '{h}{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_HDMS_HYPHEN_SEP: '{h}{d:02d}-{m:02d}-{s:0{sec_length}.{sec_prec}f}',
    }
}


class Angle:

    def __init__(self):
        pass

    @staticmethod
    def normalize_angle(ang_src: str) -> str:
        """ Normalize angle, e. g. replace ',' with '.', ensure cardinal directions (N, S etc.) are capital etc.
        :param ang_src: str, angle source valueb
        >>> assert Angle.normalize_angle(' 32   44 56,77n') == '32 44 56.77N'
        """
        norm_ang = ang_src.strip().upper().replace(',', '.')
        norm_ang = re.sub(r'\s+', ' ', norm_ang)
        return norm_ang

    @staticmethod
    def is_angle_within_range(ang_dd: float, ang_type: str) -> Union[float, None]:
        """  Check if coordinate is within range for specified angle type
        :param ang_dd: float, coordinate to check
        :param ang_type: const(str): type of angle
        :return:
        """
        if ang_type == AT_LONGITUDE:
            return -180 <= ang_dd <= 180
        elif ang_type == AT_LATITUDE:
            return -90 <= ang_dd <= 90
        elif ang_type == AT_BEARING:
            return 0 <= ang_dd <= 360
        else:
            raise ValueError(f'Angle type {ang_type} not supported.')

    @staticmethod
    def dd_to_dms_parts(ang_dd: float, prec: int = 3) -> Tuple[int, int, float]:
        """ Extract degrees, minutes, seconds from angle in DD (decimal degrees) format.
        >>> assert Angle.dd_to_dms_parts(0) == (0, 0, 0.000)
        >>> assert Angle.dd_to_dms_parts(-1) == (-1, 0, 0.000)
        >>> assert Angle.dd_to_dms_parts(10) == (10, 0, 0.000)
        >>> assert Angle.dd_to_dms_parts(-45.5) == (-45, 30, 0.000)
        >>> assert Angle.dd_to_dms_parts(1.0169444444444400) == (1, 1, 1.0)
        >>> assert Angle.dd_to_dms_parts(100.1694444444444000) == (100, 10, 10.000)
        """
        minutes, seconds = divmod(fabs(ang_dd) * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        seconds = round(seconds, prec)

        # Ensure that rounded seconds with specified precision are not >= 60
        if seconds >= 60:
            seconds = 0.0
            minutes += 1
        if minutes >= 60:
            minutes = 0
            degrees += 1

        if ang_dd < 0:
            degrees = -degrees

        return int(degrees), int(minutes), seconds

    @staticmethod
    def get_hemisphere_designator(ang_dd: float, ang_type: str) -> str:
        """ Get hemisphere designator e.g. S, N base on "sign" (positive/negative) of angle in DD format and angle type.
        :param ang_dd: angle in DD format
        :param ang_type: angle type
        :return: str: hemisphere designator: N, E, S or W
        >>> assert Angle.get_hemisphere_designator(-123.44, AT_LONGITUDE) == 'W'
        >>> assert Angle.get_hemisphere_designator(33, AT_LONGITUDE) == 'E'
        >>> assert Angle.get_hemisphere_designator(23.44, AT_LATITUDE) == 'N'
        >>> assert Angle.get_hemisphere_designator(-23.44, AT_LATITUDE) == 'S'
        """
        if ang_type == AT_LONGITUDE:
            return 'E' if ang_dd >= 0 else 'W'
        elif ang_type == AT_LATITUDE:
            return 'N' if ang_dd >= 0 else 'S'

    @staticmethod
    def convert_dd_to_dms(ang_dd: float,
                          ang_type: str,
                          dms_format: str = AF_DMSH_SPACE_SEP,
                          prec: int = 3) -> str:
        """ Convert angle from DD format into DMS format
        :param ang_dd: angle in DD format
        :param ang_type: angle type
        :param dms_format:desired format of angle in DMS format
        :param prec:  int, positive number of decimal point of seconds
        :return: angle in DMS format
        >>> assert Angle.convert_dd_to_dms(145.9589599661111000,
        ...                                AT_LONGITUDE, dms_format=AF_HDMS_SPACE_SEP) == 'E145 57 32.256'
        >>> assert Angle.convert_dd_to_dms(-145.9589599661111000,
        ...                                AT_LONGITUDE, dms_format=AF_HDMS_HYPHEN_SEP) == 'W145-57-32.256'
        >>> assert Angle.convert_dd_to_dms(145.9589599661111000,
        ...                                 AT_LONGITUDE, dms_format=AF_DMSH_SPACE_SEP, prec=2) == '145 57 32.26E'
        >>> assert Angle.convert_dd_to_dms(145.9589599661111000,
        ...                                AT_LONGITUDE, dms_format=AF_DMSH_HYPHEN_SEP, prec=1) == '145-57-32.3E'
        >>> assert Angle.convert_dd_to_dms(45.9589599661111000,
        ...                                AT_LATITUDE, dms_format=AF_HDMS_SPACE_SEP) == 'N45 57 32.256'
        >>> assert Angle.convert_dd_to_dms(-45.9589599661111000,
        ...                                AT_LATITUDE, dms_format=AF_HDMS_HYPHEN_SEP) == 'S45-57-32.256'
        >>> assert Angle.convert_dd_to_dms(45.9589599661111000,
        ...                                AT_LATITUDE, dms_format=AF_DMSH_SPACE_SEP, prec=2) == '45 57 32.26N'
        >>> assert Angle.convert_dd_to_dms(-45.9589599661111000,
        ...                                AT_LATITUDE, dms_format=AF_DMSH_HYPHEN_SEP, prec=1) == '45-57-32.3S'
        """
        d, m, s = Angle.dd_to_dms_parts(ang_dd, prec)
        h = Angle.get_hemisphere_designator(ang_dd, ang_type)

        if prec > 0:
            sec_length = prec + 3
        else:
            sec_length = 2

        dms_format_pattern = ANGLE_FORMAT_PATTERNS[ang_type][dms_format]
        return dms_format_pattern.format(d=int(fabs(d)), m=m, s=s, sec_length=sec_length, sec_prec=prec, h=h)

    @staticmethod
    def dmsh_parts_to_dd(dmsh_parts: Tuple[int, int, float, str]) -> Union[float, None]:
        """ Convert coordinates parts into degrees minutes format.
        Note: If angle is within range, example longitude <-180, 180> will be check in separated method
        :param dmsh_parts: tuple of degrees (int), minutes (int), seconds (float) and hemisphere character (str)
        :return: dd: float
        >>> assert Angle.dmsh_parts_to_dd((100, 35, 44, 'N')) == 100.59555555555555
        >>> assert Angle.dmsh_parts_to_dd((100, 35, 44, 'W')) == -100.59555555555555
        >>> Angle.dmsh_parts_to_dd((100, 61, 59, 'W'))
        Traceback (most recent call last):
        ValueError: Minutes 61 or/and seconds 59 outside range <0, 60)
        >>> Angle.dmsh_parts_to_dd((100, 0, 60, 'E'))
        Traceback (most recent call last):
        ValueError: Minutes 0 or/and seconds 60 outside range <0, 60)
        >>> Angle.dmsh_parts_to_dd((100, -1, 0, 'S'))
        Traceback (most recent call last):
        ValueError: Minutes -1 or/and seconds 0 outside range <0, 60)
        >>> Angle.dmsh_parts_to_dd((100, 5, 10, 'A'))
        Traceback (most recent call last):
        ValueError: Hemisphere designator A not allowed
        """
        d, m, s, h = dmsh_parts

        if (0 <= m < 60) and (0 <= s < 60):
            dd = d + m / 60 + s / 3600
            if h in ['W', 'S']:
                return -dd
            elif h in ['N', 'E']:
                return dd
            else:
                raise ValueError(f'Hemisphere designator {h} not allowed')
        else:
            raise ValueError(f'Minutes {m} or/and seconds {s} outside range <0, 60)')

    @staticmethod
    def dmh_parts_to_dd(dmh_parts: Tuple[int, float, str]) -> Union[float, None]:
        """ Convert coordinates parts into degrees minutes format.
        Note: If angle is within range, example longitude <-180, 180> will be check in separated method
        :param dmh_parts: tuple of degrees (int), minutes (int), seconds (float) and hemisphere character (str)
        :return: dd: float
        >>> assert Angle.dmh_parts_to_dd((10, 35.123, 'N')) == 10.5853833333333333
        >>> assert Angle.dmh_parts_to_dd((100, 35.123, 'W')) == -100.5853833333333333
        >>> Angle.dmh_parts_to_dd((100, 61, 'W'))
        Traceback (most recent call last):
        ValueError: Minutes: 61 outside range <0, 60)
        >>> Angle.dmh_parts_to_dd((100, 60, 'E'))
        Traceback (most recent call last):
        ValueError: Minutes: 60 outside range <0, 60)
        >>> Angle.dmh_parts_to_dd((100, -1, 'S'))
        Traceback (most recent call last):
        ValueError: Minutes: -1 outside range <0, 60)
        >>> Angle.dmh_parts_to_dd((100, 5, 'A'))
        Traceback (most recent call last):
        ValueError: Hemisphere designator A not allowed
        """
        d, m, h = dmh_parts

        if 0 <= m < 60:
            dd = d + m / 60
            if h in ['W', 'S']:
                return -dd
            elif h in ['N', 'E']:
                return dd
            else:
                raise ValueError(f'Hemisphere designator {h} not allowed')
        else:
            raise ValueError(f'Minutes: {m} outside range <0, 60)')
