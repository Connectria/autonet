import typing

from autonet_ng.core.exceptions import RequestTypeError


def validate_union(value, tp):
    """
    Determines if the value is one of the possible inner types of a Union Type.
    :param value: The value to be validated.
    :param tp: The Union type to validate against.
    """
    for t in typing.get_args(tp):
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
