from es import add_book
from utils import delete_file


def do_task(task_data):
    """
    Add book to index task. Delete file after adding.

    :param task_data: contain path to file
    :type task_data: dict
    :return: result of book addition
    :rtype: dict
    """

    path = task_data['path']
    result = add_book(path)

    delete_file(path)
    return result
