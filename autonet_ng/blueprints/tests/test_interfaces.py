import pytest

from autonet_ng.blueprints import interface as if_bp
from autonet_ng.core import exceptions as exc
from autonet_ng.core.objects import interfaces as an_if


@pytest.mark.parametrize('test_request_name, test_interface_name, expected', [
    ('Ethernet7', 'Ethernet7', True),
    (None, 'Ethernet7', True),
    ('Ethernet7', 'Ethernet8', False)
])
def test_verify_name_match(test_request_name, test_interface_name, expected):
    result = if_bp._verify_name_match(test_request_name, test_interface_name)
    assert result == expected


@pytest.mark.parametrize('test_request_data, update, expected', [
    ({'name': 'testname', 'attributes': {}, 'mode': 'routed'},
     False, False),
    ({'name': 'testname'},
     True, False),
    ({'name': 'testname', 'mode': 'routed'},
     False, 'attributes'),
])
def test_verify_required_config_data(test_request_data, update, expected):
    result = if_bp._required_config_data_missing(test_request_data, update)
    assert result == expected


@pytest.mark.parametrize('test_request_data, expected', [
    ({'admin_enabled': False, 'mtu': 9000}, {'admin_enabled': False, 'mtu': 9000}),
    ({}, {'admin_enabled': True, 'mtu': 1500})
])
def test_prepare_defaults(test_request_data, expected):
    result = if_bp._prepare_defaults(test_request_data)
    assert result == expected



@pytest.mark.parametrize('test_request_data, expected', [
    ({
        'admin_enabled': True,
        'attributes': {
            'addresses': [
                {
                    'address': '198.18.22.22/32',
                    'family': 'ipv4',
                    'virtual': False,
                    'virtual_type': None
                }
            ],
            'vrf': None
        },
        'mode': 'routed',
        'name': 'Loopback51'
    },
     an_if.Interface(
         name='Loopback51',
         mode='routed',
         description=None,
         virtual=None,
         attributes=an_if.InterfaceRouteAttributes(
             addresses=[
                 an_if.InterfaceAddress(
                     family='ipv4',
                     address='198.18.22.22/32',
                     virtual=False,
                     virtual_type=None
                 )
             ],
             vrf=None
         ),
         admin_enabled=True,
         physical_address=None,
         child=False,
         parent=None,
         speed=None,
         duplex=None,
         mtu=None
     )
    )
])
def test_build_interface_from_request_data(test_request_data, expected):
    interface = if_bp._build_interface_from_request_data(test_request_data)
    assert interface == expected