FROM python:3.8-alpine

WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev cargo

RUN pip install --upgrade pip

RUN pip install cryptography==2.8 

RUN pip install poetry==1.0.9

COPY poetry.lock /app

COPY pyproject.toml /app

RUN poetry config virtualenvs.create false && \
poetry install --no-dev --no-interaction --no-ansi --no-dev && \
pip uninstall --yes poetry

COPY . /app/

RUN chmod u+x docker_start.sh

EXPOSE 4000
