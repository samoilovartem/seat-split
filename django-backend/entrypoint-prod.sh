#!/bin/sh

echo "Running as user: $(whoami)"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating STT staff group..."
python manage.py create_stt_staff_group

echo "Creating STT general superuser..."
python manage.py create_general_superuser

echo "Setting up periodic tasks..."
python manage.py setup_periodic_tasks

echo "Starting server..."
gunicorn --timeout "$GUNICORN_TIMEOUT" --bind 0.0.0.0:"$PORT" config.wsgi:application

echo "Server has started!"
