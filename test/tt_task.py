# _*_ coding: utf-8 _*_

"""
test tasks
"""

import logging
import time

from celery.result import AsyncResult

from tasks import test_add_func

# define tasks
task_list = []
task_id_list = []
for i in range(100):
    queue = "default" if i % 3 == 0 else "low_priority" if i % 3 == 1 else "high_priority"
    task = test_add_func.apply_async(args=(i, i), kwargs={"z": i}, queue=queue)

    # append task
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
