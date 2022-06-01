import pytest

from autonet.blueprints import bridge_vlan


@pytest.mark.parametrize('request_data, expected', [
    (
            {'admin_enabled': True, 'bridge_domain': None, 'id': 2000, 'name': 'testvlan'},
            {'admin_enabled': True, 'bridge_domain': None, 'id': 2000, 'name': 'testvlan'},
    ),
    (
            {'admin_enabled': None, 'bridge_domain': None, 'id': 2000, 'name': 'testvlan'},
            {'admin_enabled': True, 'bridge_domain': None, 'id': 2000, 'name': 'testvlan'},
    ),
    (
            {'admin_enabled': False, 'bridge_domain': None, 'id': 2000, 'name': 'testvlan'},
            {'admin_enabled': False, 'bridge_domain': None, 'id': 2000, 'name': 'testvlan'},
    )
])
def test_prepare_defaults(request_data, expected):
    assert bridge_vlan._prepare_defaults(request_data) == expected

