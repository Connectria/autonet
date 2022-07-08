import pytest

from autonet.util import evpn


@pytest.mark.parametrize('test_esi, expected', [
    ('00:aa:0b:21:dd:a8:fe:00:00:01', {
        'type': 0,
        'id': 'aa:0b:21:dd:a8:fe:00:00:01'
    }),
    ('01:aa:0b:21:dd:a8:fe:00:80:00', {
        'type': 1,
        'lacp_system_mac': 'aa:0b:21:dd:a8:fe',
        'lacp_port_key': 128
    }),
    ('02:aa:0b:21:dd:a8:fe:20:00:00', {
        'type': 2,
        'root_bridge': 'aa:0b:21:dd:a8:fe',
        'root_priority': 8192
    }),
    ('03:aa:0b:21:dd:a8:fe:00:00:00', {
        'type': 3,
        'system_mac': 'aa:0b:21:dd:a8:fe',
        'local_discriminator': 0
    }),
    ('04:c6:12:10:0a:00:00:00:ff:00', {
        'type': 4,
        'router_id': '198.18.16.10',
        'local_discriminator': 255,
    }),
    ('05:00:00:ff:dc:00:00:10:00:00', {
        'type': 5,
        'asn': 65500,
        'local_discriminator': 4096,
    }),
])
def test_parse_esi(test_esi, expected):
    assert evpn.parse_esi(test_esi) == expected
