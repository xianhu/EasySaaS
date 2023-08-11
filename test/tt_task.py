# _*_ coding: utf-8 _*_

"""
test tasks
"""

import logging
import time

from celery.result import AsyncResult

from tasks import test_add_1, test_add_2

# define tasks
task_list = []
task_id_list = []
for i in range(100):
    if i % 3 == 0:
        task = test_add_1.apply_async(args=(i, i), kwargs={"z": i}, queue="default")
    elif i % 3 == 1:
        task = test_add_1.apply_async(args=(i, i), kwargs={"z": i}, queue="low_priority")
    else:
        task = test_add_2.apply_async(args=(i, i), kwargs={"z": i}, queue="high_priority")
    task_list.append(task)
    task_id_list.append(task.id)

while True:
    # read tasks
    logging.warning("=======" * 10)
    for index, task_id in enumerate(task_id_list):
        task = AsyncResult(task_id)  # task_list[index]
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
