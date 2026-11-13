import uuid

import pytest
from jsonschema import validate

import config
from tests.api import schemas

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_login_returns_token(api):
    resp = api.login(config.USER_EMAIL, config.USER_PASSWORD)

    assert resp.status_code == 200
    validate(resp.json(), schemas.TOKEN)
    assert resp.json()["token_type"].lower() == "bearer"


def test_login_unknown_user(api):
    resp = api.login(f"nobody_{uuid.uuid4().hex[:8]}@example.com", "welcome01")

    assert resp.status_code == 401
    assert resp.json()["error"] == "Unauthorized"


def test_me_with_token(api, token):
    resp = api.me(token)

    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == config.USER_EMAIL
    assert f'{body["first_name"]} {body["last_name"]}' == config.USER_FULL_NAME


@pytest.mark.parametrize("bad_token", ["", "abc", "Bearer.fake.token"])
def test_me_without_valid_token(api, bad_token):
    assert api.me(bad_token).status_code == 401
