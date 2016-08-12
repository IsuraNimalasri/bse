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

Run Step-by-step
----------------

#### Run containers

```
docker run --name redis -d redis

docker run --name elasticsearch -d elasticsearch

docker exec elasticsearch bin/plugin install mapper-attachments

docker stop elasticsearch && docker start elasticsearch

docker run --name rabbit --hostname rabbit -d rabbitmq
```

Replace `/path/to/folder/` to real path

```
docker run --name falcon -v /path/to/folder/:/opt/books/ --link rabbit:RABBIT --link redis:REDIS --link elasticsearch:ELASTICSEARCH -d -p 8000:8000 falcon
```

#### Add books

```
docker exec falcon /bin/bash -c 'python es.py /opt/books/'
```

#### Go to page and do search

```
http://localhost:8000/
```

#### Observe logs

```
docker exec falcon cat requests.log
```

#### Cleanup

```
docker stop elasticsearch redis falcon rabbit

docker rm elasticsearch redis falcon rabbit
```

Run shortcut
------------

#### Run containers

```
docker run --name redis -d redis && docker run --name elasticsearch -d elasticsearch && docker exec elasticsearch bin/plugin install mapper-attachments && docker stop elasticsearch && docker start elasticsearch && docker run --name rabbit --hostname rabbit -d rabbitmq
```

Replace `/path/to/folder/` to real path

```
docker run --name falcon -v /path/to/folder/:/opt/books/ --link rabbit:RABBIT --link redis:REDIS --link elasticsearch:ELASTICSEARCH -d -p 8000:8000 falcon
```

#### Add books

```
docker exec falcon /bin/bash -c 'python es.py /opt/books/'
```

#### Go to page and do search

```
http://localhost:8000/
```

#### Observe logs

```
docker exec falcon /bin/bash -c 'cat requests.log'
```

#### Cleanup

```
docker stop elasticsearch redis falcon rabbit && docker rm elasticsearch redis falcon rabbit
```

Debug
-----

```
docker run --name kibana --link elasticsearch:elasticsearch -d kibana

docker exec kibana /opt/kibana/bin/kibana plugin --install elastic/sense

docker stop kibana && docker start kibana
```

License
-------

MIT