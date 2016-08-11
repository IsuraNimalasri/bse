FROM python:3.4.5

MAINTAINER Sasha

RUN \
	cd / && \
	mkdir falcon && \
	cd falcon && \
	git clone -b develop https://github.com/Sasha-P/bse.git && \
	ls && \
	cd bse && \
	pip install -r requirements/base.txt

EXPOSE 8000

WORKDIR /falcon/bse
CMD gunicorn -b 0.0.0.0:8000 bse:app
