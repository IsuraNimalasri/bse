import logging

from retask import Queue

from configs import (TASK_QUEUE_CONNECTION, TASK_QUEUE_LOG,
                     LOG_FILENAME, LOG_FORMAT)


def log_task(task_data):
    logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, level=logging.INFO)

    msg = 'email:' + task_data['email'] + '; '\
        + 'q:' + task_data['q'] + '; '\
        + 'took:' + str(task_data['took'])

    logging.info(msg)


def get_task():
    queue = Queue(TASK_QUEUE_LOG, config=TASK_QUEUE_CONNECTION)
    queue.connect()
    while queue.length != 0:
        task = queue.dequeue()
        # task = queue.wait()
        if task:
            log_task(task.data)


if __name__ == '__main__':
    get_task()
