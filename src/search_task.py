import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from elasticsearch import Elasticsearch

from yattag import Doc

from es import search
from configs import (ELASTICSEARCH_HOSTS, ELASTICSEARCH_TIMEOUT,
                     EMAIL_LOGIN, EMAIL_PASS, EMAIL_SMTP_HOST, EMAIL_SMTP_PORT)


def format_result(q, result):
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('body'):
            with tag('p'):
                text('Hi!')
            if 'hits' in result and 'hits' in result['hits'] and result['hits']['hits']:
                with tag('p'):
                    text('Here are your results:')
                with tag('ul', style='list-style-type:none;'):
                    for hit in result['hits']['hits']:
                        with tag('li'):
                            with tag('h2'):
                                if 'fields' in hit and 'title' in hit['fields'] and hit['fields']['title'][0]:
                                    text(hit['fields']['title'][0])
                                else:
                                    text(hit['fields']['file_name'][0])

                            inner_hits = hit['inner_hits']['content']['hits']['hits']
                            page_numbers = []
                            for inner_hit in inner_hits:
                                page_numbers.append(inner_hit['fields']['content.page_number'][0] + 1)

                            with tag('p'):
                                text('"{0}" found on page(s): {1}'.format(q, ', '.join(page_numbers)))
            else:
                with tag('p'):
                    text('Nothing found. Try again late!')

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

    html = format_result(task_data['q'], result)

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

    return log_task_data


def do_task(task_data):

    es = Elasticsearch(ELASTICSEARCH_HOSTS, timeout=ELASTICSEARCH_TIMEOUT)

    results = search(es, task_data['q'])
    send_email(results, task_data)
    log_task_data = log_results(results, task_data)
    return log_task_data
