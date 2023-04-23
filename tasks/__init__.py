# _*_ coding: utf-8 _*_

"""
celery tasks module
"""

from celery import Celery

from core.settings import settings

# define broker and backend
broker = f"{settings.REDIS_URI}/11"
backend = f"{settings.REDIS_URI}/12"

# celery -A tasks worker -l INFO --purge
# celery -A tasks flower --port=5555 -l INFO
app_celery = Celery(
    __name__,
    broker=broker,
    backend=backend,
    accept_content=["json", ],
    task_serializer="json",
    result_serializer="json",
    include=[
        "pages.panalysis.ptasks",
    ],
)
