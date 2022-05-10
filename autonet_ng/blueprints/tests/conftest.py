import pytest


@pytest.fixture
def test_admin1():
    return {
        'username': 'testadmin1',
        'description': 'Test Admin 1',
        'email': 'testadmin1@localhost'
    }


@pytest.fixture
def test_admin2():
    return {
        'username': 'testadmin2',
        'description': 'Test Admin 2',
        'email': 'testadmin2@localhost'
    }


@pytest.fixture
def test_admin3():
    return {
        'username': 'testadmin3',
        'description': 'Test Admin 3',
        'email': 'testadmin31@localhost'
    }
