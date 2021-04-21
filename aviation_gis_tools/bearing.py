from aviation_gis_tools.angle import *


BEARING_COMPACTED = {
    "DMS_COMPACTED": re.compile(r'''(?P<deg>^360|^[0-2]\d{2}|^0\d{2})  # Degrees
                                    (?P<min>[0-5]\d)  # Minutes
                                    (?P<sec>[0-5]\d\.\d+$|[0-5]\d$)  # Seconds
                                 ''', re.VERBOSE),
    "DM_COMPACTED": re.compile(r'''(?P<deg>^360|^[0-2]\d{2}|^0\d{2})  # Degrees
                                   (?P<min>[0-5]\d\.\d+$|[0-5]\d$)  # Minutes
                             ''', re.VERBOSE),
}


class Bearing(Angle):

    def __init__(self, brng_src, brng_label="Bearing"):
        Angle.__init__(self)
        self.brng_src = brng_src
        self.brng_label = brng_label
        self.brng_dd = None
        self.err_msg = ""
        self.validate_brng()

    @staticmethod
    def is_within_range(brng_dd):
        """  Check if bearing is within range <0, 360>.
        :param brng_dd: float
        :return: bool
        """
        return bool(0 <= brng_dd <= 360)

    @staticmethod
    def convert_compacted_dms_to_dd(brng_src, pattern):
        if pattern.match(brng_src):
            dms_parts = pattern.search(brng_src)
            d = int(dms_parts.group('deg'))
            m = int(dms_parts.group('min'))
            s = float(dms_parts.group('sec'))
            dd = d + m / 60 + s / 3600
            if Bearing.is_within_range(dd):
                return dd

    @staticmethod
    def convert_compacted_dm_to_dd(brng_src, pattern):
        if pattern.match(brng_src):
            dms_parts = pattern.search(brng_src)
            d = int(dms_parts.group('deg'))
            m = float(dms_parts.group('min'))
            dd = d + m / 60
            if Bearing.is_within_range(dd):
                return dd

    @staticmethod
    def convert_brng_to_dd(brng_src):
        dd = Bearing.convert_compacted_dms_to_dd(brng_src, BEARING_COMPACTED["DMS_COMPACTED"])

        if dd is None:
            dd = Bearing.convert_compacted_dm_to_dd(brng_src, BEARING_COMPACTED["DM_COMPACTED"])
        return dd

    def validate_brng(self):
        err_required = '{label} is required.'
        err_value = '{label} value error or format not supported.'

        if self.brng_src.strip() == "":
            self.err_msg += err_required.format(label=self.brng_label)
        else:
            brng_norm = Bearing.normalize_angle(self.brng_src)
            dd = self.convert_brng_to_dd(brng_norm)
            if dd is None:
                self.err_msg += err_value.format(label=self.brng_label)
            else:
                self.brng_dd = dd
