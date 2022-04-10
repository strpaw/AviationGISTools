"""
point.py module:
Tools for working with points (longitude, latitude) such as:
    - converting do decimal degrees
    - calculating longitude, latitude based on:
        other point longitude, latitude and:
         azimuth, distance
         azimuth, distance, offset side, offset distance
         local Cartesian coordinates into longitude, latitude
"""
from distance import Distance
from coordinate import Coordinate, AT_LONGITUDE, AT_LATITUDE
from ellipsoid_calc import vincenty_direct_solution
from typing import Union, Tuple
from functools import wraps


def check_point_definition(func):
    """ Check input data for point calculated from 'raw coordinates', polar coordinates, offset coordinates"""
    @wraps(func)
    def _(*args, **kwargs):
        err = ''
        for aname, avalue in kwargs.items():

            if aname in ['dist', 'offset_dist']:
                if avalue.err:
                    err += f'{aname}: {avalue.err}'

            if aname == 'azimuth':
                try:
                    float(avalue)
                except ValueError:
                    err += f'Azimuth value error: {avalue}.'

            if aname == 'offset_side':
                if avalue not in ['LEFT', 'RIGHT']:
                    err += f'Offset side error: {avalue}.'

        if err:
            raise ValueError(err)
        return func(*args, **kwargs)
    return _


class Point:

    """
    Attributes
    ----------
    _lon: Coordinate
       point longitude
    _lat: Coordinate
        point latitude
    _ident: str
    _err_msg: str
        check result during initializing Point form source values
    """
    def __init__(self,
                 lon: Union[int, float, str],
                 lat: Union[int, float, str],
                 ident: str) -> None:
        """
        >>> p = Point(lon='E0203000', lat='N553000', ident='TEST1')
        >>> assert p.err_msg == ''
        >>> assert p.lon.coord_dd == 20.5
        >>> assert p.lat.coord_dd == 55.5
        """
        self._ident = ident
        self._err_msg = ''

        try:
            self._lon = Coordinate(coord_src=lon,
                                   coord_type=AT_LONGITUDE,
                                   coord_label=f'{ident} longitude')
        except ValueError as e:
            self._err_msg += str(e)

        try:
            self._lat = Coordinate(coord_src=lat,
                                   coord_type=AT_LATITUDE,
                                   coord_label=f'{ident} latitude')
        except ValueError as e:
            self._err_msg += str(e)

    @property
    def lon(self):
        return self._lon

    @property
    def lat(self):
        return self._lat

    @property
    def err_msg(self):
        return self._err_msg

    @staticmethod
    def get_offset_azimuth(azimuth: float, offset_side: str) -> float:
        """
        :param azimuth float
        :param offset_side: str, 'LEFT' or 'RIGHT'
        :return: float
        >>> assert Point.get_offset_azimuth(30, 'RIGHT') == 120
        >>> assert Point.get_offset_azimuth(30, 'LEFT') == 300
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

    @check_point_definition
    def distance_azimuth_to_coordinates(self,
                                        *,
                                        dist: Distance,
                                        azimuth: float) -> Union[Tuple[float, float, str], None]:
        """
        >>> ref_p = Point(lon='E0203000', lat='N553030', ident='TEST1')
        >>> calc_p = ref_p.distance_azimuth_to_coordinates(dist=Distance('100'), azimuth=123)
        >>> assert calc_p == (20.501327360665666, 55.507844127311515, 'Ref: TEST1; Dist: 100 m; Azm: 123')
        >>> ref_p.distance_azimuth_to_coordinates(dist=Distance('100A'), azimuth=123)
        Traceback (most recent call last):
        ...
        ValueError: dist: Source value error: 100A.
        >>> ref_p.distance_azimuth_to_coordinates(dist=Distance('100'), azimuth='123A')
        Traceback (most recent call last):
        ...
        ValueError: Azimuth value error: 123A.
        >>> ref_p.distance_azimuth_to_coordinates(dist=Distance('100A'), azimuth='123A')
        Traceback (most recent call last):
        ...
        ValueError: dist: Source value error: 100A.Azimuth value error: 123A.
        """
        lon_dd, lat_dd = vincenty_direct_solution(lon_initial=self._lon.coord_dd,
                                                  lat_initial=self._lat.coord_dd,
                                                  azimuth_initial=azimuth,
                                                  distance_meters=dist.convert_to_meters())
        definition = f'Ref: {self._ident}; Dist: {dist}; Azm: {azimuth}'

        return lon_dd, lat_dd, definition

    @check_point_definition
    def distance_azimuth_offset_to_coordinates(self,
                                               *,
                                               dist: Distance,
                                               azimuth: float,
                                               offset_side: str,
                                               offset_dist: Distance) -> Union[Tuple[float, float, str], None]:
        """
        >>> ref_p = Point(lon='E0203000', lat='N553030', ident='TEST1')
        >>> calc_p = ref_p.distance_azimuth_offset_to_coordinates(dist=Distance(1800),
        ...                                                       azimuth=123,
        ...                                                       offset_side='LEFT',
        ...                                                       offset_dist=Distance(120))
        >>> assert calc_p == (20.524921659116107, 55.50042937578661,
        ...                   'Ref: TEST1; Dist: 1800 m; Azm: 123; Offset side: LEFT; Offset dist: 120 m')
        >>> calc_p = ref_p.distance_azimuth_offset_to_coordinates(dist=Distance('1800A'),
        ...                                                       azimuth=123,
        ...                                                       offset_side='LEFT',
        ...                                                       offset_dist=Distance(120))
        Traceback (most recent call last):
        ...
        ValueError: dist: Source value error: 1800A.
        >>> calc_p = ref_p.distance_azimuth_offset_to_coordinates(dist=Distance('1800'),
        ...                                                       azimuth='123A',
        ...                                                       offset_side='LEFT',
        ...                                                       offset_dist=Distance(120))
        Traceback (most recent call last):
        ...
        ValueError: Azimuth value error: 123A.
        >>> calc_p = ref_p.distance_azimuth_offset_to_coordinates(dist=Distance('1800'),
        ...                                                       azimuth=123,
        ...                                                       offset_side='TEST',
        ...                                                       offset_dist=Distance(120))
        Traceback (most recent call last):
        ...
        ValueError: Offset side error: TEST.
        >>> calc_p = ref_p.distance_azimuth_offset_to_coordinates(dist=Distance('1800'),
        ...                                                       azimuth=123,
        ...                                                       offset_side='LEFT',
        ...                                                       offset_dist=Distance('120A'))
        Traceback (most recent call last):
        ...
        ValueError: offset_dist: Source value error: 120A.
        >>> calc_p = ref_p.distance_azimuth_offset_to_coordinates(dist=Distance('1800'),
        ...                                                       azimuth='123A',
        ...                                                       offset_side='TEST',
        ...                                                       offset_dist=Distance('120A'))
        Traceback (most recent call last):
        ...
        ValueError: Azimuth value error: 123A.Offset side error: TEST.offset_dist: Source value error: 120A.
        """
        offset_azimuth = Point.get_offset_azimuth(azimuth, offset_side)

        # Calculate 'intermediate' point
        inter_lon, inter_lat = vincenty_direct_solution(lon_initial=self._lon.coord_dd,
                                                        lat_initial=self._lat.coord_dd,
                                                        azimuth_initial=azimuth,
                                                        distance_meters=dist.convert_to_meters())

        # Calculate 'final' point
        lon_dd, lat_dd = vincenty_direct_solution(lon_initial=inter_lon,
                                                  lat_initial=inter_lat,
                                                  azimuth_initial=offset_azimuth,
                                                  distance_meters=offset_dist.convert_to_meters())

        definition = f'Ref: {self._ident}; ' \
                     f'Dist: {dist}; Azm: {azimuth}; ' \
                     f'Offset side: {offset_side}; Offset dist: {offset_dist}'

        return lon_dd, lat_dd, definition
