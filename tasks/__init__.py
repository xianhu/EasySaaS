# _*_ coding: utf-8 _*_

"""
celery tasks module
"""

from celery import Celery

from config import CONFIG_REDIS_URI

# define broker and backend
broker = f"{CONFIG_REDIS_URI}/11"
backend = f"{CONFIG_REDIS_URI}/12"

# celery -A tasks worker -l INFO --purge
# celery -A tasks flower --port=5555 -l INFO
app_celery = Celery(
    __name__,
    broker=broker,
    backend=backend,
    include=[
        "pages.panalysis.ptasks",
    ],
)


@app_celery.task(name="test", serializer="json")
def test(param1, param2):
    """
    test task
    """
    return True
