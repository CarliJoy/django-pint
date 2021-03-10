FROM python:3.8-slim

# install system dependencies

RUN apt-get update

RUN apt-get install -y build-essential libpq-dev curl gettext git postgresql-client

RUN pip3 install --upgrade wheel setuptools pip

RUN pip3 install pre-commit psycopg2-binary ipdb

WORKDIR /django-pint

# copy application files
COPY . /django-pint

RUN pre-commit install

RUN pip install -e '.[testing]'
