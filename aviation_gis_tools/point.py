from aviation_gis_tools.coordinate import *


class Point:

    def __init__(self, lon, lat, name):
        self.lon = Coordinate(lon, AT_LONGITUDE)
        self.lat = Coordinate(lat, AT_LATITUDE)
        self.name = name
        self.err_msg = ""
        self.check_point()

    def check_point(self):
        if self.lon.err_msg or self.lat.err_msg:
            if self.lon.err_msg:
                self.err_msg += "{} longitude error or not supported format!".format(self.name)
            if self.lat.err_msg:
                self.err_msg += "{} latitude error or not supported format!".format(self.name)
