# Speed units
SPEED_MS = 'm/s' # Meters per hour
SPEED_KMH = 'km/h'  # Kilometers per hour
SPEED_KT = 'kt'  # Knots = 1 nautical mile per hour


def speed_to_ms(speed, unit):
    """ Convert speed from given speed unit to speed in meters per second
    :param speed: float, speed value
    :param unit: str, speed unit
    :return: float, speed in meters per second
    """
    if unit == SPEED_MS:
        return speed
    elif unit == SPEED_KMH:
        return speed * 10 / 36
    elif unit == SPEED_KT:
        return speed * 1852 / 3600


def speed_ms_to_unit(speed_ms, unit):
    """ Convert speed from meters per second to given speed unit.
    :param speed_ms: flat, speed in meters per second
    :param unit: str, speed unit
    :return: float, speed in given unit
    """
    if unit == SPEED_MS:
        return speed_ms
    elif unit == SPEED_KMH:
        return speed_ms * 36 / 10
    elif unit == SPEED_KT:
        return speed_ms * 3600 / 1852


def convert_speed(speed, from_unit, to_unit):
    """ Convert speed from one unit to another one.
    :param speed: float, speed in speed unit defined by form_unit
    :param from_unit: str, speed unit
    :param to_unit: str, speed unit
    :return: float, converted speed in speed unit defined by to_unit
    """
    speed_ms = speed_to_ms(speed, from_unit)
    if speed_ms is not None:
        return speed_ms_to_unit(speed_ms, to_unit)
