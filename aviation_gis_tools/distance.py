"""
distance.py
Distance module provides functionality to distance validation and conversion
"""
from .const import *


class Distance:
    """ Class covers actions related to distance: validation, conversion among various units of measure (UOM).
    Attributes:
    -----------
    src_dist : str
        Keeps source value of distance, note that this value can be with comma decimal separator not dot decimal
        separator, example: 109,25 109.25.
    src_uom : str
        Keeps source unit of measure of distance, e.g. UOM_M, UOM_KM.
    dist_label: str
        Keeps customized label for distance that will be used in err_msg, e. g. Circle radius,
    err_msg: str
        Keeps error message why distance is not valid, for example is unit of measure is not valid.
    is_valid: bool
        Keeps information if distance is valid or not.
        Distance if considered as valid if src_dist can be converted into float number
        and src_uom is valid unit of measure.
    num_dist: float
        Keeps source distance as float in source unit of measure, only if src_dist is valid.
    """

    def __init__(self, src_dist, src_uom=UOM_M, dist_label='Distance'):
        self.src_dist = src_dist
        self.src_uom = src_uom
        self.dist_label = dist_label
        self.err_msg = ''
        self.is_valid = None
        self.num_dist = None
        self.check_distance()

    def check_distance_value(self):
        """ Check if distance is valid: int or float positive number (also with comma as decimal point),
        e. g.:  1455.5; 1455,5
        :return: bool
        """
        if isinstance(self.src_dist, str):
            dist_norm = self.src_dist.strip().replace(',', '.')
            try:
                d = float(dist_norm)
                if d > 0:
                    self.num_dist = d
                    return True
            except ValueError:
                return False
        elif isinstance(self.src_dist, (float, int)):
            if self.src_dist > 0:
                self.num_dist = self.src_dist
                return True

    def check_distance_uom(self):
        """ Check if source distance UOM is valid.
        :return: bool
        """
        return bool(self.src_uom in UOM_LIST)

    def check_distance(self):
        """ Check if distance is valid: check i both source UOM and source (initial) distance are valid. """
        err_required = '{label} is required.'
        err_uom = '{label} UOM error.'
        err_value = '{label} value error.'
        self.is_valid = True

        if self.src_dist == "":
            self.err_msg += err_required.format(label=self.dist_label)
            self.is_valid = False

        is_valid_uom = self.check_distance_uom()
        if not is_valid_uom:
            self.err_msg += err_uom.format(label=self.dist_label)
            self.is_valid = False

        if self.src_dist:
            is_valid_distance_value = self.check_distance_value()
            if not is_valid_distance_value:
                self.err_msg += err_value.format(label=self.dist_label)
                self.is_valid = False

    def convert_distance_to_meters(self):
        """ Convert source distance value from source UOM to meters. """
        if self.src_uom == UOM_M:
            return self.num_dist
        elif self.src_uom == UOM_KM:
            return self.num_dist * 1000
        elif self.src_uom == UOM_NM:
            return self.num_dist * 1852
        elif self.src_uom == UOM_FT:
            return self.num_dist * 0.3048
        elif self.src_uom == UOM_SM:
            return self.num_dist * 1609.344

    @staticmethod
    def convert_meters_to_uom(dist_m, to_uom):
        """ Convert distance from meters to given UOM. """
        if to_uom in UOM_LIST:
            if to_uom == UOM_M:
                return dist_m
            elif to_uom == UOM_KM:
                return dist_m / 1000
            elif to_uom == UOM_NM:
                return dist_m / 1852
            elif to_uom == UOM_FT:
                return dist_m / 0.3048
            elif to_uom == UOM_SM:
                return dist_m / 1609.344

    def convert_distance_to_uom(self, to_uom):
        """ Convert distance between various units. """
        if self.is_valid:
            if to_uom in UOM_LIST:
                if self.src_uom == to_uom:
                    return self.num_dist
                else:
                    dist_m = self.convert_distance_to_meters()
                    return self.convert_meters_to_uom(dist_m, to_uom)
