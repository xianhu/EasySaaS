# _*_ coding: utf-8 _*_

"""
tasks module
"""

from celery import Celery

from core.settings import settings

# celery -A tasks worker -l INFO --purge
# celery -A tasks flower --port=5555 -l INFO
app_celery = Celery(
    __name__,
    broker=f"{settings.REDIS_URI}/11",
    backend=f"{settings.REDIS_URI}/12",
    accept_content=["json", ],
    task_serializer="json",
    result_serializer="json",
    include=[
        "pages.panalysis.ptasks",
    ],
)


@app_celery.task(name="tasks.add")
def add(x, y): return x + y
