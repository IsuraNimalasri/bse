===================
Books Search Engine
===================

Books search engine powered by Elasticserch.
Built on Falcon minimalistic Python framework.

Requirements
------------

For Python requirements see

::

  ./requirements/base.txt

::

Elasticsearch 2.1.2
Mapper Attachments Type for Elasticsearch 3.1.2
Redis 3.2.3

Run
---

docker run --name redis -d redis

docker run --name elasticsearch -d elasticsearch

docker run --name falcon --link redis:REDIS --link elasticsearch:ELASTICSEARCH -d -p 8000:8000 falcon