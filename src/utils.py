import re


def validate_email(email):
    """
    Check if entered value is valid email address.
    :param email: (str) email address to validate.
    :return: (bool) If valid return True. In other case False.

    >>> validate_email('a@b.com')
    True
    >>> validate_email('a_b@c.com')
    True
    >>> validate_email('a@b')
    False
    >>> validate_email('a.b.com')
    False
    """
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                     email)
    if match:
        return True
    return False


def extract_username(email):
    """
    Extract username part of email address. Email must be valid email address.
    :param email: (str) email address.
    :return: (str) username part of email address.

    >>> extract_username('username@domain.com')
    username
    """
    return email[:email.index('@')]
