Books Search Engine
===================

Books search engine powered by Elasticserch.

Built on Falcon minimalistic Python framework.

Requirements
------------

For Python requirements see

```
./requirements.txt
```

Mapper Attachments Type for Elasticsearch plugin

Redis

Build
-----

```
docker build -t falcon .
```

Run
---

Step-by-step instruction

#### Run containers

```
docker run --name redis -d redis

docker run --name elasticsearch -d elasticsearch

docker exec elasticsearch bin/plugin install mapper-attachments

docker run --name falcon --link redis:REDIS --link elasticsearch:ELASTICSEARCH -it -p 8000:8000 falcon /bin/bash

gunicorn -b 0.0.0.0:8000 bse:app &
```

#### Add books

```
python es.py /path/to/folder
```

#### Go to page and do search

```
http://localhost:8000/
```

#### Run workers

```
python search_task.py

python log_task.py
```

#### Observe logs

```
cat requests.log
```

Debug
-----

```
docker run --name kibana --link elasticsearch:elasticsearch -d kibana

docker exec kibana /opt/kibana/bin/kibana plugin --install elastic/sense

docker stop kibana

docker start kibana
```

License
-------

MIT