# pull official base image (platform must be linux/amd64 due to different CPU architecture between
# local Mac M1 and server linux.
# Alpine is not working for some reason
FROM --platform=linux/amd64 python:3.11

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

RUN adduser --disabled-password samoylovartem
USER samoylovartem

# run gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT config.wsgi:application