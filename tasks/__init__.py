# _*_ coding: utf-8 _*_

"""
tasks module
"""

import logging
from typing import Optional

from celery import Celery
from kombu import Queue

from core import settings

# define broker and backend
broker = f"{settings.REDIS_URI}/{10 if not settings.DEBUG else 12}"
backend = f"{settings.REDIS_URI}/{11 if not settings.DEBUG else 13}"

# celery -A tasks flower -l INFO --port=5555
# celery -A tasks worker -l INFO --concurrency=4 --purge
app_celery = Celery(__name__, broker=broker, backend=backend, include=[])

# config of celery
app_celery.conf.broker_connection_retry_on_startup = True
app_celery.conf.task_default_queue = "default"
app_celery.conf.task_queues = (
    Queue("default", queue_arguments={"x-max-priority": 5}),
    Queue("low_priority", queue_arguments={"x-max-priority": 1}),
    Queue("high_priority", queue_arguments={"x-max-priority": 10}),
)


@app_celery.task(name="low_priority.add", bind=True, rate_limit="50/m", max_retries=3)
def test_add_1(self, x: int, y: int, z: Optional[int] = None):
    # task information
    request = self.request
    logging.warning("%s: %s, %s", request.id)
    logging.warning("%s: %s, %s", request.id, request.retries, request.delivery_info)
    logging.warning("%s: %s, %s", request.id, request.args, request.kwargs)

    # task process
    return x + y + (z or 0)


@app_celery.task(name="high_priority.add", bind=True, rate_limit="50/m", max_retries=3)
def test_add_2(self, x: int, y: int, z: Optional[int] = None):
    # task information
    request = self.request
    logging.warning("%s: %s, %s", request.id, request.retries, request.delivery_info)
    logging.warning("%s: %s, %s", request.id, request.args, request.kwargs)

    # task process
    return x + y + (z or 0)
