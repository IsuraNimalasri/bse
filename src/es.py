from os import listdir
from os.path import isfile, join, basename
import sys
import mimetypes

from elasticsearch import Elasticsearch
import PyPDF2


from configs import (ELASTICSEARCH_HOSTS, ELASTICSEARCH_TIMEOUT, ELASTICSEARCH_INDEX, ELASTICSEARCH_DOC_TYPE)


def create_index():
    """
    Create index and mapping.

    :return: response data from es
    :rtype: dict
    """
    es = es_connect()

    is_library = index_exist()
    if type(is_library) is bool:
        if not is_library:

            create_index_data = es.indices.create(index=ELASTICSEARCH_INDEX)

            mapping = {
                ELASTICSEARCH_DOC_TYPE: {
                    "properties": {
                        "file_name": {
                            "store": "yes",
                            "type": "string"
                        },
                        "title": {
                            "store": "yes",
                            "type": "string"
                        },
                        "content": {
                            "type": "nested",
                            "properties": {
                                "page_number": {
                                    "store": "yes",
                                    "type": "integer"
                                },
                                "text": {
                                    "store": "yes",
                                    "type": "string"
                                }
                            }
                        }
                    }
                }
            }

            create_mapping_data = es.indices.put_mapping(doc_type=ELASTICSEARCH_DOC_TYPE, body=mapping)

            result = {
                'create_index_data': create_index_data,
                'create_mapping_data': create_mapping_data
            }

            return result
        else:
            return {'error': "index already exists. can't create."}
    else:
        return is_library


def delete_index():
    """
    Delete index.

    :return: response data from es
    :rtype: dict
    """
    es = es_connect()

    is_library = index_exist()
    if type(is_library) is bool:
        if is_library:
            return es.indices.delete(index=ELASTICSEARCH_INDEX)
        else:
            return {'error': "index don't exist. can't delete."}
    else:
        return is_library


def count_items():
    """
    Count items in index.

    :return: response data from es
    :rtype: dict
    """
    es = es_connect()

    is_library = index_exist()
    if type(is_library) is bool:
        if is_library:
            try:
                result = es.count(index=ELASTICSEARCH_INDEX, doc_type=ELASTICSEARCH_DOC_TYPE)
            except Exception as e:
                result = {'error': str(e)}
            return result
        else:
            return {'error': "index don't exist. can't count"}
    else:
        return is_library


def index_exist():

    es = es_connect()

    try:
        result = es.indices.exists(index=ELASTICSEARCH_INDEX)
    except Exception as e:
        result = {'error': str(e)}
    return result


def add_book(file_path):
    """
    Add book to index. Before adding check if index exist. If not then create it.

    :param file_path: path to file
    :type file_path: str
    :return: response data from es
    :rtype: dict
    """

    is_library = index_exist()
    if not is_library:
        create_index()

    create_book_data = {}

    with open(file_path, 'rb') as f:

        count = count_items()['count']
        print('Books in DB: {}'.format(count))

        fname = basename(f.name)
        fmime = mimetypes.MimeTypes().guess_type(f.name)[0]

        if fmime == 'application/pdf':
            pdf = PyPDF2.PdfFileReader(f)
            if not pdf.isEncrypted:

                pages = pdf.numPages
                print('Pages in book: {}'.format(pages))

                content = []
                for page_number in range(pages):
                    page = pdf.getPage(page_number)
                    text = page.extractText()

                    book_page = {
                        'page_number': page_number,
                        'text': text
                    }

                    content.append(book_page)

                title = pdf.getDocumentInfo().title

                doc = {
                    'file_name': fname,
                    'title': title,
                    'content': content
                }

                es = es_connect()

                create_book_data = es.create(index=ELASTICSEARCH_INDEX, doc_type=ELASTICSEARCH_DOC_TYPE, id=count,
                                             body=doc)
                es.indices.refresh(index=ELASTICSEARCH_INDEX)

    return create_book_data


def add_books_from_folder(folder_path):
    """
    Add books from specified folder.

    :param folder_path: path to file
    :type folder_path: str
    """
    files_path = [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]
    for file_path in files_path:
        add_book(file_path)


def search(q):
    """
    Perform search in index. Before searching check if index exist. If not then create it.

    :param q: search query
    :type q: str
    :return: response data from es
    :rtype: dict
    """
    es = es_connect()

    is_library = index_exist()
    if type(is_library) is bool:
        if not is_library:
            return {'error': "index don't exist. can't search."}
        else:
            body = {
                "fields": ["title", "file_name"],
                "query": {
                    "nested": {
                        "path": "content",
                        "query": {
                            "match": {"content.text": q}
                        },
                        "inner_hits": {
                            "fields": ["content.page_number"],
                            "size": 1000000,
                            "sort": [
                                {"content.page_number": {"order": "asc"}}
                            ]
                        }
                    }
                }
            }

            results = es.search(index=ELASTICSEARCH_INDEX, body=body)
            return results
    else:
        return is_library


def search_advanced(q):
    """
    Perform advanced search in index. Before searching check if index exist. If not then create it.

    :param q: search query structure
    :type q: str
    :return: response data from es
    :rtype: dict
    """
    es = es_connect()

    is_library = index_exist()
    if type(is_library) is bool:
        if is_library:
            results = es.search(index=ELASTICSEARCH_INDEX, body=q)
            return results
        else:
            return {'error': "index don't exist. can't search."}
    else:
        return is_library


def es_connect():
    """
    Return Elasticsearch connection

    :return: Elasticsearch class
    :rtype: :class: Elasticsearch
    """
    return Elasticsearch(ELASTICSEARCH_HOSTS, timeout=ELASTICSEARCH_TIMEOUT)


if __name__ == '__main__':

    if len(sys.argv) >= 2:
        path = sys.argv[1]

        add_books_from_folder(path)
    else:
        print('Provide 1 argument as "/path/to/folder/".')
