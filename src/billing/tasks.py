import json

import requests
import structlog
from redis import Redis

from billing.config import settings_mock
from config.celery import app

logger = structlog.getLogger(__name__)


@app.task
def mock_send_notification(key: str, type_: str):
    redis = Redis(host=settings_mock.redis_host, port=settings_mock.redis_port, db=1, decode_responses=True)
    object_ = json.loads(redis.get(key))
    data = {"event": type_, "object": object_}
    response = requests.post(
        # TODO: remove hard-coded base link
        "http://billing-service:8000/payments/notification/",
        json=data,
        headers={"Content-type": "application/json"},
        timeout=10,
    )
    logger.debug(response.json())
