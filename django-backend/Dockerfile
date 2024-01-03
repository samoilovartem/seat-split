FROM --platform=linux/amd64 python:3.12 as builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

FROM --platform=linux/amd64 python:3.12

WORKDIR /app

ENV GUNICORN_TIMEOUT=0

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . ./

RUN groupadd -r django_group && \
    useradd -r -g django_group django_user

RUN chown -R django_user:django_group /app
RUN mkdir -p /app/media/django-import-export && \
    mkdir -p /app/media/avatars && \
    chown -R django_user:django_group /app/media && \
    chmod -R 775 /app/media && \
    chown -R django_user:django_group /app/media/django-import-export && \
    chown -R django_user:django_group /app/media/avatars && \
    chmod -R 775 /app/media/django-import-export && \
    chmod -R 775 /app/media/avatars \

USER django_user

RUN chmod +x ./entrypoint-prod.sh

CMD ["./entrypoint-prod.sh"]
