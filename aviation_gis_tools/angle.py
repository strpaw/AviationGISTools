import math
import re

# Angle types
AT_LONGITUDE = 'AT_LONGITUDE '
AT_LATITUDE = 'AT_LATITUDE'

# Angle formats
AF_DMSH_SPACE_SEP = 'AF_DMSH_SPACE_SEP'  # e.g.: 55 22 43.47N
AF_DMSH_HYPHEN_SEP = 'AF_DMSH_HYPHEN_SEP'  # e.g.: 55-2-43.47N
AF_HDMS_SPACE_SEP = 'AF_HDMS_SPACE_SEP'  # e.g.: N55 22 43.47
AF_HDMS_HYPHEN_SEP = 'AF_HDMS_HYPHEN_SEP'  # e.g.: N55-22-43.47

# Angle string representation formats
ANGLE_FORMAT_PATTERNS = {
    AT_LONGITUDE: {
        AF_DMSH_SPACE_SEP: '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}{hem}',
        AF_DMSH_HYPHEN_SEP: '{d:03d}-{m:02d}-{s:0{sec_length}.{sec_prec}f}{hem}',
        AF_HDMS_SPACE_SEP: '{hem}{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_HDMS_HYPHEN_SEP: '{hem}{d:03d}-{m:02d}-{s:0{sec_length}.{sec_prec}f}',
    },
    AT_LATITUDE: {
        AF_DMSH_SPACE_SEP: '{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}{hem}',
        AF_DMSH_HYPHEN_SEP: '{d:02d}-{m:02d}-{s:0{sec_length}.{sec_prec}f}{hem}',
        AF_HDMS_SPACE_SEP: '{hem}{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_HDMS_HYPHEN_SEP: '{hem}{d:02d}-{m:02d}-{s:0{sec_length}.{sec_prec}f}',
    }
}


class Angle:

    def __init__(self): pass

    @staticmethod
    def get_dms_parts(ang_dd, prec=3):
        """ Convert angle from DD format into DMS 'parts': degrees, minutes and seconds
        :param ang_dd: float, angle in DD format
        :param prec: int, positive number of decimal point of seconds, default value is 3
        :return tuple: tuple of d, m, s (int, int, float)
        """
        d_frac_part, d_whole_part = math.modf(math.fabs(ang_dd))  # frac_part - fractional part
        m_frac_part, m_whole_part = math.modf(d_frac_part * 60)
        s_part = m_frac_part * 60

        degrees = int(d_whole_part)
        minutes = int(m_whole_part)
        seconds = round(s_part, prec)

        # Ensure that rounded seconds with specified precision are not >= 60
        if seconds >= 60:
            seconds = 0.0
            minutes += 1
            # Ensure that minutes are not >= 60
            if minutes >= 60:
                minutes += 0
                degrees += 1

        return degrees, minutes, seconds

    @staticmethod
    def get_hemisphere_character(sign, ang_type):
        """ Get hemisphere character e.g. S, N base on "sign" (positive/negative) and angle type.
        :param sign: str, character '-', '+'
        :param ang_type: str, angle type
        :return: str: hemisphere character: N, E, S or W
        """
        if ang_type == AT_LONGITUDE:
            if sign == -1:
                return 'W'
            elif sign == 1:
                return 'E'
        elif ang_type == AT_LATITUDE:
            if sign == -1:
                return 'S'
            elif sign == 1:
                return 'N'

    @staticmethod
    def convert_dd_to_dms(ang_dd, ang_type, dms_format=AF_DMSH_SPACE_SEP, prec=3):
        """ Convert angle from DD format into DMS format
        :param ang_dd: float, angle in DD
        :param ang_type: str, angle type
        :param dms_format: str, desired format of angle in DMS format
        :param prec:  int, positive number of decimal point of seconds
        :return: str, angle in DMS format
        """
        def sign(a_dd): return 1 if a_dd >= 0 else -1
        d, m, s = Angle.get_dms_parts(ang_dd, prec)
        hem = Angle.get_hemisphere_character(sign(ang_dd), ang_type)

        if prec > 0:
            sec_length = prec + 3
        else:
            sec_length = 2

        dms_format_pattern = ANGLE_FORMAT_PATTERNS[ang_type][dms_format]
        return dms_format_pattern.format(d=d, m=m, s=s, sec_length=sec_length, sec_prec=prec, hem=hem)

    @staticmethod
    def normalize_angle(ang_src):
        """ Normalize angle, e. g. replace ',' with '.', ensure cardinal directions (N, S etc.) are capital etc.
        :param ang_src: str, angle source value
        """
        norm_ang = ang_src.strip().upper().replace(',', '.')
        norm_ang = re.sub(r'\s+', ' ', norm_ang)
        return norm_ang

    @staticmethod
    def dmsh_parts_to_dd(dmsh_parts):
        """ Convert coordinates parts into degrees minutes format.
        Note: If angle is within range, example longitude <-180, 180> will be check in separated method.
        :param dmsh_parts: tuple of degrees (int), minutes (int), seconds (float) and hemisphere character (str)
        :return: dd: float
        """
        d, m, s, h = dmsh_parts
        if (0 <= m < 60) and (0 <= s < 60):
            dd = d + m / 60 + s / 3600
            if h in ['W', 'S']:
                return -dd
            elif h in ['N', 'E']:
                return dd
