import os
import random

import pytest
import requests
from faker import Faker

from jsonschema import validate

from json_schemas.user_schemas import post_user, get_user, put_user

faker = Faker("ru_RU")
url = "https://reqres.in"
endpoint = "/api/users/"
user_id = "2"


def test_post_user_positive():
    response = requests.post(url + endpoint, data={"name": f"{faker.name()}", "job": f"{faker.job()}"})

    assert response.status_code == 201
    validate(response.json(), post_user)


@pytest.mark.parametrize("name, job", [
    (faker.name(), None),
    (None, faker.job())
])
def test_post_user_negative(name, job):
    response = requests.post(url + endpoint, data={"name": name, "job": job})

    assert response.status_code == 400


def test_get_user_positive():
    response = requests.get(url + endpoint + user_id)

    assert response.status_code == 200
    validate(response.json(), get_user)


def test_get_user_negative():
    response = requests.get(url + endpoint + "88")

    assert response.status_code == 404


def test_put_user_info():
    response = requests.put(url + endpoint + user_id, data={"name": f"{faker.name()}", "job": f"{faker.job()}"})

    assert response.status_code == 200
    body = response.json()
    validate(body, put_user)


def test_delete_user_info():
    response = requests.delete(url + endpoint + user_id)
    assert response.status_code == 204
