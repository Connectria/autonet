import os
import pytest


@pytest.fixture
def test_yamlfile_path():
    cwd = os.path.dirname(os.path.abspath(__file__))
    return f'{cwd}/test_inventory.yml'
