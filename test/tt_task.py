# _*_ coding: utf-8 _*_

"""
test tasks
"""

import logging
import time

from tasks import test_add_1, test_add_2
from celery.result import AsyncResult

task_list = []
for i in range(300):
    queue = "high_priority" if i % 2 == 0 else "low_priority"
    if i % 2 == 0:
        task = test_add_1.apply_async(args=(i, i), kwargs={"z": i})
    else:
        task = test_add_2.apply_async(args=(i, i), kwargs={"z": i})
    # task = test_add.apply_async(args=(i, i), kwargs={"z": i}, queue=queue)
    task_list.append(task)

while True:
    logging.warning("=======" * 10)

    for task in task_list:
        # task.ready(), task.get()
        if task.status == "FAILURE":
            logging.warning("%s: %s, %s", task.id, task.status, task.traceback)
            continue
        if task.status == "SUCCESS":
            logging.warning("%s: %s, %s", task.id, task.status, task.result)
            continue
        # PENDING, RECEIVED, STARTED, RETRY, REVOKED
        logging.warning("%s: %s", task.id, task.status)
    time.sleep(5)
