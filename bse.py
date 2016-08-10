import json
import re

from retask import Task
from retask import Queue

import falcon


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class BSEResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = 'text/html'
        with open('./templates/base.html', 'r') as f:
            html_template = f.read()
        with open('./static/js/bse.js', 'r') as f:
            js_script = f.read()
        html_template = html_template.replace("<script></script>", "<script>" + js_script + "</script>")
        resp.body = html_template

    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            raw_json = req.stream.read().decode("utf-8")
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.args)

        try:
            result_json = json.loads(raw_json, encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')

        # inner request object
        reqo = {}
        for item in result_json:
            reqo[item['name']] = item['value']

        email = reqo['email']

        # inner response object
        reso = {}
        if not validate_email(email):
            reso['is_e'] = True
            reso['e'] = 'Email ' + email + ' is invalid.'
        else:
            reso['is_e'] = False
            reso['username'] = extract_username(email)
            reso['email'] = email

            enqueue_task(reqo)

        resp.body = json.dumps(reso)
        resp.status = falcon.HTTP_200


def enqueue_task(task_data):

    config = {
        'host': '192.168.0.29',
        'port': 6379,
        'db': 0,
        'password': None,
    }

    queue = Queue('search', config=config)
    queue.connect()
    task = Task(task_data)
    queue.enqueue(task)


def validate_email(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                     email)
    if match:
        return True
    return False


def extract_username(email):
    return email[:email.index('@')]


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
bse = BSEResource()

# things will handle all requests to the '/things' URL path
app.add_route('/', bse)
