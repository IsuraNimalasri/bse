import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from yattag import Doc

from es import search
from configs import (EMAIL_LOGIN, EMAIL_PASS, EMAIL_SMTP_HOST, EMAIL_SMTP_PORT)


def format_result(q, result):
    """
    Format result in html string for email.

    :param q: query string
    :param result: structure with search results
    :rtype result: dict
    :return: html formatted layout for email
    :rtype: str
    """

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
    """
    Send email with formatted results.

    :param result: search result
    :type result: dict
    :param task_data: task data
    :type task_data: dict
    """

    # me == my email address
    # you == recipient's email address
    me = EMAIL_LOGIN
    you = task_data['email']

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Search results for request "'+task_data['q']+'"'
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    html = format_result(task_data['q'], result)

    # Record the MIME type text/html.
    part = MIMEText(html, 'html')

    # Attach part into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part)

    # Send the message via local SMTP server.
    server = smtplib.SMTP(host=EMAIL_SMTP_HOST, port=EMAIL_SMTP_PORT)
    server.connect(host=EMAIL_SMTP_HOST, port=EMAIL_SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.login(me, EMAIL_PASS)
    server.sendmail(me, you, msg.as_string())
    server.close()


def log_results(result, task_data):
    """
    Form log task data.

    :param result: search result
    :type result: dict
    :param task_data: task data
    :type task_data: dict
    :return: data structure for log task
    :rtype: dict
    """

    log_task_data = {
        'q': task_data['q'],
        'email': task_data['email'],
        'took': result['took']
    }

    return log_task_data


def do_task(task_data):
    """
    Search, send result to email and run log task task.

    :param task_data: data to log
    :type task_data: dict
    :return: data structure for log task
    :rtype: dict
    """

    results = search(task_data['q'])
    send_email(results, task_data)
    log_task_data = log_results(results, task_data)
    return log_task_data
