FROM python:3.4.5

MAINTAINER Sasha

ADD ./src /falcon/bse
ADD requirements.txt /falcon/bse/requirements.txt
ADD run_web.sh /falcon/bse/run_web.sh
ADD run_celery.sh /falcon/bse/run_celery.sh

WORKDIR /falcon/bse

RUN pip install -r requirements.txt

# create unprivileged user
RUN adduser --disabled-password --gecos '' fuser