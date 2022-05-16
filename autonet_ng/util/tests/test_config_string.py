import pytest

from autonet_ng.util import config_string as cs


@pytest.mark.parametrize('vlans, expected', [
    ([1, 2, 3, 6, 7, 8, 9, 11], '1-3,6-9,11'),
    ([100], '100'),
    ([100, 101], '100-101'),
    ([100, 101, 103, 105, 200, 201, 202, 203, 204, 205, 206, 210],
     '100-101,103,105,200-206,210')
])
def test_vlan_list_to_glob(vlans, expected):
    assert cs.vlan_list_to_glob(vlans) == expected


@pytest.mark.parametrize('glob, expected', [
    ('1-3,6-8,9,11', [1, 2, 3, 6, 7, 8, 9, 11]),
    ('100', [100]),
    ('100-101', [100, 101]),
    ('100-101,103,105,200-206,210',
     [100, 101, 103, 105, 200, 201, 202, 203, 204, 205, 206, 210])
])
def test_glob_to_vlan_list(glob, expected):
    assert cs.glob_to_vlan_list(glob) == expected
