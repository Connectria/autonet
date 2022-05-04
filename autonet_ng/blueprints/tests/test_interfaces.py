def test_get_interfaces(client, test_auth_header):
    response = client.post('/0/interfaces', headers=test_auth_header)
    assert response

