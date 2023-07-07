# _*_ coding: utf-8 _*_

"""
test task
"""

import logging
import time

from tasks import test_add

task_list = []
for i in range(300):
    task = test_add.apply_async((i, i), countdown=1)
    task_list.append(task)

while True:
    logging.warning("=======" * 10)
    for task in task_list:
        # task.ready(), task.get()
        if task.status == "FAILURE":
            logging.warning(task.id, task.status, task.traceback)
            continue
        if task.status == "SUCCESS":
            logging.warning(task.id, task.status, task.result)
            continue
        # PENDING, STARTED, RETRY, REVOKED
        logging.warning(task.id, task.status)
    time.sleep(5)
