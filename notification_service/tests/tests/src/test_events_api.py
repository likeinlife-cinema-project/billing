from http import HTTPStatus
from uuid import uuid4
import time

import httpx

from tests.payloads import VALID_PAYLOAD, MISSING_TEMPLATE_PAYLOAD, WRONG_PARAMS_PAYLOAD
from tests.settings import settings


def test_valid_event(api_client: httpx.Client, setup_database):
    event_response = api_client.post(
        settings.register_event_endpoint, json=VALID_PAYLOAD
    )
    assert event_response.status_code == HTTPStatus.CREATED
    time.sleep(1)
    event_status_url = (
        f"{settings.register_event_endpoint}{event_response.json()['id']}/"
    )
    status_response = api_client.get(event_status_url)
    assert status_response.status_code == HTTPStatus.OK


def test_event_with_wrong_params(api_client: httpx.Client):
    response = api_client.post(
        settings.register_event_endpoint, json=WRONG_PARAMS_PAYLOAD
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_event_missing_template(api_client: httpx.Client):
    response = api_client.post(
        settings.register_event_endpoint, json=MISSING_TEMPLATE_PAYLOAD
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_missing_event_status(api_client: httpx.Client):
    event_status_url = f"{settings.register_event_endpoint}{uuid4()}/"
    status_response = api_client.get(event_status_url)
    assert status_response.status_code == HTTPStatus.NOT_FOUND
