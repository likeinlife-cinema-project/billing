import logging

from billing.celery import app

logger = logging.getLogger(__name__)


@app.task
def test_billing_task():
    logger.debug("Start test task")
    logger.debug("End test task")
