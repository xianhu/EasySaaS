# _*_ coding: utf-8 _*_

"""
tasks module
"""

import logging
import random
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


@app_celery.task(name="add_1", bind=True, rate_limit="50/m",
                 max_retries=3, autoretry_for=(Exception,), countdown=5)
def test_add_1(self, x: int, y: int, z: Optional[int] = None):
    # task information
    request = self.request
    logging.warning("(1)%s: %s, %s", request.id, request.args, request.kwargs)
    logging.warning("(1)%s: %s, %s", request.id, request.retries, request.delivery_info)
    # task operation: self.update_state(), self.retry(), etc

    # simulate task failure
    if not random.randint(0, 10):
        raise Exception("simulate task failure")

    # task process
    return x + y + (z or 0)


@app_celery.task(name="add_2", bind=True, rate_limit="50/m",
                 max_retries=3, autoretry_for=(Exception,), countdown=5)
def test_add_2(self, x: int, y: int, z: Optional[int] = None):
    # task information
    request = self.request
    logging.warning("(2)%s: %s, %s", request.id, request.args, request.kwargs)
    logging.warning("(2)%s: %s, %s", request.id, request.retries, request.delivery_info)
    # task operation: self.update_state(), self.retry(), etc

    # simulate task failure
    if not random.randint(0, 10):
        raise Exception("simulate task failure")

    # task process
    return x + y + (z or 0)
