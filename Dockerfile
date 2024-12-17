FROM python:3.10-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=off
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

WORKDIR /source

COPY . /source/

ARG INDEX=https://mirror-pypi.runflare.com/simple
ARG INDEX-URL=https://mirror-pypi.runflare.com/simple
ARG TRUSTED-HOST=mirror-pypi.runflare.com

RUN apt-get update -y && apt-get upgrade -y
RUN pip config --user set global.index ${INDEX} &&  pip config --user set global.index-url ${INDEX-URL} &&  pip config --user set global.trusted-host ${TRUSTED-HOST}
RUN pip install -U pip && pip install -r requirements.txt poetry
RUN poetry install --with dev
RUN python manage.py makemigrations && python manage.py migrate
RUN python manage.py generate_fake_data

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]