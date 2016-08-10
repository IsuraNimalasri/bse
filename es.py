import base64
import mimetypes

from os import listdir
from os.path import isfile, join

from elasticsearch import Elasticsearch


def create_index(es):
    index = 'library'
    doc_type = 'book'

    es.indices.create(index=index)

    mapping = {
        "book": {
            "properties": {
                "file": {
                    "type": "attachment",
                    "fields": {
                        "content": {"store": "yes"},
                        "title": {"store": "yes"},
                        "date": {"store": "yes"},
                        "author": {"store": "yes"},
                        "keywords": {"store": "yes"},
                        "content_type": {"store": "yes"},
                        "content_length": {"store": "yes"},
                        "language": {"store": "yes"}
                    }
                }
            }
        }
    }

    es.indices.put_mapping(doc_type=doc_type, body=mapping)


def add_book(es, file_path):
    index = 'library'
    doc_type = 'book'

    is_library = es.indices.exists(index=index)
    if not is_library:
        create_index(es)

    count = es.count(index=index, doc_type=doc_type)['count']
    print(count)

    with open(file_path, 'rb') as f:
        fb64 = base64.standard_b64encode(f.read()).decode()
        fname = f.name
        fmine = mimetypes.MimeTypes().guess_type(f.name)[0]

    doc = {
        "file": {
            "_content_type": fmine,
            "_name": fname,
            "_language": "en",
            "_content": fb64
        }
    }
    es.create(index=index, doc_type=doc_type, id=count, body=doc)
    es.indices.refresh(index=index)


def add_books_from_folder(es, folder_path):
    files_path = [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]
    for file_path in files_path:
        add_book(es, file_path)


def search(es, q):
    is_library = es.indices.exists(index='library')
    if not is_library:
        return 'No index "library" found'

    body = {
        "fields": ["file.title", "file.author"],
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

    params = {
        "timeout": "1ms"
    }

    results = es.search(index="library", body=body, params=params)
    return results

# if __name__ == '__main__':
    # es_ = Elasticsearch(['192.168.0.29'])
    # q_ = 'java'
    # create(es)
    # result = search(es_, q_)
    #
    # for hit in result['hits']['hits']:
    #     for html in hit['highlight']['file.content']:
    #         print(html)
        # print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

    # add_books_from_folder(es, '/home/sasha/Downloads/Books/')
    # add_book(es, '../books/Hello Web App.pdf')
    # add_book(es, '../books/10104297.epub')
