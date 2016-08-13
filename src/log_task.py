import logging

from configs import (LOG_PATH, LOG_FILENAME, LOG_FORMAT)


def log_task(task_data):
    log_formatter = logging.Formatter(LOG_FORMAT)
    log = logging.getLogger()

    file_handler = logging.FileHandler("{0}/{1}.log".format(LOG_PATH, LOG_FILENAME))
    file_handler.setFormatter(log_formatter)
    log.addHandler(file_handler)

    msg = 'email:' + task_data['email'] + '; '\
        + 'q:' + task_data['q'] + '; '\
        + 'took:' + str(task_data['took'])

    log.info(msg)


def do_task(task_data):
    log_task(task_data)
