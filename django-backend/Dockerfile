# pull official base image (platform must be linux/amd64 due to different CPU architecture between
# local Mac M1 and server linux.
# Alpine is not working for some reason
FROM --platform=linux/amd64 python:3.11

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NEW_RELIC_CONFIG_FILE=newrelic.ini \
    NEW_RELIC_ENVIRONMENT=production \
    NEW_RELIC_LOG=stdout \
    NEW_RELIC_LOG_LEVEL=info

# install dependencies
COPY ./prod-requirements.txt .
RUN pip install -r prod-requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

RUN adduser --disabled-password samoylovartem
USER samoylovartem

# run gunicorn
CMD python manage.py migrate --noinput && \
    newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT config.wsgi:application
