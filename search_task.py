import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from elasticsearch import Elasticsearch

from retask import Task
from retask import Queue

from yattag import Doc

from es import search
from configs import (TASK_QUEUE_CONNECTION, TASK_QUEUE_SEARCH, TASK_QUEUE_LOG,
                     ELASTICSEARCH_HOSTS, ELASTICSEARCH_TIMEOUT,
                     EMAIL_LOGIN, EMAIL_PASS, EMAIL_SMTP_HOST, EMAIL_SMTP_PORT)


def format_result(result):
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('body'):
            with tag('p'):
                text('Hi!')
            with tag('p'):
                text('Here are your results:')

            with tag('ul'):
                for hit in result['hits']['hits']:
                    with tag('li'):
                        with tag('h2'):
                            if 'fields' in hit and 'file.title' in hit['fields'] and hit['fields']['file.title'][0]:
                                text(hit['fields']['file.title'][0])
                            else:
                                text(hit['fields']['file.name'][0])
                        with tag('ol'):
                            for r in hit['highlight']['file.content']:
                                with tag('li'):
                                    doc.asis(r)
    return doc.getvalue()


def send_email(result, task_data):

    # me == my email address
    # you == recipient's email address
    me = EMAIL_LOGIN
    you = task_data['email']
    # you = "sasha.pazuyk@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Search results for request "'+task_data['q']+'"'
    msg['From'] = me
    msg['To'] = you

    html = format_result(result)

    # Create the body of the message (a plain-text and an HTML version).
    # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"

    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    # msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    server = smtplib.SMTP(host=EMAIL_SMTP_HOST, port=EMAIL_SMTP_PORT)
    server.connect(host=EMAIL_SMTP_HOST, port=EMAIL_SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.login(me, EMAIL_PASS)
    server.sendmail(me, you, msg.as_string())
    server.close()


def log_results(results, task_data):

    log_task_data = {
        'q': task_data['q'],
        'email': task_data['email'],
        'took': results['took']
    }

    queue = Queue(TASK_QUEUE_LOG, config=TASK_QUEUE_CONNECTION)
    queue.connect()
    task = Task(log_task_data)
    queue.enqueue(task)


def get_task():

    es = Elasticsearch(ELASTICSEARCH_HOSTS, timeout=ELASTICSEARCH_TIMEOUT)

    queue = Queue(TASK_QUEUE_SEARCH, config=TASK_QUEUE_CONNECTION)
    queue.connect()
    while queue.length != 0:
        task = queue.dequeue()
        # task = queue.wait()
        if task:
            results = search(es, task.data['q'])
            send_email(results, task.data)
            log_results(results, task.data)


if __name__ == '__main__':
    get_task()

    # es_ = Elasticsearch(ELASTICSEARCH_HOSTS, timeout=ELASTICSEARCH_TIMEOUT)
    # task_ = {
    #     'q': 'sql',
    #     'email': 'sasha.pazuyk@gmail.com'
    # }
    #
    # results_ = search(es_, task_['q'])
    # send_email(results_, task_)
