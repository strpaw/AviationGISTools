"""
The ellipsoid_calc module:  Calculations on ellipsoid
"""
from math import radians, sin, cos, tan, sqrt, atan2, fabs, pi, degrees
from collections import namedtuple
from typing import Tuple

ellipsoid = namedtuple('Ellipsoid', ['a', 'b', 'f'])


ellipsoids = {
    'WGS84': ellipsoid(a=6378137.0, b=6356752.3141, f=1 / 298.25722210088),
    'WGS72': ellipsoid(a=6378135.0, b=6356750.52, f=1 / 298.26000000000)
}


def vincenty_direct_solution(*,
                             lon_initial: float,
                             lat_initial: float,
                             azimuth_initial: float,
                             distance_meters: float,
                             ellipsoid_name: str = "WGS84") -> Tuple[float, float]:
    """ Computes the latitude and longitude of the seond point based on latitude, longitude,
    of the first point and distance and azimuth from first point to second point.
    Uses the algorithm by Thaddeus Vincenty for direct geodetic problem.
    For more information refer to: http://www.ngs.noaa.gov/PUBS_LIB/inverse.pdf.
    >>> vincenty_direct_solution(lon_initial=0.0,
    ...                          lat_initial=0.0,
    ...                          azimuth_initial=0.0,
    ...                          distance_meters=10000.0)
    (0.0, 0.09043694695356691)
    >>> vincenty_direct_solution(lon_initial=0.0,
    ...                          lat_initial=0.0,
    ...                          azimuth_initial=90.0,
    ...                          distance_meters=10000.0)
    (0.08983152841248263, 5.5376636427532604e-18)
    >>> vincenty_direct_solution(lon_initial=0.0,
    ...                          lat_initial=0.0,
    ...                          azimuth_initial=180.0,
    ...                          distance_meters=1000.0)
    (0.0, -0.009043694727216058)
    >>> vincenty_direct_solution(lon_initial=0.0,
    ...                          lat_initial=0.0,
    ...                          azimuth_initial=270.0,
    ...                          distance_meters=10000.0)
    (-0.08983152841248263, -1.661299092825978e-17)
    >>> vincenty_direct_solution(lon_initial=0.0,
    ...                          lat_initial=0.0,
    ...                          azimuth_initial=360.0,
    ...                          distance_meters=100000.0)
    (0.0, 0.9043687229398173)
    >>> vincenty_direct_solution(lon_initial=137.5,
    ...                          lat_initial=-32.5,
    ...                          azimuth_initial=127.5,
    ...                          distance_meters=243855.411,
    ...                          ellipsoid_name='WGS84')
    (139.58969185673908, -33.8212028224309)
    >>> isinstance(vincenty_direct_solution(lon_initial=137.5,
    ...                          lat_initial=-32.5,
    ...                          azimuth_initial=127.5,
    ...                          distance_meters=243855.411,
    ...                          ellipsoid_name='WGS84'), tuple)
    True
    >>> end_coordinates = vincenty_direct_solution(lon_initial=137.5,
    ...                          lat_initial=-32.5,
    ...                          azimuth_initial=127.5,
    ...                          distance_meters=243855.411,
    ...                          ellipsoid_name='WGS84')  # Tuple elements are float
    >>> all(map(lambda coordinate: isinstance(coordinate, float), end_coordinates))
    True
    >>> vincenty_direct_solution(lon_initial=137.5,
    ...                          lat_initial=-32.5,
    ...                          azimuth_initial=127.5,
    ...                          distance_meters=243855.411,
    ...                          ellipsoid_name='not defined ellipsoid') # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    KeyError: Ellipsoid not defined ellipsoid not found!
    >>> vincenty_direct_solution(137.5,
    ...                          -32.5,
    ...                          127.5,
    ...                          243855.411)
    Traceback (most recent call last):
    ...
    TypeError: vincenty_direct_solution() takes 0 positional arguments but 4 were given
    """
    try:
        a, b, f = ellipsoids[ellipsoid_name]
    except KeyError:
        raise KeyError(f'Ellipsoid {ellipsoid_name} not found!')

    lon1 = radians(lon_initial)
    lat1 = radians(lat_initial)
    alpha1 = radians(azimuth_initial)

    sin_alpha1 = sin(alpha1)
    cos_alpha1 = cos(alpha1)

    # u1 - reduced latitude
    tan_u1 = (1 - f) * tan(lat1)
    cos_u1 = 1 / sqrt(1 + tan_u1 * tan_u1)
    sin_u1 = tan_u1 * cos_u1

    # sigma1 - angular distance on the sphere from the equator to initial point
    sigma1 = atan2(tan_u1, cos(alpha1))

    # sin_alpha - azimuth of the geodesic at the equator
    sin_alpha = cos_u1 * sin_alpha1
    cos_sq_alpha = 1 - sin_alpha * sin_alpha
    u_sq = cos_sq_alpha * (a * a - b * b) / (b * b)
    A = 1 + u_sq / 16384 * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
    B = u_sq / 1024 * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))

    sigma = distance_meters / (b * A)
    sigmap = 1
    sin_sigma, cos_sigma, cos2sigma_m = None, None, None

    while fabs(sigma - sigmap) > 1e-12:
        cos2sigma_m = cos(2 * sigma1 + sigma)
        sin_sigma = sin(sigma)
        cos_sigma = cos(sigma)
        d_sigma = B * sin_sigma * (cos2sigma_m + B / 4 * (
                    cos_sigma * (-1 + 2 * cos2sigma_m * cos2sigma_m) - B / 6 * cos2sigma_m * (
                        -3 + 4 * sin_sigma * sin_sigma) * (-3 + 4 * cos2sigma_m * cos2sigma_m)))
        sigmap = sigma
        sigma = distance_meters / (b * A) + d_sigma

    var_aux = sin_u1 * sin_sigma - cos_u1 * cos_sigma * cos_alpha1  # Auxiliary variable

    lat2 = atan2(sin_u1 * cos_sigma + cos_u1 * sin_sigma * cos_alpha1,
                 (1 - f) * sqrt(sin_alpha * sin_alpha + var_aux * var_aux))

    lamb = atan2(sin_sigma * sin_alpha1, cos_u1 * cos_sigma - sin_u1 * sin_sigma * cos_alpha1)
    C = f / 16 * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))
    L = lamb - (1 - C) * f * sin_alpha * (
                sigma + C * sin_sigma * (cos2sigma_m + C * cos_sigma * (-1 + 2 * cos2sigma_m * cos2sigma_m)))

    lon2 = (lon1 + L + 3 * pi) % (2 * pi) - pi

    return degrees(lon2), degrees(lat2)
