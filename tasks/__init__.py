# _*_ coding: utf-8 _*_

"""
tasks module
"""

from celery import Celery

from core.settings import settings

# define broker and backend
broker = f"{settings.REDIS_URI}/{10 if not settings.DEBUG else 12}"
backend = f"{settings.REDIS_URI}/{11 if not settings.DEBUG else 13}"

# celery -A tasks worker -l INFO --purge
# celery -A tasks flower --port=5555 -l INFO
app_celery = Celery(__name__, broker=broker, backend=backend, include=[
    "pages.panalysis.ptasks",
])


@app_celery.task(name="tasks.add")
def add(x, y): return x + y
