FROM --platform=linux/amd64 python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.4.2 \
    GUNICORN_TIMEOUT=0

RUN apt-get update && \
    apt-get install -y binutils libproj-dev gdal-bin && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install

COPY . .

RUN python manage.py collectstatic --noinput

CMD python manage.py migrate --noinput && \
    gunicorn --timeout $GUNICORN_TIMEOUT --bind 0.0.0.0:$PORT config.wsgi:application
