import pytest

from autonet.core import exceptions as exc
from autonet.core.objects import interfaces as an_if


@pytest.mark.parametrize('test_kwargs, expected, raises', [
    (
            {
                'address': '198.18.0.1/32'
            },
            {
                'address': '198.18.0.1/32',
                'family': 'ipv4',
                'virtual': False,
                'virtual_type': None
            },
            None
    ),
    (
            {
                'address': '2001:db8:a:b::1/64'
            },
            {
                'address': '2001:db8:a:b::1/64',
                'family': 'ipv6',
                'virtual': False,
                'virtual_type': None
            },
            None
    ),
    (
            {
                'address': '198.18.0.1/32',
                'family': 'ipv6'
            },
            None,
            exc.RequestValueError
    ),
    (
            {
                'address': 'a.b.c.d/22',
            },
            None,
            ValueError
    ),
    (
            {
                'address': '198.18.0.1/32',
                'virtual': True,
                'virtual_type': 'hsrp_v5'
            },
            None,
            exc.RequestValueError
    )
])
def test_interface_address(test_kwargs, expected, raises):
    if raises:
        with pytest.raises(raises):
            an_if.InterfaceAddress(**test_kwargs)
    else:
        interface = an_if.InterfaceAddress(**test_kwargs)
        for key, value in expected.items():
            assert getattr(interface, key) == value
