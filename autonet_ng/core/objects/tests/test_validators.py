import pytest

from autonet_ng.core.objects import validators as v


@pytest.mark.parametrize('number, expected', [
    ('3.1415', False),
    ('3000', True),
    ('abc1234', False),
    ('65537', False),
    ('-100', False)
])
def test_is_uint16(number, expected):
    assert v.is_uint16(number) == expected


@pytest.mark.parametrize('number, expected', [
    ('3.1415', False),
    ('3000', True),
    ('abc1234', False),
    ('429000000', True),
    ('-100', False),
    ('4294967297', False)
])
def test_is_uint32(number, expected):
    assert v.is_uint32(number) == expected


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
    ('515555:82', True)
])
def test_is_route_distinguisher(rd, expected):
    assert v.is_route_distinguisher(rd) == expected


@pytest.mark.parametrize('rt, allow_auto, expected', [
    ('198.18.0.1:65', True, False),
    ('65531:65531', False, True),
    ('route:target', True, False),
    ('515555:82', False, True),
    ('82:515555', True, True),
    ('515555:515555', False, False),
    ('auto', True, True),
    ('auto', False, False)
])
def test_is_route_target(rt, allow_auto, expected):
    assert v.is_route_target(rt, allow_auto) == expected


@pytest.mark.parametrize('test_esi, expected', [
    ('no:t0:a0:va:li:d0:es:i0:00:00', False),
    ('00:01:22:ea:fb:99:ed:00:00:00', True),
    ('0001:22ea:fb99:ed00:0000', True),
    ('00_01_22_ea_fb_99_ed_00_00_00', True),
    ('00-01-22-ea-fb-99-ed-00-00-00', True),
    ('00.01.22.ea.fb.99.ed.00.00.00', True)
])
def test_is_esi(test_esi, expected):
    assert v.is_esi(test_esi) == expected
