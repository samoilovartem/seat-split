# pull official base image (platform must be linux/amd64 due to different CPU architecture between
# local Mac M1 and server linux.
# Alpine is not working for some reason
FROM --platform=linux/amd64 python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NEW_RELIC_CONFIG_FILE=newrelic.ini \
    NEW_RELIC_ENVIRONMENT=production \
    NEW_RELIC_LOG=stdout \
    NEW_RELIC_LOG_LEVEL=info \
    POETRY_VERSION=1.4.2 \
    GUNICORN_TIMEOUT=30

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

RUN python manage.py collectstatic --noinput

RUN adduser --disabled-password samoylovartem
USER samoylovartem

CMD python manage.py migrate --noinput && \
    newrelic-admin run-program gunicorn --timeout $GUNICORN_TIMEOUT --bind 0.0.0.0:$PORT config.wsgi:application
