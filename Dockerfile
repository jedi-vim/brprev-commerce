FROM python:3.6.9-alpine

WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

RUN pip install poetry==1.0.9

COPY poetry.lock /app

COPY pyproject.toml /app

RUN poetry config virtualenvs.create false && \
poetry install --no-dev --no-interaction --no-ansi --no-dev && \
pip uninstall --yes poetry

COPY . /app/

EXPOSE 4000
