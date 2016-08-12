FROM python:3.4.5

MAINTAINER Sasha

RUN mkdir /falcon
ADD ./src /falcon/bse
ADD requirements.txt /falcon/bse/requirements.txt

WORKDIR /falcon/bse

RUN pip install -r requirements.txt

EXPOSE 8000

CMD gunicorn -b 0.0.0.0:8000 bse:app