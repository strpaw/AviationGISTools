"""
distance.py module:
Handling distance conversion among various unit of measure, distance validation.
"""
from typing import Dict, Union
from aviation_gis_tools.aviation_base import AviationBase

# Units of measure
UOM_M: str = 'm'
UOM_KM: str = 'km'
UOM_NM: str = 'NM'
UOM_FT: str = 'ft'
UOM_SM: str = 'SM'

SUPPORTED_UOMS: set = {UOM_M, UOM_KM, UOM_NM, UOM_FT, UOM_SM}

DISTANCE_CONVERSION_FACTORS: Dict[str, float] = {
    UOM_KM: 1000.0,
    UOM_NM: 1852.0,
    UOM_FT: 0.3048,
    UOM_SM: 1609.344
}


def distance_conversion_possible(mth):
    def _(self, to_uom):
        err_msg = ""
        if self._num_value is None:
            err_msg = self._err
        if not self.is_supported_uom(to_uom):
            err_msg += f"Destination UOM not supported: {to_uom}"

        if err_msg:
            raise ValueError(f"Incorrect data to convert: {err_msg}")

        return mth(self, to_uom)
    return _


class Distance(AviationBase):

    def __init__(self,
                 value: Union[int, float, str],
                 uom: str = UOM_M,
                 allow_negative: bool = False
                 ) -> None:
        """
        >>> d = Distance(100)
        >>> assert isinstance(d, Distance)
        >>> assert d._value == 100
        >>> assert d._uom == 'm'
        >>> assert d._num_value == 100.0
        >>> assert d._allow_negative is False
        >>> assert isinstance(d._uom, str)
        >>> d = Distance('100', UOM_KM)
        >>> assert d._value == '100'
        >>> assert d._uom == 'km'
        >>> assert d._num_value == 100.0
        """
        AviationBase.__init__(self)
        self._value: Union[int, float, str] = value
        self._uom: str = uom
        self._allow_negative: bool = allow_negative
        self._err: str = ""
        self._num_value: Union[float, None] = Distance.convert_to_number(self._value)
        self.check_source_values()

    def check_source_values(self) -> None:
        """
        >>> d = Distance(100)
        >>> assert d._err == ""
        >>> d = Distance('100,1', UOM_NM)
        >>> assert d._err == ""
        >>> d = Distance(100, 'UOM_TEST')
        >>> assert d._err == "Not supported UOM: UOM_TEST."
        >>> d = Distance('100a', UOM_KM)
        >>> assert d._err == "Source value error: 100a."
        >>> d = Distance('100a', 'UOM_TEST')
        >>> assert d._err == "Not supported UOM: UOM_TEST.Source value error: 100a."
        """
        if not Distance.is_supported_uom(self._uom):
            self._err = f'Not supported UOM: {self._uom}.'
        if self._num_value is None:
            self._err += f'Source value error: {self._value}.'

    def __str__(self):
        """
        >>> d = Distance(100)
        >>> print(d)
        100 m
        >>> d = Distance('123.44', UOM_KM)
        >>> print(d)
        123.44 km
        """
        return f"{self._value} {self._uom}"

    def __eq__(self,
               other: 'Distance'
               ) -> bool:
        """
        >>> assert Distance(1234) == Distance(1234)
        >>> assert Distance('123', UOM_KM) == Distance(123, UOM_KM)
        >>> assert Distance(1230) == Distance('1.23', UOM_KM)
        >>> assert Distance(304.800, UOM_M) == Distance('1000', UOM_FT)
        """
        if isinstance(other, Distance) and \
           self.convert_to_meters() == other.convert_to_meters():
            return True

    def __neg__(self,
                other: 'Distance'
                ) -> bool:
        """
        >>> assert not Distance(1234) == Distance(1234, UOM_FT)
        >>> assert not Distance('1.23', UOM_KM) == Distance(1230.1, UOM_M)
        >>> assert not Distance(3048, UOM_M) == Distance('1000.00')
        """
        return not self.__eq__(other)

    @staticmethod
    def is_supported_uom(uom: str) -> bool:
        """
        >>> assert isinstance(Distance.is_supported_uom(UOM_NM), bool)
        >>> assert isinstance(Distance.is_supported_uom('NOT_SUPPORTED_UOM'), bool)
        >>> assert Distance.is_supported_uom(UOM_NM)
        >>> assert Distance.is_supported_uom('NOT_SUPPORTED_UOM') is False
        """
        return uom in SUPPORTED_UOMS

    def convert_to_meters(self) -> Union[float, None]:
        """
        >>> d = Distance(135.75)
        >>> assert d.convert_to_meters() == 135.75
        >>> d = Distance(1.0455, UOM_KM)
        >>> assert d.convert_to_meters() == 1045.5
        >>> d = Distance(17.355, UOM_NM)
        >>> assert round(d.convert_to_meters(), 7) == 32141.46
        >>> d = Distance(783.2, UOM_FT)
        >>> assert round(d.convert_to_meters(), 7) == 238.71936
        >>> d = Distance(5.8, UOM_SM)
        >>> assert round(d.convert_to_meters(), 7) == 9334.1952
        """
        if self._num_value is None:
            return

        if self._uom == UOM_M:
            return self._num_value
        else:
            return self._num_value * DISTANCE_CONVERSION_FACTORS[self._uom]

    @distance_conversion_possible
    def convert_meters_to_uom(self,
                              dist_m: float,
                              to_uom: str
                              ) -> Union[float, None]:
        if to_uom == UOM_M:
            return dist_m
        else:
            return dist_m / DISTANCE_CONVERSION_FACTORS[to_uom]

    @distance_conversion_possible
    def convert_to_uom(self, to_uom: str) -> Union[float, None]:
        """ Convert distance between various units.
        >>> d = Distance(1455)
        >>> assert d.convert_to_uom(UOM_M) == 1455
        >>> assert d.convert_to_uom(UOM_KM) == 1.455
        >>> assert d.convert_to_uom(UOM_NM) == 0.7856371490280778
        >>> assert d.convert_to_uom(UOM_FT) == 4773.622047244095
        >>> assert d.convert_to_uom(UOM_SM) == 0.9040950847053209
        >>> d = Distance(1.455, UOM_KM)
        >>> assert d.convert_to_uom(UOM_M) == 1455
        >>> assert d.convert_to_uom(UOM_KM) == 1.455
        >>> assert d.convert_to_uom(UOM_NM) == 0.7856371490280778
        >>> assert d.convert_to_uom(UOM_FT) == 4773.622047244095
        >>> assert d.convert_to_uom(UOM_SM) == 0.9040950847053209
        >>> d = Distance(2.79, UOM_NM)
        >>> assert d.convert_to_uom(UOM_M) == 5167.08
        >>> assert d.convert_to_uom(UOM_KM) == 5.16708
        >>> assert d.convert_to_uom(UOM_NM) == 2.79
        >>> assert d.convert_to_uom(UOM_FT) == 16952.36220472441
        >>> assert d.convert_to_uom(UOM_SM) == 3.2106746599856835
        >>> d = Distance(3722.5, UOM_FT)
        >>> assert d.convert_to_uom(UOM_M) == 1134.6180000000002
        >>> assert d.convert_to_uom(UOM_KM) == 1.1346180000000002
        >>> assert d.convert_to_uom(UOM_NM) == 0.6126447084233262
        >>> assert d.convert_to_uom(UOM_FT) == 3722.5
        >>> assert d.convert_to_uom(UOM_SM) == 0.7050189393939394
        >>> d = Distance('2.3', UOM_SM)
        >>> assert d.convert_to_uom(UOM_M) == 3701.4912
        >>> assert d.convert_to_uom(UOM_KM) == 3.7014912
        >>> assert d.convert_to_uom(UOM_NM) == 1.9986453563714903
        >>> assert d.convert_to_uom(UOM_FT) == 12144.0
        >>> assert d.convert_to_uom(UOM_SM) == 2.3
        """
        if self._uom == to_uom:
            return self._value
        else:
            dist_m = self.convert_to_meters()
            return self.convert_meters_to_uom(dist_m, to_uom)
