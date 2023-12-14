FROM --platform=linux/amd64 python:3.12

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    GUNICORN_TIMEOUT=0

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install

COPY . .

RUN chmod +x ./entrypoint-prod.sh

CMD ["./entrypoint-prod.sh"]
