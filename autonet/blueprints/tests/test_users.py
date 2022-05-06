import string


def compare_user_object(first, other):
    compare_values = ['username', 'email', 'description']
    for cv in compare_values:
        if first[cv] != other[cv]:
            return False
    return True


def verify_response(response, expected_status: int = 200,
                    expected_errors: list = None) -> None:
    expected_errors = expected_errors or []
    assert response.status_code == response.json['status'] == expected_status
    assert response.json['errors'] == expected_errors


def test_create_user(client, db_session, test_auth_header, test_admin3):
    response = client.post('/admin/users', json=test_admin3, headers=test_auth_header)
    assert isinstance(response.json['data'], dict)
    assert compare_user_object(response.json['data'], test_admin3)
    assert response.json['data']['tokens'] == []
    verify_response(response, 201)


def test_create_duplicate_user(client, db_session, test_auth_header, test_admin1):
    response = client.post('/admin/users', json=test_admin1, headers=test_auth_header)
    assert response.json['data'] is None
    verify_response(response, 409)


def test_get_users(client, db_session, test_auth_header, test_admin1, test_admin2):
    response = client.get('/admin/users', headers=test_auth_header)
    assert isinstance(response.json['data'], list)
    assert len(response.json['data']) == 3
    verify_response(response)
    found = {'testadmin1': False, 'testadmin2': False}
    for user_object in response.json['data']:
        if compare_user_object(test_admin1, user_object):
            found['testadmin1'] = True
        if compare_user_object(test_admin2, user_object):
            found['testadmin2'] = True
    for _, v in found.items():
        assert v


def test_get_user(client, db_session, test_auth_header, test_admin2):
    user_id = '2a575546-b5d1-44f0-a485-301305ff1be4'
    response = client.get(f'/admin/users/{user_id}', headers=test_auth_header)
    assert isinstance(response.json['data'], dict)
    assert compare_user_object(response.json['data'], test_admin2)
    verify_response(response)


def test_get_invalid_user(client, db_session, test_auth_header, test_admin2):
    user_id = '2a575546-b5d1-44f0-a485-301305ff1be5'
    response = client.get(f'/admin/users/{user_id}', headers=test_auth_header)
    assert response.json['data'] is None
    verify_response(response, 404)


def test_update_user(client, db_session, test_auth_header, test_admin2):
    user_id = '2a575546-b5d1-44f0-a485-301305ff1be4'
    updated_email = 'updated@localhost'
    updated_user_object = {**test_admin2, **{'email': updated_email}}
    response = client.patch(f'/admin/users/{user_id}',
                            json=updated_user_object, headers=test_auth_header)
    assert isinstance(response.json['data'], dict)
    assert compare_user_object(response.json['data'], updated_user_object)
    verify_response(response, 200)


def test_update_invalid_user(client, db_session, test_auth_header, test_admin2):
    user_id = '3a575546-b5d1-44f0-a485-301305ff1be4'
    updated_email = 'invaliduser@localhost'
    updated_user_object = {**test_admin2, **{'email': updated_email}}
    response = client.patch(f'/admin/users/{user_id}',
                            json=updated_user_object, headers=test_auth_header)
    assert response.json['data'] is None
    assert response.json['status'] == response.status_code == 404


def test_delete_user(client, db_session, test_auth_header):
    user_id = '2a575546-b5d1-44f0-a485-301305ff1be4'
    response = client.delete(f'/admin/users/{user_id}', headers=test_auth_header)
    assert not response.data
    assert response.status_code == 204


def test_delete_invalid_user(client, db_session, test_auth_header):
    user_id = '3a575546-b5d1-44f0-a485-301305ff1be4'
    response = client.delete(f'/admin/users/{user_id}', headers=test_auth_header)
    assert response.json['data'] is None
    assert response.json['status'] == response.status_code == 404


def test_get_user_tokens(client, db_session, test_auth_header):
    user_id = '5d76f0bc-1687-4ed2-b6c6-7c879d6db4b6'
    response = client.get(f'/admin/users/{user_id}/tokens', headers=test_auth_header)
    assert isinstance(response.json['data'], list)
    assert len(response.json['data']) == 1
    token = response.json['data'][0]
    assert token['id'] == '71297e83-a230-4209-98a1-27f30b5299ef'
    assert token['user_id'] == user_id


def test_create_user_token(client, db_session, test_auth_header):
    user_id = '2a575546-b5d1-44f0-a485-301305ff1be4'
    response = client.post(f'/admin/users/{user_id}/tokens', headers=test_auth_header)
    assert not response.json['data']
    assert 'X-API-Key' in response.headers
    token = response.headers.get('X-API-Key')
    assert len(token) == 32
    assert all(c in string.hexdigits for c in token)


def test_create_token_for_invalid_user(client, db_session, test_auth_header):
    user_id = '3a575546-b5d1-44f0-a485-301305ff1be4'
    response = client.post(f'/admin/users/{user_id}/tokens', headers=test_auth_header)
    assert response.status_code == 404
    assert ['X-API-Key'] not in response.headers


def test_delete_user_token(client, db_session, test_auth_header):
    user_id = '2a575546-b5d1-44f0-a485-301305ff1be4'
    token_id = '5cd88f51-79ab-43e8-afc5-626743e9220b'
    response = client.delete(f'/admin/users/{user_id}/tokens/{token_id}', headers=test_auth_header)
    assert not response.data
    assert response.status_code == 204


def test_delete_invalid_user_token(client, db_session, test_auth_header):
    user_id = '3a575546-b5d1-44f0-a485-301305ff1be4'
    token_id = '5cd88f51-79ab-43e8-afc5-626743e9220b'
    response = client.delete(f'/admin/users/{user_id}/tokens/{token_id}', headers=test_auth_header)
    assert response.json['data'] is None
    assert response.json['status'] == response.status_code == 404


def test_delete_user_invalid_token(client, db_session, test_auth_header):
    user_id = '2a575546-b5d1-44f0-a485-301305ff1be4'
    token_id = '6cd88f51-79ab-43e8-afc5-626743e9220b'
    response = client.delete(f'/admin/users/{user_id}/tokens/{token_id}', headers=test_auth_header)
    assert response.json['data'] is None
    assert response.json['status'] == response.status_code == 404
