import typing

from core.exceptions import RequestTypeError


def validate_union(value, tp):
    for t in typing.get_args(tp):
        if isinstance(value, t):
            return True
    return False


def validate(obj: object):
    for attr, tp in typing.get_type_hints(obj):
        value = getattr(obj, attr)

        if typing.get_origin(tp) is typing.Union \
                and not validate_union(value, tp):
            raise RequestTypeError(attr, value, tp, valid_types=typing.get_args(tp))

        if not isinstance(value, tp):
            raise RequestTypeError(attr, value, tp)
    return True
