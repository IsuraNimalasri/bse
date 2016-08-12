import logging

from configs import (LOG_FILENAME, LOG_FORMAT)


def log_task(task_data):
    logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, level=logging.INFO)

    msg = 'email:' + task_data['email'] + '; '\
        + 'q:' + task_data['q'] + '; '\
        + 'took:' + str(task_data['took'])

    logging.info(msg)


def do_task(task_data):
    log_task(task_data)
