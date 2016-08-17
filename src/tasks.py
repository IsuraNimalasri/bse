from celery import Celery

from search_task import do_task as do_search_task
from log_task import do_task as do_log_task
from add_book_task import do_task as do_add_book_task


app = Celery('tasks', broker='amqp://guest@RABBIT//')


@app.task
def search_task(task_data):
    log_task_data = do_search_task(task_data)
    log_task.delay(log_task_data)


@app.task
def log_task(task_data):
    do_log_task(task_data)


@app.task
def add_book_task(task_data):
    do_add_book_task(task_data)
