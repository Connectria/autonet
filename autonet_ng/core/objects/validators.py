import ipaddress
import typing

from autonet_ng.core.exceptions import RequestTypeError


def is_uint16(number: str) -> bool:
    """
    Verify that the provided string is a 16bit unsigned integer.
    :param number: An unsigned 16bit integers, as a string.
    """
    try:
        return 0 <= int(number) <= 65535
    except ValueError:
        pass
    return False


def is_uint32(number: str) -> bool:
    """
    Verify that the provided string is a 32bit unsigned integer.
    :param number: An unsigned 32bit integer, as a string
    :return:
    """
    try:
        return 0 <= int(number) <= 4294967295
    except ValueError:
        pass
    return False


def is_ipv4_address(address: str) -> bool:
    """
    Verify that string represents a valid IPv4 address.
    :param address: An IPv4 address string.
    """
    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        pass
    return False


def is_route_distinguisher(rd: str) -> bool:
    """
    Verifies that the provided string is a properly formatted route
    distinguisher.  Also accepts "auto" which is a special signal
    to an Autonet driver to derive the RD automatically using methods
    appropriate to the device.
    :param rd: Route distinguisher, as a string.
    :return:
    """
    if rd == 'auto':
        return True
    parts = rd.split(':')
    # There should be exactly two parts. First part can be an integer
    # or an IPv4 address.  The last part must be an integer.
    case1 = is_ipv4_address(parts[0]) and is_uint16(parts[1])
    case2 = is_uint32(parts[0]) and is_uint16(parts[1])
    case3 = is_uint16(parts[0]) and is_uint32(parts[1])
    return len(parts) == 2 and (case1 or case2 or case3)


def is_route_target(rt: str, allow_auto: bool = True) -> bool:
    """
    Verifies that the provided string is a valid route target.  Also
    accepts "auto" which is a special signal to an Autonet driver to
    derive the RT automatically as appropriate for the device.
    :param rt: A route target string
    :param allow_auto: Allow the special value `auto`.
    :return:
    """
    if allow_auto and rt == 'auto':
        return True

    parts = rt.split(':')
    # There should be exactly 2 parts, both of which are integers.
    if len(parts) != 2:
        return False
    case1 = is_uint16(parts[0]) and is_uint32(parts[1])
    case2 = is_uint32(parts[0]) and is_uint16(parts[1])
    return case1 or case2


def validate_union(value, tp):
    """
    Determines if the value is one of the possible inner types of a Union Type.
    :param value: The value to be validated.
    :param tp: The Union type to validate against.
    """
    for t in typing.get_args(tp):
        if typing.get_origin(t) is list:
            return validate_list(value, t)
        if isinstance(value, t):
            return True
    return False


def validate_list(value, tp):
    """
    Determines if the values inside a list are of the proper inner
    type.  This function takes the outer list type hint as defined and
    will determine the proper inner type to validate against.
    :param value: The list to be validated.
    :param tp: The list type to validate against.
    """
    inner_tp = typing.get_args(tp)
    for v in value:
        if not isinstance(v, inner_tp):
            return False
    return True


def validate(obj: object):
    for attr, tp in typing.get_type_hints(obj).items():
        value = getattr(obj, attr)

        if typing.get_origin(tp) is typing.Union:
            if not validate_union(value, tp):
                raise RequestTypeError(attr, value, tp, valid_types=typing.get_args(tp))
        elif typing.get_origin(tp) is list:
            if not validate_list(value, tp):
                raise RequestTypeError(attr, value, tp, valid_types=typing.get_args(tp))
        elif not isinstance(value, tp):
            raise RequestTypeError(attr, value, tp)
    return True
