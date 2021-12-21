from typing import Union


class AviationBase:

    @staticmethod
    def normalize(value: str) -> str:
        """
        >>> assert AviationBase.normalize("   123    ") == "123"
        >>> assert AviationBase.normalize("123\\n") == "123"
        >>> assert AviationBase.normalize("123,123") == "123.123"
        >>> assert AviationBase.normalize("n770000") == "N770000"
        >>> assert AviationBase.normalize(" n77 00 00,00") == "N77 00 00.00"
        """
        return value.strip().replace(",", ".").upper()

    @staticmethod
    def convert_to_number(value: Union[str, int, float]) -> float:
        """
        >>> assert AviationBase.convert_to_number(1) == 1.0
        >>> assert AviationBase.convert_to_number(1.123) == 1.123
        >>> assert AviationBase.convert_to_number('1') == 1.0
        >>> assert AviationBase.convert_to_number('1.123') == 1.123
        >>> assert AviationBase.convert_to_number('1,123') == 1.123
        """
        if type(value) == str:
            try:
                return float(AviationBase.normalize(value))
            except ValueError:
                pass
        else:
            return float(value)
