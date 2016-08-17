Books Search Engine
===================

Books search engine powered by Elasticserch.

Built on Falcon minimalistic Python framework and Celery task queue.

Packed in Docker container.

Requirements
------------

For Python requirements see

```
./requirements.txt
```

**Works only with books in `PDF` format!** May not work with non-latin alphabet. 

Build
-----

_(optional)_ Specify path to folder with books by replacing `/path/to/folder/` in docker-compose.yml

```
...

  web:
    build: .
    command: ./run_web.sh
    volumes:
      - ./src:/falcon/bse
      - /path/to/folder/:/opt/books/
    ports:
      - "8000:8000"
    depends_on:
      - elasticsearch

...
```

Run build command

```
docker-compose build
```

Run
---

Run composition

```
docker-compose up
```

_(optional)_ Add books to Elasticsearch 

```
docker exec bse_web_1 /bin/bash -c 'python es.py /opt/books/'
```

Go to admin page and create index or add book etc.

```
http://localhost:8000/admin
```

Go to page and do search

```
http://localhost:8000/
```

Observe logs

```
docker exec bse_web_1 cat requests.log
```

Cleanup

```
docker-compose down --rmi all
```

License
-------

MIT