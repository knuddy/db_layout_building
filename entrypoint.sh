#!/bin/sh -c

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
uvicorn proj.asgi:application --reload --host 0.0.0.0 --port 8005

exec "$@"