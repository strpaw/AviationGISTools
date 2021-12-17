from aviation_gis_tools.coordinate import *
from aviation_gis_tools.distance import *
from aviation_gis_tools.bearing import *
from aviation_gis_tools.ellipsoid_calc import *


def check_point_definition(func):
    """ Check input data for point calculated from 'raw coordinates', polar coordinates, offset coordinates"""
    def wrapper(*args, **kwargs):
        err = ''
        for argname, argvalue in kwargs.items():
            if argname == 'point_id':
                if not argvalue.strip():
                    err = 'Point ident required. '
            if argname == 'lon':
                if argvalue.ang_type != AT_LONGITUDE:
                    err += f'Arg lon: Coordinate type longitude expected, type {argvalue.ang_type} passed. '
            if argname == 'lat':
                if argvalue.ang_type != AT_LATITUDE:
                    err += f'Arg lat: Coordinate type latitude expected, type {argvalue.ang_type} passed. '

        err += ' '.join([argvalue.err_msg for argname, argvalue in kwargs.items()
                         if argname in ['distance', 'azimuth', 'offset_distance', 'lon', 'lat'] and argvalue.err_msg])
        if err:
            raise ValueError(err)
        return func(*args, **kwargs)
    return wrapper


class Point:

    def __init__(self, point_id, lon, lat, definition=None):
        self._point_id = point_id
        self._lon = lon
        self._lat = lat
        self._definition = definition

    def __str__(self):
        lon_dms = Angle.convert_dd_to_dms(self._lon, AT_LONGITUDE)
        lat_dms = Angle.convert_dd_to_dms(self._lat, AT_LATITUDE)
        return f'{lon_dms} {lat_dms}'

    @staticmethod
    def get_offset_azimuth(azimuth, offset_side):
        """
        :param azimuth float
        :param offset_side: str, "LEFT" or "RIGHT"
        :return: float
        """

        if offset_side == 'LEFT':
            offset_azimuth = azimuth - 90
        elif offset_side == 'RIGHT':
            offset_azimuth = azimuth + 90
        # Normalize azm to [0,360] degrees
        if offset_azimuth < 0:
            offset_azimuth += 360
        elif offset_azimuth > 360:
            offset_azimuth -= 360

        return offset_azimuth

    @classmethod
    @check_point_definition
    def from_raw_coordinates(cls, *, point_id: str, lon: Coordinate, lat: Coordinate) -> 'Point':
        """ Create Point from 'raw' coordinates, example: 'E0150000', 'N770000'. """
        return cls(point_id, lon.ang_dd, lat.ang_dd, definition=f'{lon} {lat}')

    @classmethod
    @check_point_definition
    def from_polar_coordinates(cls, *, ref_point: 'Point', point_id: str, distance: Distance, azimuth: Bearing) -> 'Point':
        """ Create point based on:
                reference point longitude, latitude
                distance from reference point to calculated point
                azimuth from reference point to calculated point
        """
        try:
            lon_dd, lat_dd = vincenty_direct_solution(lon_initial=ref_point._lon,
                                                      lat_initial=ref_point._lat,
                                                      azimuth_initial=azimuth.brng_dd,
                                                      distance=distance.convert_distance_to_uom(UOM_M))
        except TypeError:
            pass  # TODO: add handling error: TypeError: cannot unpack non-iterable NoneType object
        else:
            definition = f'Ref: {ref_point._point_id} {ref_point._definition}; ' \
                         f'Dist: {distance}; Azm: {azimuth}'
            return cls(point_id, lon_dd, lat_dd, definition)

    @classmethod
    @check_point_definition
    def from_offset(cls, *, ref_point: 'Point', point_id: str, distance: Distance, azimuth: Bearing, offset_side: str,
                    offset_distance: Distance) -> 'Point':
        """ Create point based on:
                reference point longitude, latitude
                'offset' side: LEFT, RIGHT
                distance from reference point along azimuth
                distance from azimuth line to calculated point
        """
        try:
            offset_azimuth = Point.get_offset_azimuth(azimuth.brng_dd, offset_side)

            # Calculate 'intermediate' point
            inter_lon, inter_lat = vincenty_direct_solution(lon_initial=ref_point._lon,
                                                            lat_initial=ref_point._lat,
                                                            azimuth_initial=azimuth.brng_dd,
                                                            distance=distance.convert_distance_to_uom(UOM_M))

            lon_dd, lat_dd = vincenty_direct_solution(lon_initial=inter_lon,
                                                      lat_initial=inter_lat,
                                                      azimuth_initial=offset_azimuth,
                                                      distance=offset_distance.convert_distance_to_uom(UOM_M))
        except TypeError:
            pass  # TODO: add handling error: TypeError: cannot unpack non-iterable NoneType object
        else:
            definition = f'Ref: {ref_point._point_id} {ref_point._definition}; ' \
                         f'Dist: {distance}; Azm: {azimuth}; ' \
                         f'Offset side: {offset_side}; Offset dist: {offset_distance}'
            return cls(point_id, lon_dd, lat_dd, definition)


class PointCalculation:

    def __init__(self, ref_id, ref_lon, ref_lat):
        self.ref_id = ref_id
        self.ref_lon = Coordinate(ref_lon, AT_LONGITUDE)
        self.ref_lat = Coordinate(ref_lat, AT_LATITUDE)
        self._ref_err = ""
        self._calc_err = ""
        self._check_point()

    @property
    def ref_err(self):
        return self._ref_err

    @property
    def calc_err(self):
        return self._calc_err

    def _check_point(self):
        if self.ref_id.strip() == "":
            self._ref_err = "Reference point id required!"

        if self.ref_lon.err_msg:
            self._ref_err += "{} longitude error or not supported format!".format(self.ref_id)

        if self.ref_lat.err_msg:
            self._ref_err += "{} latitude error or not supported format!".format(self.ref_id)

    @staticmethod
    def check_location_definition(*args):
        err_msg = ""
        for arg in args:
            if arg.err_msg:
                err_msg += arg.err_msg
        return err_msg

    def point_by_polar_coordinates(self, distance, azimuth):
        """ Calculate longitude, latitude base on:
                reference point longitude, latitude
                distance from reference point to calculated point
                azimuth from reference point to calculated point
        :param distance: Distance
        :param azimuth: Bearing
        :return: tuple(float, float)
        """
        self._calc_err = ""
        self._calc_err = self._calc_err + PointCalculation.check_location_definition(distance, azimuth)
        if not self._calc_err:
            return vincenty_direct_solution(lon_initial=self.ref_lon.ang_dd,
                                            lat_initial=self.ref_lat.ang_dd,
                                            azimuth_initial=azimuth.brng_dd,
                                            distance=distance.convert_distance_to_uom(UOM_M))

    def info_by_polar_coordinates(self, distance, azimuth):
        """ Return 'info' string related to calculated point based on:
                reference point longitude, latitude
                distance from reference point to calculated point
                azimuth from reference point to calculated point
        Note: It does not check correctness of input (distance, azimuth) -
        use only right after calculation point by polar coordinates!
        :param distance: Distance
        :param azimuth: Bearing
        :return: str
        """
        return "Reference point:  Id {0.ref_id} Coordinates {0.ref_lon} {0.ref_lat}, " \
               "Distance: {1}, Azimuth: {2} ".format(self, distance, azimuth)

    @staticmethod
    def get_offset_azimuth(azimuth, offset_side):
        """
        :param azimuth float
        :param offset_side: str, "LEFT" or "RIGHT"
        :return: float
        """

        if offset_side == 'LEFT':
            offset_azimuth = azimuth - 90
        elif offset_side == 'RIGHT':
            offset_azimuth = azimuth + 90
        # Normalize azm to [0,360] degrees
        if offset_azimuth < 0:
            offset_azimuth += 360
        elif offset_azimuth > 360:
            offset_azimuth -= 360

        return offset_azimuth

    def point_by_offset(self, distance, azimuth, offset_side, offset_distance):
        """
        
        """
        self._calc_err = ""
        self._calc_err = self._calc_err + PointCalculation.check_location_definition(distance, azimuth, offset_distance)
        if not self._calc_err:
            offset_azimuth = PointCalculation.get_offset_azimuth(azimuth.brng_dd, offset_side)

            # Calculate 'intermediate' point
            inter_lon, inter_lat = vincenty_direct_solution(lon_initial=self.ref_lon.ang_dd,
                                                            lat_initial=self.ref_lat.ang_dd,
                                                            azimuth_initial=azimuth.brng_dd,
                                                            distance=distance.convert_distance_to_uom(UOM_M))

            return vincenty_direct_solution(lon_initial=inter_lon,
                                            lat_initial=inter_lat,
                                            azimuth_initial=offset_azimuth,
                                            distance=offset_distance.convert_distance_to_uom(UOM_M))

    def info_by_offset(self, distance, azimuth, offset_side, offset_distance):
        """ Return 'info' string related to calculated point based on:
                reference point longitude, latitude
                distance from reference point to calculated point
                azimuth from reference point to calculated point
        Note: It does not check correctness of input (distance, azimuth, offset_distance) -
        use only right after calculation point by offset!
        :param distance: Distance
        :param azimuth: Bearing
        :param offset_side: str, 'LEFT' or 'RIGHT'
        :param offset_distance: Distance
        :return: str
        """
        return "Reference point:  Id {0.ref_id} Coordinates {0.ref_lon} {0.ref_lat}, " \
               "Distance: {1}, Azimuth: {2}, Offset side: {3}, Offset distance: {4}".format(self, distance, azimuth,
                                                                                            offset_side,
                                                                                            offset_distance)
