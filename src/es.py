from os import listdir
from os.path import isfile, join, basename
import sys
import mimetypes

from elasticsearch import Elasticsearch
import PyPDF2

from configs import (ELASTICSEARCH_HOSTS, ELASTICSEARCH_TIMEOUT, ELASTICSEARCH_INDEX, ELASTICSEARCH_DOC_TYPE)


def create_index(es):

    es.indices.create(index=ELASTICSEARCH_INDEX)

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

    es.indices.put_mapping(doc_type=ELASTICSEARCH_DOC_TYPE, body=mapping)


def add_book(es, file_path):

    is_library = es.indices.exists(index=ELASTICSEARCH_INDEX)
    if not is_library:
        create_index(es)

    count = es.count(index=ELASTICSEARCH_INDEX, doc_type=ELASTICSEARCH_DOC_TYPE)['count']
    print(count)

    with open(file_path, 'rb') as f:
        fname = basename(f.name)
        fmime = mimetypes.MimeTypes().guess_type(f.name)[0]

        if fmime == 'application/pdf':
            pdf = PyPDF2.PdfFileReader(f)
            if not pdf.isEncrypted:

                pages = pdf.numPages
                print(pages)

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

                es.create(index=ELASTICSEARCH_INDEX, doc_type=ELASTICSEARCH_DOC_TYPE, id=count, body=doc)
                es.indices.refresh(index=ELASTICSEARCH_INDEX)


def add_books_from_folder(es, folder_path):
    files_path = [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]
    for file_path in files_path:
        add_book(es, file_path)


def search(es, q):

    is_library = es.indices.exists(index=ELASTICSEARCH_INDEX)
    if not is_library:
        create_index(es)

    body = {
        "fields": ["content.page_number", "title", "file_name"],
        "query": {
            "match": {
                "content.text": q
            }
        },
        "highlight": {
            "number_of_fragments": 10000,
            "pre_tags": ["<b>"],
            "post_tags": ["</b>"],
            "fields": {
                "content.text": {
                }
            }
        }
    }

    results = es.search(index=ELASTICSEARCH_INDEX, body=body)
    return results


if __name__ == '__main__':

    es_ = Elasticsearch(ELASTICSEARCH_HOSTS, timeout=ELASTICSEARCH_TIMEOUT)

    if len(sys.argv) >= 2:
        path = sys.argv[1]

        add_books_from_folder(es_, path)
    else:
        print('Provide 1 argument as "/path/to/folder/".')
