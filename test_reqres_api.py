import pytest
import requests
import jsonschema
from utils import load_schema


def test_get_list_users():
    url = 'https://reqres.in/api/users?page=2'
    result = requests.get(url)
    schema = load_schema('json_schemas/list_users_schema.json')

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_post_create_user():
    name = 'Alex'
    job = 'Artist'
    url = 'https://reqres.in/api/users'
    result = requests.post(url, json={'name': f"{name}", 'job': f"{job}"})
    schema = load_schema('json_schemas/create_user_schema.json')

    assert result.status_code == 201
    assert result.json()['name'] == name
    assert result.json()['job'] == job
    jsonschema.validate(result.json(), schema)


def test_put_update_user():
    name = 'new_name'
    job = 'new_job'
    url = 'https://reqres.in/api/users/2'
    result = requests.put(url, json={'name': f"{name}", 'job': f"{job}"})
    schema = load_schema('json_schemas/update_user_schema.json')

    assert result.status_code == 200
    assert result.json()['name'] == name
    assert result.json()['job'] == job
    jsonschema.validate(result.json(), schema)


def test_delete_user():
    url = 'https://reqres.in/api/users/2'
    result = requests.delete(url)

    assert result.status_code == 204
    assert result.text == ''


def test_get_single_user_not_found():
    url = 'https://reqres.in/api/users/100500'
    result = requests.get(url)

    assert result.status_code == 404
    assert result.text == '{}'


def test_post_register_successful():
    url = 'https://reqres.in/api/register'
    result = requests.post(url, json={'email': "eve.holt@reqres.in", 'password': "pistol"})
    schema = load_schema('json_schemas/register_success_schema.json')

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_post_register_invaliv_email():
    url = 'https://reqres.in/api/register'
    result = requests.post(url, json={'email': "vasya@example.com", 'password': "qwerty"})

    assert result.status_code == 400
    assert result.json()['error'] == 'Note: Only defined users succeed registration'


def test_post_register_unsuccessful():
    url = 'https://reqres.in/api/register'
    result = requests.post(url, json={'email': "vasya@example.com"})

    assert result.status_code == 400
    assert result.text == '{"error":"Missing password"}'

@pytest.mark.parametrize('id_', [1, 2, 3])
def test_get_single_resource_id(id_):
    url = f'https://reqres.in/api/unknown/{id_}'
    result = requests.get(url)

    assert result.json()['data']['id'] == id_