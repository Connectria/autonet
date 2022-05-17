import pytest

from autonet_ng.core.objects import validators as v


@pytest.mark.parametrize('number, expected', [
    ('3.1415', False),
    ('3000', True),
    ('abc1234', False)
])
def test_is_uint16(number, expected):
    assert v.is_uint16(number) == expected


@pytest.mark.parametrize('address, expected', [
    ('ip_address', False),
    ('192.168.4.4', True),
    ('198.19.198.18/32', False),
    (21559259592, False)
])
def test_is_ipv4_address(address, expected):
    assert v.is_ipv4_address(address) == expected


@pytest.mark.parametrize('rd, expected', [
    ('198.18.0.1:65', True),
    ('65531:65531', True),
    ('rd:distingisher', False),
    ('515555:82', False)
])
def test_is_route_distinguisher(rd, expected):
    assert v.is_route_distinguisher(rd) == expected


@pytest.mark.parametrize('rt, expected', [
    ('198.18.0.1:65', False),
    ('65531:65531', True),
    ('route:target', False),
    ('515555:82', False)
])
def test_is_route_target(rt, expected):
    assert v.is_route_target(rt) == expected
