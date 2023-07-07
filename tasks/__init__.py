# _*_ coding: utf-8 _*_

"""
tasks module
"""

import logging

from celery import Celery

from core.settings import settings

# define broker and backend
broker = f"{settings.REDIS_URI}/{10 if not settings.DEBUG else 12}"
backend = f"{settings.REDIS_URI}/{11 if not settings.DEBUG else 13}"

# celery -A tasks flower -l INFO --port=5555
# celery -A tasks worker -l INFO --concurrency=4 --purge
app_celery = Celery(__name__, broker=broker, backend=backend, include=[
    # "pages.panalysis.ptasks",
])


@app_celery.task(bind=True, rate_limit="50/m")
def test_add(self, x, y):
    # task information
    request = self.request
    logging.warning("%s: %s, %s, %s", request.id, request.retries, request.delivery_info)
    logging.warning("%s: %s, %s, %s", request.id, request.args, request.kwargs)

    # task process
    return x + y
