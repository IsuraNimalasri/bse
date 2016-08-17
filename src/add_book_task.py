from es import add_book
from utils import delete_file


def do_task(task_data):

    path = task_data['path']
    results = add_book(path)
    print(results)
    delete_file(path)
    return results
