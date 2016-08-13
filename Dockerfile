FROM python:3.4.5

MAINTAINER Sasha

ADD requirements.txt /falcon/bse/requirements.txt

WORKDIR /falcon/bse

RUN pip install -r requirements.txt

# create unprivileged user
RUN adduser --disabled-password --gecos '' fuser