import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from elasticsearch import Elasticsearch
from retask import Queue
from yattag import Doc

from es import search


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
                                text('<not_set>')
                        with tag('ol'):
                            for r in hit['highlight']['file.content']:
                                with tag('li'):
                                    doc.asis(r)
    return doc.getvalue()


def send_email(result, task_data):

    # me == my email address
    # you == recipient's email address
    me = "results.bse@gmail.com"
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
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.connect(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(me, 'Create your Google Account')
    server.sendmail(me, you, msg.as_string())
    server.close()


def get_task():
    config = {
        'host': '192.168.0.29',
        'port': 6379,
        'db': 0,
        'password': None,
    }

    es = Elasticsearch(['192.168.0.29'])

    queue = Queue('search', config=config)
    queue.connect()
    while queue.length != 0:
        # task = queue.dequeue()
        task = queue.wait()
        if task:
            results = search(es, task.data['q'])
            send_email(results, task.data)


if __name__ == '__main__':
    es_ = Elasticsearch(['192.168.0.29'])
    task_ = {
        'q': 'sql',
        'email': 'sasha.pazuyk@gmail.com'
    }

    results_ = search(es_, task_['q'])
    send_email(results_, task_)
