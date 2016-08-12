from os import listdir
from os.path import isfile, join, basename
import sys
import base64
import mimetypes

from elasticsearch import Elasticsearch

from configs import (ELASTICSEARCH_HOSTS, ELASTICSEARCH_TIMEOUT, ELASTICSEARCH_INDEX, ELASTICSEARCH_DOC_TYPE)


def create_index(es):

    es.indices.create(index=ELASTICSEARCH_INDEX)

    mapping = {
        ELASTICSEARCH_DOC_TYPE: {
            "properties": {
                "file": {
                    "type": "attachment",
                    "fields": {
                        "date": {"store": "yes"},
                        "title": {"store": "yes"},
                        "name": {"store": "yes"},
                        "author": {"store": "yes"},
                        "keywords": {"store": "yes"},
                        "content_type": {"store": "yes"},
                        "content_length": {"store": "yes"},
                        "language": {"store": "yes"},
                        "content": {"store": "yes"}
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
        fb64 = base64.standard_b64encode(f.read()).decode()
        fname = basename(f.name)
        fmine = mimetypes.MimeTypes().guess_type(f.name)[0]

    doc = {
        "file": {
            "_content_type": fmine,
            "_name": fname,
            "_language": "en",
            "_indexed_chars": -1,
            "_content": fb64
        }
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
        "fields": ["file.title", "file.name"],
        "query": {
            "match": {
                "file.content": {
                    "query": q,
                    "operator": "and"
                }
            }
        },
        "highlight": {
            "number_of_fragments": 10000,
            "pre_tags": ["<b>"],
            "post_tags": ["</b>"],
            "fields": {
                "file.content": {
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
