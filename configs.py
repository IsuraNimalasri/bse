# Task queue configuration
TASK_QUEUE_CONNECTION = {
        'host': '192.168.0.29',
        'port': 6379,
        'db': 0,
        'password': None,
    }
TASK_QUEUE_SEARCH = 'search'
TASK_QUEUE_LOG = 'log'

# E-mail configuration
EMAIL_LOGIN = 'results.bse@gmail.com'
EMAIL_PASS = 'Create your Google Account'
EMAIL_SMTP_HOST = 'smtp.gmail.com'
EMAIL_SMTP_PORT = 587

# Elasticsearch configuration
ELASTICSEARCH_HOSTS = ['192.168.0.29']
ELASTICSEARCH_TIMEOUT = 300
ELASTICSEARCH_INDEX = 'library'
ELASTICSEARCH_DOC_TYPE = 'book'

# Log configuration
LOG_FILENAME = 'requests.log'
LOG_FORMAT = '%(asctime)s | %(message)s'

