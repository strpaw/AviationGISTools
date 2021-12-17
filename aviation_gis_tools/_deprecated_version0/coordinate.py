from aviation_gis_tools._deprecated_version0.angle import *

COORDINATE_COMPACTED = {
    AT_LONGITUDE: {
        'DMSH_COMPACTED': re.compile(r'''(?P<deg>^180|^1[0-7]\d|^0\d{2})  # Degrees
                                         (?P<min>[0-5]\d)  # Minutes
                                         (?P<sec>[0-5]\d\.\d+|[0-5]\d)  # Seconds
                                         (?P<hem>[EW]$)  # Hemisphere
                                      ''', re.VERBOSE),
        'HDMS_COMPACTED': re.compile(r'''(?P<hem>^[EW])  # Hemisphere
                                         (?P<deg>180|1[0-7]\d|0\d{2})  # Degrees
                                         (?P<min>[0-5]\d)  # Minutes
                                         (?P<sec>[0-5]\d\.\d+$|[0-5]\d$)  # Seconds             
                                      ''', re.VERBOSE),
        'DMH_COMPACTED': re.compile(r'''(?P<deg>^180|^1[0-7]\d|^0\d{2})  # Degrees
                                        (?P<min>[0-5]\d\.\d+|[0-5]\d)  # Minutes
                                        (?P<hem>[EW]$)  # Hemisphere
                                    ''', re.VERBOSE),
        'HDM_COMPACTED': re.compile(r'''(?P<hem>^[EW])  # Hemisphere
                                        (?P<deg>180|1[0-7]\d|0\d{2})  # Degrees
                                        (?P<min>[0-5]\d\.\d+$|[0-5]\d$)  # Minutes
                                    ''', re.VERBOSE)
    },
    AT_LATITUDE: {
        'DMSH_COMPACTED': re.compile(r'''(?P<deg>^90|^[0-8]\d)  # Degrees
                                         (?P<min>[0-5]\d)  # Minutes
                                         (?P<sec>[0-5]\d\.\d+|[0-5]\d)  # Seconds
                                         (?P<hem>[NS]$)  # Hemisphere
                                    ''', re.VERBOSE),
        'HDMS_COMPACTED': re.compile(r'''(?P<hem>^[NS])  # Hemisphere
                                         (?P<deg>90|[0-8]\d)  # Degrees
                                         (?P<min>[0-5]\d)  # Minutes
                                         (?P<sec>[0-5]\d\.\d+$|[0-5]\d$)  # Seconds
                                     ''', re.VERBOSE),
        'DMH_COMPACTED': re.compile(r'''(?P<deg>^90|^[0-8]\d)  # Degrees
                                        (?P<min>[0-5]\d\.\d+|[0-5]\d)  # Minutes
                                        (?P<hem>[NS]$)  # Hemisphere
                                    ''', re.VERBOSE),
        'HDM_COMPACTED': re.compile(r'''(?P<hem>^[NS])  # Hemisphere
                                         (?P<deg>90|[0-8]\d)  # Degrees
                                         (?P<min>[0-5]\d\.\d+$|[0-5]\d$)  # Seconds
                                    ''', re.VERBOSE)
    }
}


class Coordinate(Angle):

    def __init__(self, ang_src, ang_type, ang_label=None):
        Angle.__init__(self)
        self.ang_src = ang_src
        self.ang_type = ang_type
        self.ang_label = ang_label
        self.ang_dd = None
        self.err_msg = ""
        self.validate_coordinate()

    def __str__(self):
        return self.ang_src

    @staticmethod
    def is_coordinate_within_range(coord_dd, ang_type):
        """  Check if coordinate is within range for specified angle type.
        :param coord_dd: float, coordinate to check
        :param ang_type: const(str): type of angle
        :return:
        """
        if ang_type == AT_LONGITUDE:
            return bool(-180 <= coord_dd <= 180)
        elif ang_type == AT_LATITUDE:
            return bool(-90 <= coord_dd <= 90)

    @staticmethod
    def convert_compacted_to_dd(ang, ang_type):
        """ Converts DMSH or HDMS format into DD format.
        :param ang: str
        :param ang_type: str
        :return: float: angle in decimal degrees format, if conversion failed (not supported format,
                 error in angle example minutes >= 60, incorrect type - returns None)
        """
        dd = None
        for coord_type, pattern in COORDINATE_COMPACTED[ang_type].items():
            if pattern.match(ang):
                if coord_type in ['DMSH_COMPACTED', 'HDMS_COMPACTED']:
                    dmsh_parts = pattern.search(ang)
                    d = int(dmsh_parts.group('deg'))
                    m = int(dmsh_parts.group('min'))
                    s = float(dmsh_parts.group('sec'))
                    h = dmsh_parts.group('hem')
                    dd = Coordinate.dmsh_parts_to_dd((d, m, s, h))
                elif coord_type in ['DMH_COMPACTED', 'HDM_COMPACTED']:
                    dmh_parts = pattern.search(ang)
                    d = int(dmh_parts.group('deg'))
                    m = float(dmh_parts.group('min'))
                    h = dmh_parts.group('hem')
                    dd = Coordinate.dmh_parts_to_dd((d, m, h))
        if dd:
            if Coordinate.is_coordinate_within_range(dd, ang_type):
                return dd

    def validate_coordinate(self):
        if not self.ang_src.strip():
            self.ang_dd = None
            if self.ang_label:
                self.err_msg = "{} is required!".format(self.ang_label)
            else:
                if self.ang_type == AT_LONGITUDE:
                    self.err_msg = "Longitude is required!"
                elif self.ang_type == AT_LATITUDE:
                    self.err_msg = "Latitude is required!"
        else:
            ang_norm = Coordinate.normalize_angle(self.ang_src)
            self.ang_dd = Coordinate.convert_compacted_to_dd(ang_norm, self.ang_type)
            if self.ang_dd is None:
                if self.ang_label:
                    self.err_msg = "{} error or not supported format!".format(self.ang_label)
                else:
                    if self.ang_type == AT_LONGITUDE:
                        self.err_msg = "Longitude error or not supported format!"
                    elif self.ang_type == AT_LATITUDE:
                        self.err_msg = "Latitude error or not supported format!"
