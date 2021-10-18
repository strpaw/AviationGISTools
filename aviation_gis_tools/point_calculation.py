from aviation_gis_tools.coordinate import *


class PointCalculation:

    def __init__(self, ref_id, ref_lon, ref_lat):
        self.ref_id = ref_id
        self.ref_lon = Coordinate(ref_lon, AT_LONGITUDE)
        self.ref_lat = Coordinate(ref_lat, AT_LATITUDE)
        self.err_msg = ""
        self.check_point()

    def check_point(self):
        self.err_msg = ""
        if self.ref_id.strip() == "":
            self.err_msg = "Reference point id required!"

        if self.ref_lon.err_msg:
            self.err_msg += "{} longitude error or not supported format!".format(self.ref_id)

        if self.ref_lat.err_msg:
            self.err_msg += "{} latitude error or not supported format!".format(self.ref_id)
