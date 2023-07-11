# _*_ coding: utf-8 _*_

"""
test tasks
"""

import logging
import time

from tasks import test_add

task_list = []
for i in range(300):
    task = test_add.apply_async((i, i), kwargs={"z": i}, countdown=1)
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
        # PENDING, STARTED, RETRY, REVOKED
        logging.warning("%s: %s", task.id, task.status)
    time.sleep(5)
