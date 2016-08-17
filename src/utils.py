import re
import os


def validate_email(email):
    """
    Check if entered value is valid email address.

    :param email: email address to validate.
    :type email: str
    :return: If valid return True. In other case False.
    :rtype: bool

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

    :param email: email address.
    :type email: str
    :return: username part of email address.
    :rtype: str

    >>> extract_username('username@domain.com')
    username
    """
    
    return email[:email.index('@')]


def save_file(book):
    """
    Save data in file.

    :param book: byte stream
    :type book: byte
    :return: absolute path to file
    :rtype: str
    """

    print(book.filename)
    raw = book.file.read()
    with open(book.filename, 'wb') as f:
        f.write(raw)
        return os.path.abspath(book.filename)


def delete_file(file_path):
    """
    Delete file by specified path.

    :param file_path: path to file
    :type file_path: str
    """

    os.remove(file_path)
